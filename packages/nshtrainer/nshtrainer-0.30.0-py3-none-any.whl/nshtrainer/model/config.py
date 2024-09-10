import copy
import logging
import os
import string
import time
from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from datetime import timedelta
from pathlib import Path
from typing import (
    Annotated,
    Any,
    ClassVar,
    Literal,
    Protocol,
    TypeAlias,
    runtime_checkable,
)

import nshconfig as C
import numpy as np
import torch
from lightning.fabric.plugins import CheckpointIO, ClusterEnvironment
from lightning.fabric.plugins.precision.precision import _PRECISION_INPUT
from lightning.pytorch.accelerators import Accelerator
from lightning.pytorch.callbacks.callback import Callback
from lightning.pytorch.loggers import Logger
from lightning.pytorch.plugins import _PLUGIN_INPUT
from lightning.pytorch.plugins.layer_sync import LayerSync
from lightning.pytorch.plugins.precision.precision import Precision
from lightning.pytorch.profilers import Profiler
from lightning.pytorch.strategies.strategy import Strategy
from typing_extensions import Self, TypedDict, TypeVar, override

from .._checkpoint.loader import CheckpointLoadingConfig
from .._hf_hub import HuggingFaceHubConfig
from ..callbacks import (
    BestCheckpointCallbackConfig,
    CallbackConfig,
    EarlyStoppingConfig,
    LastCheckpointCallbackConfig,
    OnExceptionCheckpointCallbackConfig,
)
from ..callbacks.base import CallbackConfigBase
from ..loggers import (
    CSVLoggerConfig,
    LoggerConfig,
    TensorboardLoggerConfig,
    WandbLoggerConfig,
)
from ..metrics import MetricConfig
from ..util._environment_info import EnvironmentConfig

log = logging.getLogger(__name__)


class BaseProfilerConfig(C.Config, ABC):
    dirpath: str | Path | None = None
    """
    Directory path for the ``filename``. If ``dirpath`` is ``None`` but ``filename`` is present, the
        ``trainer.log_dir`` (from :class:`~lightning.pytorch.loggers.tensorboard.TensorBoardLogger`)
        will be used.
    """
    filename: str | None = None
    """
    If present, filename where the profiler results will be saved instead of printing to stdout.
        The ``.txt`` extension will be used automatically.
    """

    @abstractmethod
    def create_profiler(self, root_config: "BaseConfig") -> Profiler: ...


class SimpleProfilerConfig(BaseProfilerConfig):
    name: Literal["simple"] = "simple"

    extended: bool = True
    """
    If ``True``, adds extra columns representing number of calls and percentage of
        total time spent onrespective action.
    """

    @override
    def create_profiler(self, root_config):
        from lightning.pytorch.profilers.simple import SimpleProfiler

        if (dirpath := self.dirpath) is None:
            dirpath = root_config.directory.resolve_subdirectory(
                root_config.id, "profile"
            )

        if (filename := self.filename) is None:
            filename = f"{root_config.id}_profile.txt"

        return SimpleProfiler(
            extended=self.extended,
            dirpath=dirpath,
            filename=filename,
        )


class AdvancedProfilerConfig(BaseProfilerConfig):
    name: Literal["advanced"] = "advanced"

    line_count_restriction: float = 1.0
    """
    This can be used to limit the number of functions
        reported for each action. either an integer (to select a count of lines),
        or a decimal fraction between 0.0 and 1.0 inclusive (to select a percentage of lines)
    """

    @override
    def create_profiler(self, root_config):
        from lightning.pytorch.profilers.advanced import AdvancedProfiler

        if (dirpath := self.dirpath) is None:
            dirpath = root_config.directory.resolve_subdirectory(
                root_config.id, "profile"
            )

        if (filename := self.filename) is None:
            filename = f"{root_config.id}_profile.txt"

        return AdvancedProfiler(
            line_count_restriction=self.line_count_restriction,
            dirpath=dirpath,
            filename=filename,
        )


