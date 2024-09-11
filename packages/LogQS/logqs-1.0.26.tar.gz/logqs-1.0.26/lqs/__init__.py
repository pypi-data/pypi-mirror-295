from importlib.metadata import version

from lqs.client import RESTClient

__version__ = version("LogQS")

LogQS = RESTClient
