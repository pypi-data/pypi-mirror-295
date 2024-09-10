import asyncio
from functools import wraps
import os
import subprocess
import time
import platform
from contextlib import asynccontextmanager
import psutil
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from IPython import get_ipython
from aimmocore import config as acc


class MongoDB:
    """Motor Client"""

    def __init__(self, port: int = acc.get_database_port()):
        self.manage_db = ManageDatabase(port)
        self.client = None
        self.engine = None

    def connect(self, port: int = acc.get_database_port()):
        self.client = AsyncIOMotorClient(f"mongodb://127.0.0.1:{port}")
        self.engine = self.client["aimmocore"]
        asyncio.get_event_loop().run_until_complete(self.init_document())

    def get_engine(self):
        return self.engine

    async def init_document(self):
        """Initialize the MongoDB collections and indexes"""
        await self.engine.dataset_info.create_index([("dataset_id", 1), ("dataset_name", 1)])
        await self.engine.datasets.create_index([("dataset_id", 1), ("image_id", 1)])
        await self.engine.raw_files.create_index([("id", 1)])

    async def ping(self):
        try:
            if self.client is None:
                return False
            result = await self.client["admin"].command("ping")
            return result["ok"] == 1

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None
            self.engine = None


async def get_mongodb_instance():
    mongo_db = MongoDB()
    mongo_db.connect()
    return mongo_db


@asynccontextmanager
async def db_connection():
    """Get the MongoDB engine instance"""
    mongo_db = await get_mongodb_instance()
    try:
        yield mongo_db.engine
    finally:
        mongo_db.close()


def with_db_connection(func):
    """Decorator to provide a MongoDB engine instance to a function"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with db_connection() as db:
            return await func(db, *args, **kwargs)

    return wrapper


class ManageDatabase:
    """Manage the MongoDB database"""

    def __init__(self, port: int, bootup_timeout: int = 10):
        self.port = port
        self.mongod_process = None
        self.bootup_timeout = bootup_timeout
        self.platform = platform.system()
        self._ensure_mongodb()

    def _ensure_mongodb(self):
        self.mongo_dir = os.path.join(os.path.expanduser("~"), ".aimmocore", "mongodb_installation", "mongodb")
        self.mongod_file_path = os.path.join(self.mongo_dir, "bin", self._get_mongod_file())

        # Check if mongod exists, if not, install it
        if not os.path.exists(self.mongod_file_path):
            logger.debug("aimmocore-db not found. Installing MongoDB as aimmocore-db...")
            subprocess.call(["python", "-m", "aimmocore_db.install_mongodb"])

        # Check if mongod is running, if not, start it
        if not self._is_mongod_running():
            logger.debug("aimmocore-db not running. Starting aimmocore-db...")
            self._start_mongodb()

    def _get_mongod_file(self):
        if self.platform == "Windows":
            return "mongod.exe"
        else:
            return "mongod"

    def _is_mongod_running(self):
        """Check if mongod is running on the specified port."""
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            if "mongod" in proc.info["name"]:
                cmdline_str = " ".join(proc.info["cmdline"])
                if f"--port {self.port}" in cmdline_str:
                    return True
        return False

    def _wait_for_starting_db(self):
        """Wait until MongoDB is running on the specified port or timeout."""
        start_time = time.time()
        while (time.time() - start_time) < self.bootup_timeout:
            if self._is_mongod_running():
                return True
            logger.debug("aimmocore-db is starting...")
            time.sleep(2)  # Check every 5 seconds
        return False

    def _start_mongodb(self):
        """Start MongoDB server."""
        data_dir = os.path.join(os.path.dirname(self.mongo_dir), "data")
        log_file = os.path.join(os.path.dirname(self.mongo_dir), "mongod.log")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        command = [
            self.mongod_file_path,
            "--dbpath",
            data_dir,
            "--logpath",
            log_file,
            "--bind_ip",
            "0.0.0.0",
            "--port",
            str(self.port),
        ]

        in_container = os.environ.get("SDK_IN_CONTAINER", "false") == "true"
        if self.platform != "Windows" and not in_container:
            logger.debug("SDK not in container, ")
            command.append("--fork")

        self.mongod_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )

        """check :: communicate() is not working under container
        logger.debug(f"Starting MongoDB with command: {command}")
        _, stderr = self.mongod_process.communicate()
        logger.debug("After communicate")

        if stderr:
            logger.error(stderr.decode())
            return
        """

        if self._wait_for_starting_db():
            logger.debug(
                f"MongoDB started on port {self.port} with data directory: {data_dir} and log file: {log_file}"
            )
            ip = get_ipython()
            if ip is not None:
                logger.debug("SDK running under IPython. Registering post_execute event.")
                ip.events.register("post_execute", self._check_kernel_status)
        else:
            raise RuntimeError("aimmocore-db failed to start.")

    def _check_kernel_status(self):
        """Check if the kernel is shutting down and stop MongoDB if it is."""
        if self.mongod_process.poll() is None:
            logger.debug("mongod_process.poll() is none")
            # self._stop_mongodb()

    def _stop_mongodb(self):
        """Stop MongoDB server."""
        if self.mongod_process is not None:
            # Using mongo shell to shut down the server
            shutdown_command = f"{self.mongod_file_path} --eval \"db.getSiblingDB('admin').shutdownServer()\""

            try:
                subprocess.call(shutdown_command, shell=True)
                logger.debug("MongoDB has been stopped.")
            except Exception as e:  # pylint: disable=broad-except
                logger.error(f"Error stopping MongoDB: {e}")