class PyTorchProfilerConfig(BaseProfilerConfig):
    name: Literal["pytorch"] = "pytorch"

    group_by_input_shapes: bool = False
    """Include operator input shapes and group calls by shape."""

    emit_nvtx: bool = False
    """
    Context manager that makes every autograd operation emit an NVTX range
        Run::

            nvprof --profile-from-start off -o trace_name.prof -- <regular command here>

        To visualize, you can either use::

            nvvp trace_name.prof
            torch.autograd.profiler.load_nvprof(path)
    """

    export_to_chrome: bool = True
    """
    Whether to export the sequence of profiled operators for Chrome.
        It will generate a ``.json`` file which can be read by Chrome.
    """

    row_limit: int = 20
    """
    Limit the number of rows in a table, ``-1`` is a special value that
        removes the limit completely.
    """

    sort_by_key: str | None = None
    """
    Attribute used to sort entries. By default
        they are printed in the same order as they were registered.
        Valid keys include: ``cpu_time``, ``cuda_time``, ``cpu_time_total``,
        ``cuda_time_total``, ``cpu_memory_usage``, ``cuda_memory_usage``,
        ``self_cpu_memory_usage``, ``self_cuda_memory_usage``, ``count``.
    """

    record_module_names: bool = True
    """Whether to add module names while recording autograd operation."""

    table_kwargs: dict[str, Any] | None = None
    """Dictionary with keyword arguments for the summary table."""

    additional_profiler_kwargs: dict[str, Any] = {}
    """Keyword arguments for the PyTorch profiler. This depends on your PyTorch version"""

    @override
    def create_profiler(self, root_config):
        from lightning.pytorch.profilers.pytorch import PyTorchProfiler

        if (dirpath := self.dirpath) is None:
            dirpath = root_config.directory.resolve_subdirectory(
                root_config.id, "profile"
            )

        if (filename := self.filename) is None:
            filename = f"{root_config.id}_profile.txt"

        return PyTorchProfiler(
            group_by_input_shapes=self.group_by_input_shapes,
            emit_nvtx=self.emit_nvtx,
            export_to_chrome=self.export_to_chrome,
            row_limit=self.row_limit,
            sort_by_key=self.sort_by_key,
            record_module_names=self.record_module_names,
            table_kwargs=self.table_kwargs,
            dirpath=dirpath,
            filename=filename,
            **self.additional_profiler_kwargs,
        )


ProfilerConfig: TypeAlias = Annotated[
    SimpleProfilerConfig | AdvancedProfilerConfig | PyTorchProfilerConfig,
    C.Field(discriminator="name"),
]


class LoggingConfig(CallbackConfigBase):
    enabled: bool = True
    """Enable experiment tracking."""

    loggers: Sequence[LoggerConfig] = [
        WandbLoggerConfig(),
        CSVLoggerConfig(),
        TensorboardLoggerConfig(),
    ]
    """Loggers to use for experiment tracking."""

    log_lr: bool | Literal["step", "epoch"] = True
    """If enabled, will register a `LearningRateMonitor` callback to log the learning rate to the logger."""
    log_epoch: bool = True
    """If enabled, will log the fractional epoch number to the logger."""

    actsave_logged_metrics: bool = False
    """If enabled, will automatically save logged metrics using ActSave (if nshutils is installed)."""

    @property
    def wandb(self):
        return next(
            (
                logger
                for logger in self.loggers
                if isinstance(logger, WandbLoggerConfig)
            ),
            None,
        )

    @property
    def csv(self):
        return next(
            (logger for logger in self.loggers if isinstance(logger, CSVLoggerConfig)),
            None,
        )

    @property
    def tensorboard(self):
        return next(
            (
                logger
                for logger in self.loggers
                if isinstance(logger, TensorboardLoggerConfig)
            ),
            None,
        )

    def create_loggers(self, root_config: "BaseConfig"):
        """
        Constructs and returns a list of loggers based on the provided root configuration.

        Args:
            root_config (BaseConfig): The root configuration object.

        Returns:
            list[Logger]: A list of constructed loggers.
        """
        if not self.enabled:
            return

        for logger_config in sorted(
            self.loggers,
            key=lambda x: x.priority,
            reverse=True,
        ):
            if not logger_config.enabled:
                continue
            if (logger := logger_config.create_logger(root_config)) is None:
                continue
            yield logger

    @override
    def create_callbacks(self, root_config):
        if self.log_lr:
            from lightning.pytorch.callbacks import LearningRateMonitor

            logging_interval: str | None = None
            if isinstance(self.log_lr, str):
                logging_interval = self.log_lr

            yield LearningRateMonitor(logging_interval=logging_interval)

        if self.log_epoch:
            from ..callbacks.log_epoch import LogEpochCallback

            yield LogEpochCallback()

        for logger in self.loggers:
            if not logger or not isinstance(logger, CallbackConfigBase):
                continue

            yield from logger.create_callbacks(root_config)


class GradientClippingConfig(C.Config):
    enabled: bool = True
    """Enable gradient clipping."""
    value: int | float
    """Value to use for gradient clipping."""
    algorithm: Literal["value", "norm"] = "norm"
    """Norm type to use for gradient clipping."""


class OptimizationConfig(CallbackConfigBase):
    log_grad_norm: bool | str | float = False
    """If enabled, will log the gradient norm (averaged across all model parameters) to the logger."""
    log_grad_norm_per_param: bool | str | float = False
    """If enabled, will log the gradient norm for each model parameter to the logger."""

    log_param_norm: bool | str | float = False
    """If enabled, will log the parameter norm (averaged across all model parameters) to the logger."""
    log_param_norm_per_param: bool | str | float = False
    """If enabled, will log the parameter norm for each model parameter to the logger."""

    gradient_clipping: GradientClippingConfig | None = None
    """Gradient clipping configuration, or None to disable gradient clipping."""

    @override
    def create_callbacks(self, root_config):
        from ..callbacks.norm_logging import NormLoggingConfig

        yield from NormLoggingConfig(
            log_grad_norm=self.log_grad_norm,
            log_grad_norm_per_param=self.log_grad_norm_per_param,
            log_param_norm=self.log_param_norm,
            log_param_norm_per_param=self.log_param_norm_per_param,
        ).create_callbacks(root_config)


