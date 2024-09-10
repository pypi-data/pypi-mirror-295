""" Image processing functions for the AIMMO SDK. """

import traceback
from pathlib import Path
import asyncio
import json
from typing import List, Dict, Any, Optional
import aiohttp
from loguru import logger
from tqdm import tqdm
from motor.motor_asyncio import AsyncIOMotorCollection
from aimmocore import config as conf


async def download_sas_url(session: aiohttp.ClientSession, sas_url: str):
    """
    Download the content from a given SAS URL.

    Args:
        session (aiohttp.ClientSession): The aiohttp session used to make the HTTP request.
        sas_url (str): The SAS URL from which to download the file content.

    Returns:
        str: The content of the file as a string if successful, otherwise None.

    Raises:
        None: This function handles all exceptions internally and logs errors.
    """
    try:
        async with session.get(sas_url) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:  # pylint: disable=broad-except
        logger.error(f"Error downloading file {sas_url}: {e}")
        print(traceback.format_exc())
        return None


async def parse_file_content_to_list(file_content: str) -> List[Dict[str, Any]]:
    """파일 내용을 라인별로 읽어 list[dict]로 변환"""
    lines = file_content.strip().splitlines()  # 각 라인을 리스트로 분리
    list_of_dicts = []

    for line in lines:
        try:
            dict_obj = json.loads(line)
            list_of_dicts.append(dict_obj)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON on line: {line}, error: {e}")

    return list_of_dicts


async def download_and_save_image(session: aiohttp.ClientSession, image_url: str, save_path: str) -> bool:
    """
    Downloads an image from the provided URL and saves it to the specified path.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        image_url (str): The URL of the image to download.
        save_path (str): The path and filename where the image will be saved.

    Returns:
        bool: True if the image was successfully downloaded and saved, False otherwise.
    """
    try:
        async with session.get(image_url) as response:
            response.raise_for_status()
            image_data = await response.read()

            save_dir = Path(save_path).parent
            save_dir.mkdir(parents=True, exist_ok=True)

            with open(save_path, "wb") as image_file:
                image_file.write(image_data)

            # I think this line is unnecessary, but I'm not sure.
            # logger.info(f"Image downloaded and saved to {save_path}")
            return True

    except Exception as e:  # pylint: disable=broad-except
        logger.error(f"Error downloading or saving image {image_url}: {e}")

        return False


async def get_thumbnail_url(session: aiohttp.ClientSession, dataset_id: str, headers: dict) -> Optional[str]:
    """Get the thumbnail URL from the server for the given dataset ID.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for the request.
        dataset_id (str): The dataset ID to fetch the thumbnail URL for.
        headers (dict): The headers to use for the request.

    Returns:
        str: The thumbnail URL, or None if the URL is not available.
    """
    try:
        async with session.get(f"{conf.CURATION_THUMB_ENDPOINT}?dataset_id={dataset_id}", headers=headers) as response:
            if response.status == 200:
                thumb_info = await response.json()
                return thumb_info.get("thumb_url")
    except Exception as e:  # pylint: disable=broad-except
        logger.error(f"Error fetching thumbnail URL for dataset {dataset_id}: {e}")
    return None


async def process_thumbnail_generation(
    session: aiohttp.ClientSession,
    dataset_id: str,
    headers: Dict[str, str],
    image_ids_in_progress: List[str],
    collection: AsyncIOMotorCollection,
):
    """
    Process the generation of thumbnails for the given image IDs.

    This function fetches the thumbnail URL for a dataset, downloads the associated file,
    parses the content to extract thumbnail URLs for each image ID, and then saves the thumbnails
    and updates the database accordingly.

    Args:
        session (aiohttp.ClientSession): The aiohttp session used for making HTTP requests.
        dataset_id (str): The ID of the dataset for which thumbnails are being generated.
        headers (Dict[str, str]): The HTTP headers to include in the request for the thumbnail URL.
        image_ids_in_progress (List[str]): A list of image IDs that are currently being processed.
        collection (AsyncIOMotorCollection): The MongoDB collection to update with the thumbnail status.

    Returns:
        bool: True if the thumbnails were successfully generated and saved, False otherwise.
    """
    thumb_url = await get_thumbnail_url(session, dataset_id, headers)
    if not thumb_url:
        return False

    file_content = await download_sas_url(session, thumb_url)
    if not file_content:
        return False

    thumbs_dict = await parse_thumbnails(file_content)
    await save_thumbnails(session, thumbs_dict, image_ids_in_progress, collection)

    return True


