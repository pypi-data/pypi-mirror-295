from scrapeanything.utils.config import Config
from scrapeanything.database.repository import Repository
from scrapeanything.utils.requests import Methods
from scrapeanything.utils.requests import ResponseTypes
from scrapeanything.utils.constants import *
import requests

class Service:

    def __init__(self, config: Config=None, repository: Repository=None) -> None:
        if repository is not None:
            self.repository = repository
    
        if config is not None:
            self.config = config

    def wget(self, url: str, parameters: dict=None, method: Methods=Methods.GET, response_type: ResponseTypes=ResponseTypes.JSON) -> any:
        if method == Methods.GET:
            response = self.config.get(url=url, data=parameters)
        elif method == Methods.POST:
            response = self.config.post(url=url, data=parameters)
        else:
            raise Exception(f'{method} method is not supported')

        if response_type == ResponseTypes.JSON:
            return response.json()
        elif response_type == ResponseTypes.TEXT:
            return response.text
        else:
            raise Exception(f'{response_type} response type is not supported')