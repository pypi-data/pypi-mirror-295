import importlib.metadata
import logging
from typing import TYPE_CHECKING, Literal

import nshconfig as C
from lightning.pytorch import Callback, LightningModule, Trainer
from packaging import version
from typing_extensions import override

from ..callbacks import WandbWatchConfig
from ..callbacks.base import CallbackConfigBase
from ._base import BaseLoggerConfig

if TYPE_CHECKING:
    from ..model.config import BaseConfig

log = logging.getLogger(__name__)


def _project_name(
    root_config: "BaseConfig",
    default_project: str = "lightning_logs",
):
    # If the config has a project name, use that.
    if project := root_config.project:
        return project

    # Otherwise, we should use the name of the module that the config is defined in,
    #   if we can find it.
    # If this isn't in a module, use the default project name.
    if not (module := root_config.__module__):
        return default_project

    # If the module is a package, use the package name.
    if not (module := module.split(".", maxsplit=1)[0].strip()):
        return default_project

    return module


def _wandb_available():
    try:
        from lightning.pytorch.loggers.wandb import _WANDB_AVAILABLE

        if not _WANDB_AVAILABLE:
            log.warning("WandB not found. Disabling WandbLogger.")
            return False
        return True
    except ImportError:
        return False


class FinishWandbOnTeardownCallback(Callback):
    @override
    def teardown(
        self,
        trainer: Trainer,
        pl_module: LightningModule,
        stage: str,
    ):
        try:
            import wandb  # type: ignore
        except ImportError:
            return

        if wandb.run is None:
            return

        wandb.finish()


class WandbLoggerConfig(CallbackConfigBase, BaseLoggerConfig):
    name: Literal["wandb"] = "wandb"

    enabled: bool = C.Field(default_factory=lambda: _wandb_available())
    """Enable WandB logging."""

    priority: int = 2
    """Priority of the logger. Higher priority loggers are created first,
    and the highest priority logger is the "main" logger for PyTorch Lightning."""

    project: str | None = None
    """WandB project name to use for the logger. If None, will use the root config's project name."""

    log_model: bool | Literal["all"] = False
    """
    Whether to log the model checkpoints to wandb.
    Valid values are:
        - False: Do not log the model checkpoints.
        - True: Log the latest model checkpoint.
        - "all": Log all model checkpoints.
    """

    watch: WandbWatchConfig | None = WandbWatchConfig()
    """WandB model watch configuration. Used to log model architecture, gradients, and parameters."""

    offline: bool = False
    """Whether to run WandB in offline mode."""

    use_wandb_core: bool = True
    """Whether to use the new `wandb-core` backend for WandB.
    `wandb-core` is a new backend for WandB that is faster and more efficient than the old backend.
    """

    def offline_(self, value: bool = True):
        self.offline = value
        return self

    def core_(self, value: bool = True):
        self.use_wandb_core = value
        return self

    @override
    def create_logger(self, root_config):
        if not self.enabled:
            return None

        # If `wandb-core` is enabled, we should use the new backend.
        if self.use_wandb_core:
            try:
                import wandb  # type: ignore

                # The minimum version that supports the new backend is 0.17.5
                wandb_version = version.parse(importlib.metadata.version("wandb"))
                if wandb_version < version.parse("0.17.5"):
                    log.warning(
                        "The version of WandB installed does not support the `wandb-core` backend "
                        f"(expected version >= 0.17.5, found version {wandb.__version__}). "
                        "Please either upgrade to a newer version of WandB or disable the `use_wandb_core` option."
                    )
                else:
                    wandb.require("core")
                    log.critical("Using the `wandb-core` backend for WandB.")
            except ImportError:
                pass

        from lightning.pytorch.loggers.wandb import WandbLogger

        save_dir = root_config.directory._resolve_log_directory_for_logger(
            root_config.id,
            self,
        )
        return WandbLogger(
            save_dir=save_dir,
            project=self.project or _project_name(root_config),
            name=root_config.run_name,
            version=root_config.id,
            log_model=self.log_model,
            notes=(
                "\n".join(f"- {note}" for note in root_config.notes)
                if root_config.notes
                else None
            ),
            tags=root_config.tags,
            offline=self.offline,
        )

    @override
    def create_callbacks(self, root_config):
        yield FinishWandbOnTeardownCallback()

        if self.watch:
            yield from self.watch.create_callbacks(root_config)