TPlugin = TypeVar(
    "TPlugin",
    Precision,
    ClusterEnvironment,
    CheckpointIO,
    LayerSync,
    infer_variance=True,
)


@runtime_checkable
class PluginConfigProtocol(Protocol[TPlugin]):
    def create_plugin(self) -> TPlugin: ...


@runtime_checkable
class AcceleratorConfigProtocol(Protocol):
    def create_accelerator(self) -> Accelerator: ...


@runtime_checkable
class StrategyConfigProtocol(Protocol):
    def create_strategy(self) -> Strategy: ...


AcceleratorLiteral: TypeAlias = Literal[
    "cpu", "gpu", "tpu", "ipu", "hpu", "mps", "auto"
]

StrategyLiteral: TypeAlias = Literal[
    "auto",
    "ddp",
    "ddp_find_unused_parameters_false",
    "ddp_find_unused_parameters_true",
    "ddp_spawn",
    "ddp_spawn_find_unused_parameters_false",
    "ddp_spawn_find_unused_parameters_true",
    "ddp_fork",
    "ddp_fork_find_unused_parameters_false",
    "ddp_fork_find_unused_parameters_true",
    "ddp_notebook",
    "dp",
    "deepspeed",
    "deepspeed_stage_1",
    "deepspeed_stage_1_offload",
    "deepspeed_stage_2",
    "deepspeed_stage_2_offload",
    "deepspeed_stage_3",
    "deepspeed_stage_3_offload",
    "deepspeed_stage_3_offload_nvme",
    "fsdp",
    "fsdp_cpu_offload",
    "single_xla",
    "xla_fsdp",
    "xla",
    "single_tpu",
]


def _create_symlink_to_nshrunner(base_dir: Path):
    # Resolve the current nshrunner session directory
    if not (session_dir := os.environ.get("NSHRUNNER_SESSION_DIR")):
        log.warning("NSHRUNNER_SESSION_DIR is not set. Skipping symlink creation.")
        return
    session_dir = Path(session_dir)
    if not session_dir.exists() or not session_dir.is_dir():
        log.warning(
            f"NSHRUNNER_SESSION_DIR is not a valid directory: {session_dir}. "
            "Skipping symlink creation."
        )
        return

    # Create the symlink
    symlink_path = base_dir / "nshrunner"
    if symlink_path.exists():
        # If it already points to the correct directory, we're done
        if symlink_path.resolve() == session_dir.resolve():
            return

        # Otherwise, we should log a warning and remove the existing symlink
        log.warning(
            f"A symlink pointing to {symlink_path.resolve()} already exists at {symlink_path}. "
            "Removing the existing symlink."
        )
        symlink_path.unlink()

    symlink_path.symlink_to(session_dir)


class DirectoryConfig(C.Config):
    project_root: Path | None = None
    """
    Root directory for this project.

    This isn't specific to the run; it is the parent directory of all runs.
    """

    create_symlink_to_nshrunner_root: bool = True
    """Should we create a symlink to the root folder for the Runner (if we're in one)?"""

    log: Path | None = None
    """Base directory for all experiment tracking (e.g., WandB, Tensorboard, etc.) files. If None, will use nshtrainer/{id}/log/."""

    stdio: Path | None = None
    """stdout/stderr log directory to use for the trainer. If None, will use nshtrainer/{id}/stdio/."""

    checkpoint: Path | None = None
    """Checkpoint directory to use for the trainer. If None, will use nshtrainer/{id}/checkpoint/."""

    activation: Path | None = None
    """Activation directory to use for the trainer. If None, will use nshtrainer/{id}/activation/."""

    profile: Path | None = None
    """Directory to save profiling information to. If None, will use nshtrainer/{id}/profile/."""

    def resolve_run_root_directory(self, run_id: str) -> Path:
        if (project_root_dir := self.project_root) is None:
            project_root_dir = Path.cwd()

        # The default base dir is $CWD/nshtrainer/{id}/
        base_dir = project_root_dir / "nshtrainer"
        base_dir.mkdir(exist_ok=True)

        # Add a .gitignore file to the nshtrainer directory
        #   which will ignore all files except for the .gitignore file itself
        gitignore_path = base_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.touch()
            gitignore_path.write_text("*\n")

        base_dir = base_dir / run_id
        base_dir.mkdir(exist_ok=True)

        # Create a symlink to the root folder for the Runner
        if self.create_symlink_to_nshrunner_root:
            _create_symlink_to_nshrunner(base_dir)

        return base_dir

    def resolve_subdirectory(
        self,
        run_id: str,
        # subdirectory: Literal["log", "stdio", "checkpoint", "activation", "profile"],
        subdirectory: str,
    ) -> Path:
        # The subdir will be $CWD/nshtrainer/{id}/{log, stdio, checkpoint, activation}/
        if (subdir := getattr(self, subdirectory, None)) is not None:
            assert isinstance(
                subdir, Path
            ), f"Expected a Path for {subdirectory}, got {type(subdir)}"
            return subdir

        dir = self.resolve_run_root_directory(run_id)
        dir = dir / subdirectory
        dir.mkdir(exist_ok=True)
        return dir

    def _resolve_log_directory_for_logger(
        self,
        run_id: str,
        logger: LoggerConfig,
    ) -> Path:
        if (log_dir := logger.log_dir) is not None:
            return log_dir

        # Save to nshtrainer/{id}/log/{logger name}
        log_dir = self.resolve_subdirectory(run_id, "log")
        log_dir = log_dir / logger.name
        log_dir.mkdir(exist_ok=True)

        return log_dir


