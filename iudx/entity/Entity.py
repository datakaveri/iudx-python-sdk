"""Module doc string. Leave empty for now.

Entity.py
"""
from typing import TypeVar, Generic, Any, List, Dict

from iudx.cat.Catalogue import Catalogue
from iudx.cat.CatalogueQuery import CatalogueQuery

from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery
from iudx.rs.ResourceResult import ResourceResult

import pandas as pd
from tqdm import tqdm
from multiprocessing import Process, Pool

Entity = TypeVar('T')
str_or_float = TypeVar('str_or_float', str, float)


class Entity():
    """Abstract class for Entity. Helps to create a modular interface
       for each inidividual Entity.
    """

    def __init__(self: Entity, entity_id: str=None):
        """Entity base class constructor for getting the resources from
                catalogue server.

        Args:
            entity_id (String): Id of the entity to be queried.
        """
        self.catalogue: Catalogue = Catalogue(
            cat_url="https://api.catalogue.iudx.org.in/iudx/cat/v1",
            headers={"content-type": "application/json"}
        )
        self.rs: ResourceServer = None
        self.resources: List[str] = []
        self.entity_id = entity_id

        self._iudx_entity_type: str = None
        self._voc_url: str = None
        self._cat_doc: Dict = None
        self._data_descriptor: Dict = None
        self._geo_properties: List[Dict] = None
        self._time_properties: List[Dict] = None
        self._quantitative_properties: List[Dict] = None
        self._properties: List[Dict] = None

        # Query the Catalogue module and fetch the item based on entity_id
        # and set the data descriptors
        documents_result = self.catalogue.get_item(self.entity_id)
        self._data_descriptor = documents_result.documents[0]["dataDescriptor"]

        # Parse the data schema from the data descriptor
        for key in self._data_descriptor.keys():
            pass

        # Fetch all Resources for the entity from Catalogue.
        cat_query = CatalogueQuery()
        param1 = {"key": "resourceGroup", "value": [self.entity_id]}
        param2 = {"key": "type", "value": ["iudx:Resource"]}

        query = cat_query.property_search(
                    key=param1["key"],
                    value=param1["value"]
                ).property_search(
                    key=param2["key"],
                    value=param2["value"]
                )

        # update resources list with the resources retrieved
        # from Catalogue query.
        cat_result = self.catalogue.search_entity(query)

        for res in cat_result.documents:
            self.resources.append(res["id"])

        self.rs: ResourceServer = ResourceServer(
            rs_url="https://rs.iudx.org.in/ngsi-ld/v1",
            headers={"content-type": "application/json"}
        )
        return

    def latest(self) -> pd.DataFrame:
        """Method to fetch resources for latest data
            and generate a dataframe.

        Returns:
            resources_df (pd.DataFrame): Pandas DataFrame with latest data.
        """
        resources_df = pd.DataFrame()
        for resource in self.resources:
            resource_query = ResourceQuery()
            query = resource_query.add_entity(resource)

            rs_result: ResourceResult = self.rs.get_latest(query)

            if rs_result.type == 200:
                resource_df = pd.DataFrame(rs_result.results)
                resources_df.append(resource_df)
        return resources_df

    def during_search(self, start_time: str=None,
                      end_time: str=None) -> pd.DataFrame:
        """Method to fetch resources for temporal based search
            and generate a dataframe.

        Args:
            start_time (String): The starting timestamp for the query.
            end_time (String): The ending timestamp for the query.

        Returns:
            resources_df (pd.DataFrame): Pandas DataFrame with temporal data.
        """
        resources_df = pd.DataFrame()

        queries = []
        for resource in tqdm(self.resources):
            resource_query = ResourceQuery()
            resource_query.add_entity(resource)

            query = resource_query.during_search(
                start_time=start_time,
                end_time=end_time
            )
            queries.append(query)
        rs_results: List[ResourceResult] = self.rs.get_data(queries)

        for rs_result in tqdm(rs_results):
            try:
                if rs_result.type == 200:
                    resource_df = pd.DataFrame(rs_result.results)

                    if len(resources_df) == 0:
                        resources_df = resource_df
                    else:
                        resources_df = pd.concat([resources_df, resource_df])
            except Exception as e:
                print(f"No Resource Data: {e}")
        return resources_df

    def property_search(self, key: str=None, value: str_or_float=None, 
                        operation: str=None) -> pd.DataFrame:
        """Method to fetch resources for temporal based search
            and generate a dataframe.

        Args:
            key (String): Property key to query.
            value (str/float): Values for the comparision with the key.
            operation (String): Operation to be performed
                between key and value.

        Returns:
            resources_df (pd.DataFrame): Pandas DataFrame with property data.
        """
        resources_df = pd.DataFrame()

        queries = []
        for resource in tqdm(self.resources):
            resource_query = ResourceQuery()
            resource_query.add_entity(resource)

            # TODO: temporal(during) query is required for property search.
            query = resource_query.property_search(
                key=key,
                value=value,
                operation=operation
            )
            queries.append(query)
        rs_results: List[ResourceResult] = self.rs.get_data(queries)

        for rs_result in tqdm(rs_results):
            try:
                if rs_result.type == 200:
                    resource_df = pd.DataFrame(rs_result.results)

                    if len(resources_df) == 0:
                        resources_df = resource_df
                    else:
                        resources_df = pd.concat([resources_df, resource_df])
            except Exception as e:
                print(f"No Resource Data: {e}")
        return resources_df

    def geo_search(self, geoproperty: str=None, geometry: str=None,
                   georel: str=None, _max_distance: int=None,
                   coordinates: List[Any]=None) -> pd.DataFrame:
        """Method to fetch resources for geo based search
            and generate a dataframe.

        Args:
            geoproperty (String): Which geoproperty to query.
            geometry (String): GeoJson geometries.
            georel (String): Geo-relationship.
            _max_distance (Integer): Radius from the center in meters.
            coordinates (List[Any]): The Coordinates of the geometry.

        Returns:
            resources_df (pd.DataFrame): Pandas DataFrame with geo data.
        """
        resources_df = pd.DataFrame()

        queries = []
        for resource in tqdm(self.resources):
            resource_query = ResourceQuery()
            resource_query.add_entity(resource)

            # TODO: temporal(during) query is required for geo search.
            query = resource_query.geo_search(
                geoproperty=geoproperty,
                geometry=geometry,
                georel=georel,
                max_distance=_max_distance,
                coordinates=coordinates
            )
            queries.append(query)
        rs_results: List[ResourceResult] = self.rs.get_data(queries)

        for rs_result in tqdm(rs_results):
            try:
                if rs_result.type == 200:
                    resource_df = pd.DataFrame(rs_result.results)

                    if len(resources_df) == 0:
                        resources_df = resource_df
                    else:
                        resources_df = pd.concat([resources_df, resource_df])
            except Exception as e:
                print(f"No Resource Data: {e}")
        return resources_df
