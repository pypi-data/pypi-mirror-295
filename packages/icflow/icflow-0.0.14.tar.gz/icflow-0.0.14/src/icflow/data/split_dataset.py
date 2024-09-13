"""
This module has functionaly for handling datasets that feed into
models.
"""

from pathlib import Path
import logging
import typing

from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler

from icflow.utils.runtime import RuntimeContext

from .dataset import BaseDataset

logger = logging.getLogger(__name__)


class SplitDataset(BaseDataset):
    """
    A dataset supporting splits into parts, e.g 'test', 'train', 'val'
    """

    def __init__(
        self,
        path: Path,
        batch_size: int,
        name: str = "",
        archive_name: str = "",
        hostname: str = "",
    ):
        super().__init__(path, name, archive_name, hostname)

        self.batch_size = batch_size
        self.splits: dict = {}
        self.dataloaders: dict = {}
        self.samplers: dict = {}
        self.runtime_ctx: RuntimeContext | None = None
        self.transform: typing.Any = None
        self.split_config = {
            "train": {"path": "train", "shuffle": True, "sample": True},
            "val": {"path": "val", "shuffle": True, "sample": True},
            "test": {"path": "test", "shuffle": False, "sample": False},
        }

    def load(self):
        """
        Load the dataset from the supplied path
        """

        if self.splits:
            return

        logger.info("Loading dataset from %s", self.path)
        if not self.path.exists():
            raise RuntimeError(f"Provided dataset path {self.path} not found")

        for label, config in self.split_config.items():
            self.splits[label] = self.load_dataset(config["path"])

        self.setup_dataloaders()

        logger.info(
            "Finished loading dataset with %d dataloaders", len(self.splits.keys())
        )

    def load_dataset(self, stage: str) -> Dataset:
        """
        Stub method to load a PyTorch dataset
        """
        raise NotImplementedError()

    def get_data(self, split: str) -> Dataset:
        return self.splits[split]

    def get_dataloader(self, split: str) -> DataLoader:
        return self.dataloaders[split]

    def get_num_batches(self, split: str) -> int:
        return len(self.dataloaders[split])

    def get_num_classes(self) -> int:
        if self.splits:
            return list(self.splits.values())[0].num_classes
        return 0

    def set_sampler_epoch(self, epoch: int):
        for sampler in self.samplers.values():
            sampler.set_epoch(epoch)

    def on_epoch_start(self, epoch_idx: int):
        self.set_sampler_epoch(epoch_idx)

    def setup_dataloaders(self):
        """
        Given the datasets generate suitable dataloaders,
        and if running in a multi-gpu context suitable samplers.
        """

        logger.info("Setting up dataloaders")
        if self.runtime_ctx and self.runtime_ctx.is_multigpu:
            logger.info("Running in multigpu mode - setting up Samplers")
            for label, config in self.split_config:

                if not config["sample"]:
                    continue

                self.samplers[label] = DistributedSampler(
                    self.splits[label],
                    num_replicas=self.runtime_ctx.world_size,
                    rank=self.runtime_ctx.global_rank,
                )

        num_workers = 0
        if self.runtime_ctx:
            num_workers = self.runtime_ctx.num_workers
        for key, value in self.splits.items():
            self.dataloaders[key] = DataLoader(
                dataset=value,
                batch_size=self.batch_size,
                shuffle=self.split_config[key]["shuffle"],
                sampler=self.samplers[key] if key in self.samplers else None,
                num_workers=num_workers,
            )
