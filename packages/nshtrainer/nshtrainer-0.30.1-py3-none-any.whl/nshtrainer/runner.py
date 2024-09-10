import copy
import functools
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Generic

from nshrunner import RunInfo, Snapshot
from nshrunner import Runner as _Runner
from nshrunner._submit import screen
from typing_extensions import TypeVar, TypeVarTuple, Unpack, override

from .model.config import BaseConfig

TConfig = TypeVar("TConfig", bound=BaseConfig, infer_variance=True)
TArguments = TypeVarTuple("TArguments", default=Unpack[tuple[()]])
TReturn = TypeVar("TReturn", infer_variance=True)


class Runner(
    _Runner[TReturn, TConfig, Unpack[TArguments]],
    Generic[TReturn, TConfig, Unpack[TArguments]],
):
    @override
    @classmethod
    def default_validate_fn(cls, config: TConfig, *args: Unpack[TArguments]) -> None:
        super().default_validate_fn(config, *args)

    @override
    @classmethod
    def default_info_fn(cls, config: TConfig, *args: Unpack[TArguments]) -> RunInfo:
        run_info = super().default_info_fn(config, *args)
        return {
            **run_info,
            "id": config.id,
            "base_dir": config.directory.project_root,
        }

    def _fast_dev_run_transform(
        self,
        config: TConfig,
        *args: Unpack[TArguments],
        n_batches: int,
    ):
        config = copy.deepcopy(config)
        config.trainer.fast_dev_run = n_batches
        return (config, *args)

    def fast_dev_run(
        self,
        runs: Iterable[tuple[TConfig, Unpack[TArguments]]],
        n_batches: int = 1,
        *,
        env: Mapping[str, str] | None = None,
        transforms: list[
            Callable[[TConfig, Unpack[TArguments]], tuple[TConfig, Unpack[TArguments]]]
        ]
        | None = None,
    ):
        transforms = transforms or []
        transforms.append(
            functools.partial(self._fast_dev_run_transform, n_batches=n_batches)
        )
        return self.local(
            runs,
            env=env,
            transforms=transforms,
        )

    def fast_dev_run_generator(
        self,
        runs: Iterable[tuple[TConfig, Unpack[TArguments]]],
        n_batches: int = 1,
        *,
        env: Mapping[str, str] | None = None,
        transforms: list[
            Callable[[TConfig, Unpack[TArguments]], tuple[TConfig, Unpack[TArguments]]]
        ]
        | None = None,
    ):
        transforms = transforms or []
        transforms.append(
            functools.partial(self._fast_dev_run_transform, n_batches=n_batches)
        )
        return self.local_generator(
            runs,
            env=env,
            transforms=transforms,
        )

    def fast_dev_run_session(
        self,
        runs: Iterable[tuple[TConfig, Unpack[TArguments]]],
        options: screen.ScreenJobKwargs = {},
        n_batches: int = 1,
        *,
        snapshot: Snapshot,
        setup_commands: Sequence[str] | None = None,
        env: Mapping[str, str] | None = None,
        transforms: list[
            Callable[[TConfig, Unpack[TArguments]], tuple[TConfig, Unpack[TArguments]]]
        ]
        | None = None,
        activate_venv: bool = True,
        print_command: bool = True,
    ):
        transforms = transforms or []
        transforms.append(
            functools.partial(self._fast_dev_run_transform, n_batches=n_batches)
        )
        return self.session(
            runs,
            options,
            snapshot=snapshot,
            setup_commands=setup_commands,
            env=env,
            transforms=transforms,
            activate_venv=activate_venv,
            print_command=print_command,
        )