async def parse_thumbnails(file_content: str) -> Dict[str, str]:
    """
    Parse the file content and return a dictionary of thumbnail URLs.

    This function reads the file content, which is expected to contain a list of JSON objects,
    each representing an image and its associated thumbnail URL. The function returns a dictionary
    mapping image IDs to their corresponding thumbnail URLs.

    Args:
        file_content (str): The content of the file to be parsed. It is expected to be a JSON-formatted string
                            where each line represents an image with its thumbnail URL.

    Returns:
        Dict[str, str]: A dictionary where the keys are image IDs (str) and the values are the corresponding
                        thumbnail URLs (str) or any other associated data.
    """
    list_of_dicts = await parse_file_content_to_list(file_content)
    return {d["id"]: d["thumbnail_url"] for d in list_of_dicts}


async def save_thumbnails(
    session: aiohttp.ClientSession,
    thumbs_dict: Dict[str, str],
    image_ids_in_progress: List[str],
    collection: AsyncIOMotorCollection,
) -> None:
    """
    Save thumbnails to the local storage and update the database.

    This function iterates over a list of image IDs, downloads their corresponding thumbnails
    using the provided session, saves them to the specified local directory, and updates the
    database to mark the thumbnails as successfully processed.

    Args:
        session (aiohttp.ClientSession): The aiohttp session used for downloading the thumbnails.
        thumbs_dict (Dict[str, str]): A dictionary mapping image IDs to their respective thumbnail URLs.
        image_ids_in_progress (List[str]): A list of image IDs that are being processed.
        collection (AsyncIOMotorCollection): The MongoDB collection where the thumbnail status will be updated.

    Returns:
        None
    """
    for image_id in tqdm(image_ids_in_progress, desc="Downloading thumbnails"):
        if image_id in thumbs_dict:
            save_path = f"{conf.THUMBNAIL_DIR}/{image_id}.jpg"
            downloaded = await download_and_save_image(session, thumbs_dict[image_id], save_path)
            if downloaded:
                await collection.update_one({"id": image_id}, {"$set": {"thumbnail": "Y"}})


async def generate_thumbnail(headers: str, db, dataset_id: str):
    """
    Generate thumbnails for images in the database and update their status.

    Args:
        headers (str): HTTP headers to use for requests to the thumbnail generation endpoint.
        db (Any): The database connection object, typically an instance of AsyncIOMotorDatabase.
        dataset_id (str): The dataset ID for which thumbnails are being generated.

    Returns:
        None
    """
    logger.info("Processing thumbnails for images from server.")
    async with aiohttp.ClientSession() as session:
        collection = db.raw_files
        documents = await collection.find({"thumbnail": {"$nin": ["Y", "P"]}}, {"_id": 0}).to_list(None)
        image_ids_in_progress = [document.get("id") for document in documents]
        if image_ids_in_progress:
            await collection.update_many({"id": {"$in": image_ids_in_progress}}, {"$set": {"thumbnail": "P"}})
        else:
            logger.info("No images to process for thumbnail generation.")
            return

        thumb_generation = False
        max_retries = 100

        for _ in range(max_retries):
            thumb_generation = await process_thumbnail_generation(
                session, dataset_id, headers, image_ids_in_progress, collection
            )

            if thumb_generation:
                break

            await asyncio.sleep(3)

        if not thumb_generation:
            logger.warning(f"Thumbnail generation failed after {max_retries} attempts.")