class ReproducibilityConfig(C.Config):
    deterministic: bool | Literal["warn"] | None = None
    """
    If ``True``, sets whether PyTorch operations must use deterministic algorithms.
        Set to ``"warn"`` to use deterministic algorithms whenever possible, throwing warnings on operations
        that don't support deterministic mode. If not set, defaults to ``False``. Default: ``None``.
    """


CheckpointCallbackConfig: TypeAlias = Annotated[
    BestCheckpointCallbackConfig
    | LastCheckpointCallbackConfig
    | OnExceptionCheckpointCallbackConfig,
    C.Field(discriminator="name"),
]


class CheckpointSavingConfig(CallbackConfigBase):
    enabled: bool = True
    """Enable checkpoint saving."""

    checkpoint_callbacks: Sequence[CheckpointCallbackConfig] = [
        BestCheckpointCallbackConfig(),
        LastCheckpointCallbackConfig(),
        OnExceptionCheckpointCallbackConfig(),
    ]
    """Checkpoint callback configurations."""

    def disable_(self):
        self.enabled = False
        return self

    def should_save_checkpoints(self, root_config: "BaseConfig"):
        if not self.enabled:
            return False

        if root_config.trainer.fast_dev_run:
            return False

        return True

    @override
    def create_callbacks(self, root_config: "BaseConfig"):
        if not self.should_save_checkpoints(root_config):
            return

        for callback_config in self.checkpoint_callbacks:
            yield from callback_config.create_callbacks(root_config)


