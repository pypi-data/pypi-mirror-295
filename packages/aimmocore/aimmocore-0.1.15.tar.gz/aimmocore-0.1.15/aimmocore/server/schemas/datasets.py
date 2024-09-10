""" Dataset schemas """

from typing import List
from enum import Enum
from pydantic import Field, model_validator
from .base import CamelModel


class ProcessStatus(Enum):
    """Curation task Status"""

    PREPARING = "Preparing"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    ERROR = "Error"


class Dataset(CamelModel):
    """Default dataset schema"""

    dataset_id: str = Field(alias="datasetId")
    dataset_name: str = Field(alias="datasetName")
    status: str = Field(alias="status")
    applied_metas: List[str] = Field(alias="appliedMetas")
    embedding_model: str = Field(alias="embeddingModel")
    file_count: int = Field(alias="fileCount")
    dataset_source: str = Field("blob://", alias="datasetSource")
    created_at: int = Field(alias="createdAt")


class Thumbnail(CamelModel):
    """Thumbnail schema"""

    dataset_id: str = Field(alias="datasetId")
    file_id: str = Field(alias="fileId")
    thumbnail_url: str = Field(alias="thumbnailUrl")
    image_url: str = Field(alias="imageUrl")
    created_at: int = Field(alias="createdAt")


class ThumbnailPageList(CamelModel):
    """Thumbnail page list schema"""

    items: List[Thumbnail]
    page: int = Field(alias="page")
    per_page: int = Field(alias="perPage")
    total: int = Field(alias="total")


class DatasetList(CamelModel):
    """Dataset list schema"""

    items: List[Dataset]


class DatasetFile(CamelModel):
    """Dataset file schema"""

    dataset_id: str = Field(alias="datasetId")
    file_id: str = Field(alias="fileId")
    file_name: str = Field(alias="fileName")
    file_path: str = Field("/", alias="filePath")
    file_size: int = Field(alias="fileSize")
    file_type: str = Field("Image", title="File Type", alias="fileType")
    thumbnail_url: str = Field(alias="thumbnailUrl")
    image_url: str = Field(alias="imageUrl")
    metas: List = Field(alias="metas")
    embeddings: List[float] = Field(alias="embeddings")
    curated_mask: int = Field(alias="curatedMask")
    anomaly_score: float = Field(alias="anomalyScore")
    created_at: int = Field(alias="createdAt")

    @model_validator(mode="before")
    def replace_values(cls, values):
        """change wrong values to correct one"""
        values["metas"] = ["sunrise/sunset" if x in ["sunset", "sunrise"] else x for x in values["metas"]]
        return values


class DatasetFileList(CamelModel):
    """Dataset file list schema"""

    items: List[DatasetFile]


class DatasetFilePageList(CamelModel):
    """Dataset file page list schema"""

    items: List[DatasetFile]
    page: int = Field(alias="page")
    per_page: int = Field(alias="perPage")
    total: int = Field(alias="total")


class Embeddings(CamelModel):
    """Embeddings schema"""

    file_id: str = Field(alias="fileId")
    thumbnail_url: str = Field(alias="thumbnailUrl")
    image_url: str = Field(alias="imageUrl")
    embeddings: List[float] = Field(alias="embeddings")
    curated_mask: int = Field(alias="curatedMask")
    anomaly_score: float = Field(alias="anomalyScore")


class EmbeddingsList(CamelModel):
    """Embeddings list schema"""

    items: List[Embeddings]


class Cluster(CamelModel):
    """Dataset cluster schema"""

    size: List[int]
