""" Module for managing datasets available in the AIMMO core Curation Dataset Zoo. """

import traceback
import zipfile
from pathlib import Path
from typing import Dict, Type, List, Optional, Any
import asyncio
import aiohttp
import aiofiles
from tqdm.asyncio import tqdm
import requests
from loguru import logger
from aimmocore import config as conf
from aimmocore.core import utils
from aimmocore.core.database import MongoDB


class ZooDataset:
    """Base class for datasets made available in the aimmo core Curation Dataset Zoo."""

    @property
    def name(self):
        """The name of the dataset."""
        raise NotImplementedError("subclasses must implement name")

    @property
    def description(self):
        """A description of the dataset."""
        raise NotImplementedError("subclasses must implement description")

    @property
    def count(self) -> int:
        """count of the dataset."""
        raise NotImplementedError("subclasses must implement count")

    @property
    def id(self):
        """the id of the dataset."""
        raise NotImplementedError("subclasses must implement id")

    async def download_and_prepare(self):
        """Downloads the dataset and prepares it for use."""
        raise NotImplementedError("subclasses must implement download_and_prepare")

    async def load(self):
        """Loads the dataset."""
        raise NotImplementedError("subclasses must implement load")

    def _get_dataset_loader(self):
        return DatasetLoader(self.count, self.name)


class DatasetLoader:
    def __init__(self, count: int, dataset_name: str):
        db = MongoDB()
        db.connect()
        self._db = db.get_engine()
        self._count = count
        self._dataset_name = dataset_name

    async def load(self) -> bool:
        """Loads the dataset into the database."""
        try:
            dataset_info = await self._load_json_data(self._dataset_name, "sample_dataset_info.json")
            datasets = await self._load_json_data(self._dataset_name, "sample_datasets.json")
            raw_files = await self._load_json_data(self._dataset_name, "sample_raw_files.json")

            await self._update_dataset_info(dataset_info)
            dataset_count = await self._update_datasets(datasets)
            raw_file_count = await self._update_raw_files(raw_files)

            return self._verify_load_success(dataset_count, raw_file_count)
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Failed to load {self._dataset_name} dataset: {str(e)}")
            return False

    async def _load_json_data(self, dataset_name: str, file_name: str) -> List[Dict[str, Any]]:
        file_path = Path(conf.SAMPLES_DIR) / dataset_name / file_name
        return utils.get_data_from_json(file_path)

    async def _update_dataset_info(self, dataset_info: List[Dict[str, Any]]) -> None:
        for info in dataset_info:
            await self._db.dataset_info.update_one({"dataset_id": info["dataset_id"]}, {"$set": info}, upsert=True)

    async def _update_datasets(self, datasets: List[Dict[str, Any]]) -> int:
        return await self._update_documents(
            self._db.datasets,
            datasets,
            lambda dataset: {"dataset_id": dataset["dataset_id"], "image_id": dataset["image_id"]},
        )

    async def _update_raw_files(self, raw_files: List[Dict[str, Any]]) -> int:
        return await self._update_documents(self._db.raw_files, raw_files, lambda file: {"id": file["id"]})

    async def _update_documents(self, collection, documents: List[Dict[str, Any]], id_func) -> int:
        count = 0
        for doc in documents:
            result = await collection.update_one(id_func(doc), {"$set": doc}, upsert=True)
            if result.upserted_id:
                count += 1
        return count

    def _verify_load_success(self, dataset_count: int, raw_file_count: int) -> bool:
        if dataset_count == self._count:
            logger.info(f"Loaded dataset with {dataset_count} curation datas.")
            return True
        else:
            logger.error(f"Failed. Expected {self._count} items, got {dataset_count} curation datas")
            return False


