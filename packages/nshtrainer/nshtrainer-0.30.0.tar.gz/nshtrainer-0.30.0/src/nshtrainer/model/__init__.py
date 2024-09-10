from typing_extensions import TypeAlias

from .base import Base as Base
from .base import LightningModuleBase as LightningModuleBase
from .config import BaseConfig as BaseConfig
from .config import BaseProfilerConfig as BaseProfilerConfig
from .config import BestCheckpointCallbackConfig as BestCheckpointCallbackConfig
from .config import CheckpointLoadingConfig as CheckpointLoadingConfig
from .config import CheckpointSavingConfig as CheckpointSavingConfig
from .config import DirectoryConfig as DirectoryConfig
from .config import EarlyStoppingConfig as EarlyStoppingConfig
from .config import GradientClippingConfig as GradientClippingConfig
from .config import HuggingFaceHubConfig as HuggingFaceHubConfig
from .config import LastCheckpointCallbackConfig as LastCheckpointCallbackConfig
from .config import LoggingConfig as LoggingConfig
from .config import MetricConfig as MetricConfig
from .config import (
    OnExceptionCheckpointCallbackConfig as OnExceptionCheckpointCallbackConfig,
)
from .config import OptimizationConfig as OptimizationConfig
from .config import PrimaryMetricConfig as PrimaryMetricConfig
from .config import ReproducibilityConfig as ReproducibilityConfig
from .config import SanityCheckingConfig as SanityCheckingConfig
from .config import TrainerConfig as TrainerConfig

ConfigList: TypeAlias = list[tuple[BaseConfig, type[LightningModuleBase]]]
