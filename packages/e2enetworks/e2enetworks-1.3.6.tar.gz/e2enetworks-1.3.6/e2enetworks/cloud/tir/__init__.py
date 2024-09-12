import urllib3

from e2enetworks.cloud.tir import version as tir_version

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
__version__ = tir_version.__version__

from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.apitoken import APITokens
from e2enetworks.cloud.tir.datasets import Datasets
from e2enetworks.cloud.tir.inference.endpoints import EndPoints
from e2enetworks.cloud.tir.images import Images
from e2enetworks.cloud.tir.models import Models
from e2enetworks.cloud.tir.notebook import Notebooks
from e2enetworks.cloud.tir.pipelines import PipelineClient
from e2enetworks.cloud.tir.projects import Projects
from e2enetworks.cloud.tir.skus import Plans
from e2enetworks.cloud.tir.teams import Teams
from e2enetworks.cloud.tir.api_client import ModelAPIClient
from e2enetworks.cloud.tir.finetuning.finetuner import FinetuningClient
from e2enetworks.cloud.tir.vector_db.vector_db import VectorDB
from e2enetworks.cloud.tir.distributed_jobs.distributed_job import DistributedJobClient

init = client.Default.init

__all__ = (
    "init",
    "PipelineClient"
)


def help():
    print("\t\tAIPlatform Help")
    print("\t\t=================")
    print("\t\tAvailable classes:")
    print("\t\t- init: Provides functionalities for initialization.")
    print("\t\t- Images: Provides functionalities to interact with images.")
    print("\t\t- Plans: Provides functionalities to interact with skus.")
    print("\t\t- Teams: Provides functionalities to interact with teams.")
    print("\t\t- Projects: Provides functionalities to interact with projects.")
    print("\t\t- Notebooks: Provides functionalities to interact with notebooks.")
    print("\t\t- Datasets: Provides functionalities to interact with datasets.")
    print("\t\t- EndPoints: Provides functionalities to interact with endpoints.")
    print("\t\t- Models: Provides functionalities to interact with models.")
    print("\t\t- PipelineClient: Provides functionalities to interact with Pipelines.")
    print("\t\t- APITokens: Provides functionalities to interact with API tokens.")
    print("\t\t- list_endpoint_plans: List Available Endpoint Plans")
    print("\t\t- VectorDB: Provides functionalities to interact with Vector Databases.")

    # Call help() method on each class
    client.Default.help()
    Images.help()
    Plans.help()
    Teams.help()
    Projects.help()
    Notebooks.help()
    Datasets.help()
    EndPoints.help()
    PipelineClient.help()
    Models.help()
    APITokens.help()
    ModelAPIClient.help()
    FinetuningClient.help()
    VectorDB.help()
    DistributedJobClient.help()


def list_endpoint_plans():
    return Plans().list_endpoint_plans()
