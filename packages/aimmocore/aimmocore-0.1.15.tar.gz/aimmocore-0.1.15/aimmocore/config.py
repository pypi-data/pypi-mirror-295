"""Configuration file for AIMMOCORE"""

import os

AIMMOCORE_HOME = os.path.join(os.path.expanduser("~"), ".aimmocore")
AIMMOCORE_WORKDIR = f"{AIMMOCORE_HOME}/workdir"
CURATION_ENDPOINT = "https://aimmo-core-curation.koreacentral.cloudapp.azure.com/api/curation"
LOCAL_STATUS_CURATION_ENDPOINT = "http://localhost:7071/api/curation"
LOCAL_UPLOAD_CURATION_ENDPOINT = "http://localhost:7072/api/curation"
CURATION_UPLOAD_ENDPOINT = f"{CURATION_ENDPOINT}/upload"
CURATION_STATUS_ENDPOINT = f"{CURATION_ENDPOINT}/status"
CURATION_AUTH_ENDPOINT = f"{CURATION_ENDPOINT}/auth"
CURATION_THUMB_ENDPOINT = f"{CURATION_ENDPOINT}/thumbnails"
THUMBNAIL_DIR = f"{AIMMOCORE_HOME}/thumbnails"
SAMPLES_DIR = f"{AIMMOCORE_HOME}/samples"
DEFAULT_CURATION_MODEL_ID = "va-torch-meta-emd:3"
REQUEST_TIMEOUT = 10
CURATION_MINIMUM_SIZE = 30
SAMPLING_CLUSTER_RANGE = 5
SUPPORT_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp"]
DEFAULT_LOCAL_DB_PORT = 27817
web_viewer_port = 10321


def init_directory(path):
    """Ensure that the directory exists."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def get_database_port():
    """Get the default local database port."""
    return DEFAULT_LOCAL_DB_PORT


init_directory(AIMMOCORE_WORKDIR)
init_directory(THUMBNAIL_DIR)
init_directory(SAMPLES_DIR)
