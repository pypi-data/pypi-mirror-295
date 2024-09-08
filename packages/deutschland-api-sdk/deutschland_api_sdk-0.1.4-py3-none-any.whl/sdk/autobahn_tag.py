"""
AutobahnTag automatically generated by SDKgen please do not edit this file manually
https://sdkgen.app
"""

import requests
import sdkgen
from requests import RequestException
from typing import List

from .autobahn_charging_station_tag import AutobahnChargingStationTag
from .autobahn_closure_tag import AutobahnClosureTag
from .autobahn_collection import AutobahnCollection
from .autobahn_parking_lorry_tag import AutobahnParkingLorryTag
from .autobahn_warning_tag import AutobahnWarningTag
from .response_exception import ResponseException

class AutobahnTag(sdkgen.TagAbstract):
    def __init__(self, http_client: requests.Session, parser: sdkgen.Parser):
        super().__init__(http_client, parser)

    def warning(self) -> AutobahnWarningTag:
        return AutobahnWarningTag(
            self.http_client,
            self.parser
        )

    def parking_lorry(self) -> AutobahnParkingLorryTag:
        return AutobahnParkingLorryTag(
            self.http_client,
            self.parser
        )

    def closure(self) -> AutobahnClosureTag:
        return AutobahnClosureTag(
            self.http_client,
            self.parser
        )

    def charging_station(self) -> AutobahnChargingStationTag:
        return AutobahnChargingStationTag(
            self.http_client,
            self.parser
        )


    def get_all(self) -> AutobahnCollection:
        """
        Returns all available autobahns
        """
        try:
            path_params = {}

            query_params = {}

            query_struct_names = []

            url = self.parser.url("/autobahn", path_params)

            headers = {}

            response = self.http_client.get(url, headers=headers, params=self.parser.query(query_params, query_struct_names))

            if response.status_code >= 200 and response.status_code < 300:
                return AutobahnCollection.model_validate_json(json_data=response.content)

            if response.status_code == 400:
                raise ResponseException(response.content)
            if response.status_code == 404:
                raise ResponseException(response.content)
            if response.status_code == 500:
                raise ResponseException(response.content)

            raise sdkgen.UnknownStatusCodeException("The server returned an unknown status code")
        except RequestException as e:
            raise sdkgen.ClientException("An unknown error occurred: " + str(e))