class LightningTrainerKwargs(TypedDict, total=False):
    accelerator: str | Accelerator
    """Supports passing different accelerator types ("cpu", "gpu", "tpu", "ipu", "hpu", "mps", "auto")
    as well as custom accelerator instances."""

    strategy: str | Strategy
    """Supports different training strategies with aliases as well custom strategies.
    Default: ``"auto"``.
    """

    devices: list[int] | str | int
    """The devices to use. Can be set to a positive number (int or str), a sequence of device indices
    (list or str), the value ``-1`` to indicate all available devices should be used, or ``"auto"`` for
    automatic selection based on the chosen accelerator. Default: ``"auto"``.
    """

    num_nodes: int
    """Number of GPU nodes for distributed training.
    Default: ``1``.
    """

    precision: _PRECISION_INPUT | None
    """Double precision (64, '64' or '64-true'), full precision (32, '32' or '32-true'),
    16bit mixed precision (16, '16', '16-mixed') or bfloat16 mixed precision ('bf16', 'bf16-mixed').
    Can be used on CPU, GPU, TPUs, HPUs or IPUs.
    Default: ``'32-true'``.
    """

    logger: Logger | Iterable[Logger] | bool | None
    """Logger (or iterable collection of loggers) for experiment tracking. A ``True`` value uses
    the default ``TensorBoardLogger`` if it is installed, otherwise ``CSVLogger``.
    ``False`` will disable logging. If multiple loggers are provided, local files
    (checkpoints, profiler traces, etc.) are saved in the ``log_dir`` of the first logger.
    Default: ``True``.
    """

    callbacks: list[Callback] | Callback | None
    """Add a callback or list of callbacks.
    Default: ``None``.
    """

    fast_dev_run: int | bool
    """Runs n if set to ``n`` (int) else 1 if set to ``True`` batch(es)
    of train, val and test to find any bugs (ie: a sort of unit test).
    Default: ``False``.
    """

    max_epochs: int | None
    """Stop training once this number of epochs is reached. Disabled by default (None).
    If both max_epochs and max_steps are not specified, defaults to ``max_epochs = 1000``.
    To enable infinite training, set ``max_epochs = -1``.
    """

    min_epochs: int | None
    """Force training for at least these many epochs. Disabled by default (None).
    """

    max_steps: int
    """Stop training after this number of steps. Disabled by default (-1). If ``max_steps = -1``
    and ``max_epochs = None``, will default to ``max_epochs = 1000``. To enable infinite training, set
    ``max_epochs`` to ``-1``.
    """

    min_steps: int | None
    """Force training for at least these number of steps. Disabled by default (``None``).
    """

    max_time: str | timedelta | dict[str, int] | None
    """Stop training after this amount of time has passed. Disabled by default (``None``).
    The time duration can be specified in the format DD:HH:MM:SS (days, hours, minutes seconds), as a
    :class:`datetime.timedelta`, or a dictionary with keys that will be passed to
    :class:`datetime.timedelta`.
    """

    limit_train_batches: int | float | None
    """How much of training dataset to check (float = fraction, int = num_batches).
    Default: ``1.0``.
    """

    limit_val_batches: int | float | None
    """How much of validation dataset to check (float = fraction, int = num_batches).
    Default: ``1.0``.
    """

    limit_test_batches: int | float | None
    """How much of test dataset to check (float = fraction, int = num_batches).
    Default: ``1.0``.
    """

    limit_predict_batches: int | float | None
    """How much of prediction dataset to check (float = fraction, int = num_batches).
    Default: ``1.0``.
    """

    overfit_batches: int | float
    """Overfit a fraction of training/validation data (float) or a set number of batches (int).
    Default: ``0.0``.
    """

    val_check_interval: int | float | None
    """How often to check the validation set. Pass a ``float`` in the range [0.0, 1.0] to check
    after a fraction of the training epoch. Pass an ``int`` to check after a fixed number of training
    batches. An ``int`` value can only be higher than the number of training batches when
    ``check_val_every_n_epoch=None``, which validates after every ``N`` training batches
    across epochs or during iteration-based training.
    Default: ``1.0``.
    """

    check_val_every_n_epoch: int | None
    """Perform a validation loop every after every `N` training epochs. If ``None``,
    validation will be done solely based on the number of training batches, requiring ``val_check_interval``
    to be an integer value.
    Default: ``1``.
    """

    num_sanity_val_steps: int | None
    """Sanity check runs n validation batches before starting the training routine.
    Set it to `-1` to run all batches in all validation dataloaders.
    Default: ``2``.
    """

    log_every_n_steps: int | None
    """How often to log within steps.
    Default: ``50``.
    """

    enable_checkpointing: bool | None
    """If ``True``, enable checkpointing.
    It will configure a default ModelCheckpoint callback if there is no user-defined ModelCheckpoint in
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.callbacks`.
    Default: ``True``.
    """

    enable_progress_bar: bool | None
    """Whether to enable to progress bar by default.
    Default: ``True``.
    """

    enable_model_summary: bool | None
    """Whether to enable model summarization by default.
    Default: ``True``.
    """

    accumulate_grad_batches: int
    """Accumulates gradients over k batches before stepping the optimizer.
    Default: 1.
    """

    gradient_clip_val: int | float | None
    """The value at which to clip gradients. Passing ``gradient_clip_val=None`` disables
    gradient clipping. If using Automatic Mixed Precision (AMP), the gradients will be unscaled before.
    Default: ``None``.
    """

    gradient_clip_algorithm: str | None
    """The gradient clipping algorithm to use. Pass ``gradient_clip_algorithm="value"``
    to clip by value, and ``gradient_clip_algorithm="norm"`` to clip by norm. By default it will
    be set to ``"norm"``.
    """

    deterministic: bool | Literal["warn"] | None
    """If ``True``, sets whether PyTorch operations must use deterministic algorithms.
    Set to ``"warn"`` to use deterministic algorithms whenever possible, throwing warnings on operations
    that don't support deterministic mode. If not set, defaults to ``False``. Default: ``None``.
    """

    benchmark: bool | None
    """The value (``True`` or ``False``) to set ``torch.backends.cudnn.benchmark`` to.
    The value for ``torch.backends.cudnn.benchmark`` set in the current session will be used
    (``False`` if not manually set). If :paramref:`~lightning.pytorch.trainer.trainer.Trainer.deterministic`
    is set to ``True``, this will default to ``False``. Override to manually set a different value.
    Default: ``None``.
    """

    inference_mode: bool
    """Whether to use :func:`torch.inference_mode` or :func:`torch.no_grad` during
    evaluation (``validate``/``test``/``predict``).
    """

    use_distributed_sampler: bool
    """Whether to wrap the DataLoader's sampler with
    :class:`torch.utils.data.DistributedSampler`. If not specified this is toggled automatically for
    strategies that require it. By default, it will add ``shuffle=True`` for the train sampler and
    ``shuffle=False`` for validation/test/predict samplers. If you want to disable this logic, you can pass
    ``False`` and add your own distributed sampler in the dataloader hooks. If ``True`` and a distributed
    sampler was already added, Lightning will not replace the existing one. For iterable-style datasets,
    we don't do this automatically.
    """

    profiler: Profiler | str | None
    """To profile individual steps during training and assist in identifying bottlenecks.
    Default: ``None``.
    """

    detect_anomaly: bool
    """Enable anomaly detection for the autograd engine.
    Default: ``False``.
    """

    barebones: bool
    """Whether to run in "barebones mode", where all features that may impact raw speed are
    disabled. This is meant for analyzing the Trainer overhead and is discouraged during regular training
    runs. The following features are deactivated:
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.enable_checkpointing`,
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.logger`,
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.enable_progress_bar`,
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.log_every_n_steps`,
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.enable_model_summary`,
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.num_sanity_val_steps`,
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.fast_dev_run`,
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.detect_anomaly`,
    :paramref:`~lightning.pytorch.trainer.trainer.Trainer.profiler`,
    :meth:`~lightning.pytorch.core.LightningModule.log`,
    :meth:`~lightning.pytorch.core.LightningModule.log_dict`.
    """

    plugins: _PLUGIN_INPUT | list[_PLUGIN_INPUT] | None
    """Plugins allow modification of core behavior like ddp and amp, and enable custom lightning plugins.
    Default: ``None``.
    """

    sync_batchnorm: bool
    """Synchronize batch norm layers between process groups/whole world.
    Default: ``False``.
    """

    reload_dataloaders_every_n_epochs: int
    """Set to a positive integer to reload dataloaders every n epochs.
    Default: ``0``.
    """

    default_root_dir: Path | None
    """Default path for logs and weights when no logger/ckpt_callback passed.
    Default: ``os.getcwd()``.
    Can be remote file paths such as `s3://mybucket/path` or 'hdfs://path/'
    """