class AimmoAdDataset(ZooDataset):
    """The aimmo-ad dataset from the AIMMO core Curation Dataset Zoo."""

    _SAS_URL = "https://dataplatform.blob.core.windows.net/curation-sdk-samples/samples-aimmo-ad-dataset.zip?sv=2017-04-17&st=2024-09-02T04%3A47%3A43Z&se=2026-09-03T04%3A47%3A00Z&sr=b&sp=r&sig=Mqn8NPFCFRan7KhtHbngHgG5zc20NZ9cvEZyJAIPiD0%3D"
    _NAME = "aimmo-ad-dataset"
    _ID = "66d1d68946842c989cb5495a"
    _COUNT = 299

    @property
    def id(self):
        return self._ID

    @property
    def name(self):
        return self._NAME

    @property
    def description(self):
        return "AIMMO AD sample dataset for curation tasks"

    @property
    def count(self):
        return self._COUNT

    async def download_and_prepare(self):
        """Downloads the dataset and prepares it for use."""
        dataset_dir = Path(conf.AIMMOCORE_HOME)
        dataset_dir.mkdir(parents=True, exist_ok=True)
        zip_path = dataset_dir / "temp.zip"

        try:
            logger.info(f"Downloading {self.name} dataset...")
            async with aiohttp.ClientSession() as session:
                async with session.get(self._SAS_URL) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get("content-length", 0))

                    with tqdm(
                        total=total_size, unit="iB", unit_scale=True, desc=f"Downloading {self.name}"
                    ) as progress_bar:
                        async with aiofiles.open(zip_path, "wb") as f:
                            downloaded = 0
                            last_progress_time = asyncio.get_event_loop().time()
                            async for chunk in response.content.iter_chunked(8192):
                                if (
                                    asyncio.get_event_loop().time() - last_progress_time > 30
                                ):  # 30 seconds without progress
                                    raise asyncio.TimeoutError("Download stalled for too long")
                                size = len(chunk)
                                downloaded += size
                                await f.write(chunk)
                                progress_bar.update(size)
                                last_progress_time = asyncio.get_event_loop().time()

            logger.info(f"Extracting {self.name} dataset...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(dataset_dir)

            logger.info(f"{self.name} dataset has been successfully downloaded : {conf.AIMMOCORE_HOME}/{self.name}")

        except requests.RequestException as e:
            logger.error(f"Error downloading the dataset: {e}")
        except asyncio.TimeoutError as e:
            logger.error(f"Download timed out: {e}")
        except zipfile.BadZipFile:
            logger.error("Error: The downloaded file is not a valid ZIP file.")
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"An unexpected error occurred: {e}")
            logger.error(traceback.format_exc())
        finally:
            if zip_path.exists():
                zip_path.unlink()

        self._cleanup_dataset()

    async def load(self):
        dataset_loader = self._get_dataset_loader()
        await dataset_loader.load()

    def _cleanup_dataset(self):
        pass


DATASET_REGISTRY: Dict[str, Type[ZooDataset]] = {"aimmo-ad-dataset": AimmoAdDataset}


async def check_dataset_status(dataset_id: str):
    """Checks if the dataset is already loaded in the database."""
    db = MongoDB()
    db.connect()
    engine = db.get_engine()
    dataset = await engine.dataset_info.find_one({"dataset_id": dataset_id})
    return bool(dataset)


async def load_zoo_dataset(dataset_name: str = "aimmo-ad-dataset") -> Optional[bool]:
    """
    Loads the sample dataset corresponding to the specified dataset name.

    Args:
        dataset_name (str): The name of the dataset to load. Defaults to "aimmo-ad-dataset".

    Returns:
        Optional[bool]: True if the dataset was loaded successfully, None if it was already loaded or an error occurred.
    """
    if dataset_name not in DATASET_REGISTRY:
        logger.error(f"Unknown dataset name: {dataset_name}")
        return None

    dataset_dir = Path(conf.SAMPLES_DIR) / dataset_name
    downloaded = dataset_dir.exists()

    try:
        dataset_class = DATASET_REGISTRY[dataset_name]
        dataset = dataset_class()

        if await check_dataset_status(dataset.id):
            logger.info(f"Dataset '{dataset_name}' is already loaded.")
            return None

        if not downloaded:
            await dataset.download_and_prepare()
        await dataset.load()

        logger.info(f"Dataset '{dataset_name}' has been successfully loaded.")
        return True

    except Exception as e:  # pylint: disable=broad-except
        logger.error(f"Failed to load dataset '{dataset_name}': {str(e)}")
        return None


def list_zoo_datasets() -> List[Dict[str, str]]:
    """
    Returns a list of all available sample datasets.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing information about each dataset.
        Each dictionary includes the keys 'id', 'name', 'description', and 'status'.
    """
    datasets = []
    for _, dataset_class in DATASET_REGISTRY.items():
        dataset = dataset_class()
        dataset_dir = Path(conf.SAMPLES_DIR) / dataset.name
        status = "Downloaded" if dataset_dir.exists() else "Not Downloaded"

        datasets.append(
            {
                "name": dataset.name,
                "description": dataset.description,
                "count": dataset.count,
                "status": status,
            }
        )

    return datasets