class SanityCheckingConfig(C.Config):
    reduce_lr_on_plateau: Literal["disable", "error", "warn"] = "error"
    """
    If enabled, will do some sanity checks if the `ReduceLROnPlateau` scheduler is used:
        - If the `interval` is step, it makes sure that validation is called every `frequency` steps.
        - If the `interval` is epoch, it makes sure that validation is called every `frequency` epochs.
    Valid values are: "disable", "warn", "error".
    """


class TrainerConfig(C.Config):
    ckpt_path: Literal["none"] | str | Path | None = None
    """Path to a checkpoint to load and resume training from. If ``"none"``, will not load a checkpoint."""

    checkpoint_loading: CheckpointLoadingConfig | Literal["auto", "none"] = "auto"
    """Checkpoint loading configuration options.
    `"auto"` will automatically determine the best checkpoint loading strategy based on the provided.
    `"none"` will disable checkpoint loading.
    """

    checkpoint_saving: CheckpointSavingConfig = CheckpointSavingConfig()
    """Checkpoint saving configuration options."""

    hf_hub: HuggingFaceHubConfig = HuggingFaceHubConfig()
    """Hugging Face Hub configuration options."""

    logging: LoggingConfig = LoggingConfig()
    """Logging/experiment tracking (e.g., WandB) configuration options."""

    optimizer: OptimizationConfig = OptimizationConfig()
    """Optimization configuration options."""

    reproducibility: ReproducibilityConfig = ReproducibilityConfig()
    """Reproducibility configuration options."""

    sanity_checking: SanityCheckingConfig = SanityCheckingConfig()
    """Sanity checking configuration options."""

    early_stopping: EarlyStoppingConfig | None = None
    """Early stopping configuration options."""

    profiler: ProfilerConfig | None = None
    """
    To profile individual steps during training and assist in identifying bottlenecks.
        Default: ``None``.
    """

    callbacks: list[CallbackConfig] = []
    """Callbacks to use during training."""

    detect_anomaly: bool | None = None
    """Enable anomaly detection for the autograd engine.
    Default: ``False``.
    """

    plugins: list[PluginConfigProtocol] | None = None
    """
    Plugins allow modification of core behavior like ddp and amp, and enable custom lightning plugins.
        Default: ``None``.
    """

    auto_determine_num_nodes: bool = True
    """
    If enabled, will automatically determine the number of nodes for distributed training.

    This will only work on:
    - SLURM clusters
    - LSF clusters
    """

    fast_dev_run: int | bool = False
    """Runs n if set to ``n`` (int) else 1 if set to ``True`` batch(es)
    of train, val and test to find any bugs (ie: a sort of unit test).
    Default: ``False``.
    """

    precision: (
        Literal[
            "64-true",
            "32-true",
            "fp16-mixed",
            "bf16-mixed",
            "16-mixed-auto",
        ]
        | None
    ) = None
    """
    Training precision. Can be one of:
        - "64-true": Double precision (64-bit).
        - "32-true": Full precision (32-bit).
        - "fp16-mixed": Float16 mixed precision.
        - "bf16-mixed": BFloat16 mixed precision.
        - "16-mixed-auto": Automatic 16-bit: Uses bfloat16 if available, otherwise float16.
    """

    max_epochs: int | None = None
    """Stop training once this number of epochs is reached. Disabled by default (None).
    If both max_epochs and max_steps are not specified, defaults to ``max_epochs = 1000``.
    To enable infinite training, set ``max_epochs = -1``.
    """

    min_epochs: int | None = None
    """Force training for at least these many epochs. Disabled by default (None).
    """

    max_steps: int = -1
    """Stop training after this number of steps. Disabled by default (-1). If ``max_steps = -1``
    and ``max_epochs = None``, will default to ``max_epochs = 1000``. To enable infinite training, set
    ``max_epochs`` to ``-1``.
    """

    min_steps: int | None = None
    """Force training for at least these number of steps. Disabled by default (``None``).
    """

    max_time: str | timedelta | dict[str, int] | None = None
    """Stop training after this amount of time has passed. Disabled by default (``None``).
    The time duration can be specified in the format DD:HH:MM:SS (days, hours, minutes seconds), as a
    :class:`datetime.timedelta`, or a dictionary with keys that will be passed to
    :class:`datetime.timedelta`.
    """

    limit_train_batches: int | float | None = None
    """How much of training dataset to check (float = fraction, int = num_batches).
    Default: ``1.0``.
    """

    limit_val_batches: int | float | None = None
    """How much of validation dataset to check (float = fraction, int = num_batches).
    Default: ``1.0``.
    """

    limit_test_batches: int | float | None = None
    """How much of test dataset to check (float = fraction, int = num_batches).
    Default: ``1.0``.
    """

    limit_predict_batches: int | float | None = None
    """How much of prediction dataset to check (float = fraction, int = num_batches).
    Default: ``1.0``.
    """

    overfit_batches: int | float = 0.0
    """Overfit a fraction of training/validation data (float) or a set number of batches (int).
    Default: ``0.0``.
    """

    val_check_interval: int | float | None = None
    """How often to check the validation set. Pass a ``float`` in the range [0.0, 1.0] to check
    after a fraction of the training epoch. Pass an ``int`` to check after a fixed number of training
    batches. An ``int`` value can only be higher than the number of training batches when
    ``check_val_every_n_epoch=None``, which validates after every ``N`` training batches
    across epochs or during iteration-based training.
    Default: ``1.0``.
    """

    check_val_every_n_epoch: int | None = 1
    """Perform a validation loop every after every `N` training epochs. If ``None``,
    validation will be done solely based on the number of training batches, requiring ``val_check_interval``
    to be an integer value.
    Default: ``1``.
    """

    num_sanity_val_steps: int | None = None
    """Sanity check runs n validation batches before starting the training routine.
    Set it to `-1` to run all batches in all validation dataloaders.
    Default: ``2``.
    """

    log_every_n_steps: int | None = None
    """How often to log within steps.
    Default: ``50``.
    """

    inference_mode: bool = True
    """Whether to use :func:`torch.inference_mode` (if `True`) or :func:`torch.no_grad` (if `False`) during evaluation (``validate``/``test``/``predict``).
    Default: ``True``.
    """

    use_distributed_sampler: bool | None = None
    """Whether to wrap the DataLoader's sampler with
    :class:`torch.utils.data.DistributedSampler`. If not specified this is toggled automatically for
    strategies that require it. By default, it will add ``shuffle=True`` for the train sampler and
    ``shuffle=False`` for validation/test/predict samplers. If you want to disable this logic, you can pass
    ``False`` and add your own distributed sampler in the dataloader hooks. If ``True`` and a distributed
    sampler was already added, Lightning will not replace the existing one. For iterable-style datasets,
    we don't do this automatically.
    Default: ``True``.
    """

    accelerator: AcceleratorConfigProtocol | AcceleratorLiteral | None = None
    """Supports passing different accelerator types ("cpu", "gpu", "tpu", "ipu", "hpu", "mps", "auto")
    as well as custom accelerator instances.
    Default: ``"auto"``.
    """

    strategy: StrategyConfigProtocol | StrategyLiteral | None = None
    """Supports different training strategies with aliases as well custom strategies.
    Default: ``"auto"``.
    """

    devices: tuple[int, ...] | Sequence[int] | Literal["auto", "all"] | None = None
    """The devices to use. Can be set to a sequence of device indices, "all" to indicate all available devices should be used, or ``"auto"`` for
    automatic selection based on the chosen accelerator. Default: ``"auto"``.
    """

    auto_set_default_root_dir: bool = True
    """If enabled, will automatically set the default root dir to [cwd/lightning_logs/<id>/]. There is basically no reason to disable this."""
    supports_shared_parameters: bool = True
    """If enabled, the model supports scaling the gradients of shared parameters that are registered using `LightningModuleBase.register_shared_parameters(...)`"""
    save_checkpoint_metadata: bool = True
    """If enabled, will save additional metadata whenever a checkpoint is saved."""

    lightning_kwargs: LightningTrainerKwargs = LightningTrainerKwargs()
    """
    Additional keyword arguments to pass to the Lightning `pl.Trainer` constructor.

    Please refer to the Lightning documentation for a list of valid keyword arguments.
    """

    additional_lightning_kwargs: dict[str, Any] = {}
    """
    Additional keyword arguments to pass to the Lightning `pl.Trainer` constructor.

    This is essentially a non-type-checked version of `lightning_kwargs`.
    """

    set_float32_matmul_precision: Literal["medium", "high", "highest"] | None = None
    """If enabled, will set the torch float32 matmul precision to the specified value. Useful for faster training on Ampere+ GPUs."""


PrimaryMetricConfig: TypeAlias = MetricConfig


class BaseConfig(C.Config):
    id: str = C.Field(default_factory=lambda: BaseConfig.generate_id())
    """ID of the run."""
    name: str | None = None
    """Run name."""
    name_parts: list[str] = []
    """A list of parts used to construct the run name. This is useful for constructing the run name dynamically."""
    project: str | None = None
    """Project name."""
    tags: list[str] = []
    """Tags for the run."""
    notes: list[str] = []
    """Human readable notes for the run."""

    debug: bool = False
    """Whether to run in debug mode. This will enable debug logging and enable debug code paths."""
    environment: Annotated[EnvironmentConfig, C.Field(repr=False)] = (
        EnvironmentConfig.empty()
    )
    """A snapshot of the current environment information (e.g. python version, slurm info, etc.). This is automatically populated by the run script."""

    directory: DirectoryConfig = DirectoryConfig()
    """Directory configuration options."""
    trainer: TrainerConfig = TrainerConfig()
    """PyTorch Lightning trainer configuration options. Check Lightning's `Trainer` documentation for more information."""

    primary_metric: PrimaryMetricConfig | None = None
    """Primary metric configuration options. This is used in the following ways:
    - To determine the best model checkpoint to save with the ModelCheckpoint callback.
    - To monitor the primary metric during training and stop training based on the `early_stopping` configuration.
    - For the ReduceLROnPlateau scheduler.
    """

    meta: dict[str, Any] = {}
    """Additional metadata for this run. This can be used to store arbitrary data that is not part of the config schema."""

    @property
    def run_name(self) -> str:
        parts = self.name_parts.copy()
        if self.name is not None:
            parts = [self.name] + parts
        name = "-".join(parts)
        if not name:
            name = self.id
        return name

    def clone(self, with_new_id: bool = True) -> Self:
        c = copy.deepcopy(self)
        if with_new_id:
            c.id = BaseConfig.generate_id()
        return c

    def subdirectory(self, subdirectory: str) -> Path:
        return self.directory.resolve_subdirectory(self.id, subdirectory)

    # region Helper methods
    def with_project_root_(self, project_root: str | Path | os.PathLike) -> Self:
        """
        Set the project root directory for the trainer.

        Args:
            project_root (Path): The base directory to use.

        Returns:
            self: The current instance of the class.
        """
        self.directory.project_root = Path(project_root)
        return self

    def reset_(
        self,
        *,
        id: bool = True,
        basic: bool = True,
        project_root: bool = True,
        environment: bool = True,
        meta: bool = True,
    ):
        """
        Reset the configuration object to its initial state.

        Parameters:
        - id (bool): If True, generate a new ID for the configuration object.
        - basic (bool): If True, reset basic attributes like name, project, tags, and notes.
        - project_root (bool): If True, reset the directory configuration to its initial state.
        - environment (bool): If True, reset the environment configuration to its initial state.
        - meta (bool): If True, reset the meta dictionary to an empty dictionary.

        Returns:
        - self: The updated configuration object.

        """
        if id:
            self.id = self.generate_id()

        if basic:
            self.name = None
            self.name_parts = []
            self.project = None
            self.tags = []
            self.notes = []

        if project_root:
            self.directory = DirectoryConfig()

        if environment:
            self.environment = EnvironmentConfig.empty()

        if meta:
            self.meta = {}

        return self

    def concise_repr(self) -> str:
        """Get a concise representation of the configuration object."""

        def _truncate(s: str, max_len: int = 50):
            return s if len(s) <= max_len else f"{s[:max_len - 3]}..."

        cls_name = self.__class__.__name__

        parts: list[str] = []
        parts.append(f"name={self.run_name}")
        if self.project:
            parts.append(f"project={_truncate(self.project)}")

        return f"{cls_name}({', '.join(parts)})"

    # endregion

    # region Seeding

    _rng: ClassVar[np.random.Generator | None] = None

    @staticmethod
    def generate_id(*, length: int = 8) -> str:
        """
        Generate a random ID of specified length.

        """
        if (rng := BaseConfig._rng) is None:
            rng = np.random.default_rng()

        alphabet = list(string.ascii_lowercase + string.digits)

        id = "".join(rng.choice(alphabet) for _ in range(length))
        return id

    @staticmethod
    def set_seed(seed: int | None = None) -> None:
        """
        Set the seed for the random number generator.

        Args:
            seed (int | None, optional): The seed value to set. If None, a seed based on the current time will be used. Defaults to None.

        Returns:
            None
        """
        if seed is None:
            seed = int(time.time() * 1000)
        log.critical(f"Seeding BaseConfig with seed {seed}")
        BaseConfig._rng = np.random.default_rng(seed)

    # endregion

    @classmethod
    def from_checkpoint(
        cls,
        path: str | Path,
        *,
        hparams_key: str = "hyper_parameters",
    ):
        ckpt = torch.load(path)
        if (hparams := ckpt.get(hparams_key)) is None:
            raise ValueError(
                f"The checkpoint does not contain the `{hparams_key}` attribute. "
                "Are you sure this is a valid Lightning checkpoint?"
            )
        return cls.model_validate(hparams)

    def _nshtrainer_all_callback_configs(self) -> Iterable[CallbackConfigBase | None]:
        yield self.trainer.early_stopping
        yield self.trainer.checkpoint_saving
        yield self.trainer.logging
        yield self.trainer.optimizer
        yield self.trainer.hf_hub
        yield from self.trainer.callbacks
