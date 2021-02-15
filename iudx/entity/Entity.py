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
from datetime import date, datetime, timedelta
import click


Entity = TypeVar('T')
str_or_float = TypeVar('str_or_float', str, float)


class Entity():
    """Abstract class for Entity. Helps to create a modular interface
       for each inidividual Entity.
    """
    # TODO: need to check for better ways to load urls.    
    def __init__(
        self: Entity,
        entity_id: str=None,
        cat_url: str="https://api.catalogue.iudx.org.in/iudx/cat/v1",
        rs_url: str="https://rs.iudx.org.in/ngsi-ld/v1",
        headers: Dict={"content-type": "application/json"},
        token: str=None
    ):
        """Entity base class constructor for getting the resources from
                catalogue server.

        Args:
            entity_id (String): Id of the entity to be queried.
        """
        # public variables
        self.catalogue: Catalogue = Catalogue(
            cat_url=cat_url,
            headers=headers,
            token=token
        )
        self.rs: ResourceServer = None
        self.resources: List[Dict] = []
        self.entity_id = entity_id
        self.resources_df = None
        self.start_time = None
        self.end_time = None
        self.time_format = "%Y-%m-%dT%H:%M:%SZ"
        self.slot_hours = 24
        self.max_query_days = 61

        # private variables 
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

        if "iudx:ResourceGroup" in documents_result.documents[0]["type"]:
            self._data_descriptor = documents_result.documents[0]["dataDescriptor"]

            # TODO: Parse the data schema from the data descriptor
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

            self.resources = cat_result.documents
            # for res in cat_result.documents:
            #     self.resources.append(res["id"])

        elif "iudx:Resource" in documents_result.documents[0]["type"]:
            self.resources = [{"id": self.entity_id}]

        self.rs: ResourceServer = ResourceServer(
            rs_url=rs_url,
            headers=headers,
            token=token
        )
        return

    def set_slot_hours(self, hours:int=24) -> Entity:
        """Setter Method to change the query slot time for fetching data.

        Args:
            hours (Integer): Interger slot value in hours.
        """
        self.slot_hours = hours
        return self

    def set_time_format(self, format_str:str="%Y-%m-%dT%H:%M:%SZ") -> Entity:
        """Setter Method to change the query timestamp format.

        Args:
            format_str (String): String for setting time format.
        """
        self.time_format = format_str
        return self
    
    def latest(self) -> pd.DataFrame:
        """Method to fetch resources for latest data
            and generate a dataframe.

        Returns:
            resources_df (pd.DataFrame): Pandas DataFrame with latest data.
        """
        resources_df = pd.DataFrame()

        queries = []
        for resource in self.resources:
            resource_query = ResourceQuery()
            query = resource_query.add_entity(resource["id"])
            queries.append(query)

        rs_results: List[ResourceResult] = self.rs.get_latest(queries)

        for rs_result in rs_results:
            try:
                if rs_result.type == 200:
                    resource_df = pd.json_normalize(rs_result.results)

                    if len(resources_df) == 0:
                        resources_df = resource_df
                    else:
                        resources_df = pd.concat([resources_df, resource_df])
            except Exception as e:
                print(f"No Latest Data: {e}")

        # Processing data as a time series dataframe:
        # 1) converting time feature to datetime.
        # 2) sorting values based on time.
        # 3) resetting the indices for the dataframe.
        try:
            if len(resources_df) != 0:
                resources_df["observationDateTime"] = pd.to_datetime(
                    resources_df["observationDateTime"]
                    )
                resources_df = resources_df.sort_values(by="observationDateTime")
            else:
                print("No Data available during the timeframe.")
        except Exception as e:
            print(f"Data format issue: {e}")

        resources_df = resources_df.reset_index(drop=True)
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
        self.start_time = start_time
        self.end_time = end_time

        days = []
        start_date = datetime.strptime(self.start_time, self.time_format)
        end_date = datetime.strptime(self.end_time, self.time_format)

        if end_date <= start_date:
            raise RuntimeError("'end_time' should be greater than 'start_time'")

        try:
            if (end_date-start_date).days > self.max_query_days:
                raise RuntimeError("Can't query more than 2 months of data at once.")
        except:
            pass

        date = start_date
        while date <= end_date:
            days.append(date.strftime(self.time_format))
            date += timedelta(hours=self.slot_hours)
            
        if (date-end_date).seconds > 0:
            days.append(end_date.strftime(self.time_format))
        
        resources_df = pd.DataFrame()
        queries = []
        for resource in self.resources:
            for i in range(len(days)):
                resource_query = ResourceQuery()
                resource_query.add_entity(resource["id"])

                try:
                    start = days[i]
                    end = days[i+1]
                    query = resource_query.during_search(
                        start_time=start,
                        end_time=end
                    )
                    queries.append(query)
                except:
                    pass

        rs_results: List[ResourceResult] = self.rs.get_data(queries)

        for rs_result in rs_results:
            try:
                if rs_result.type == 200:
                    resource_df = pd.json_normalize(rs_result.results)

                    if len(resources_df) == 0:
                        resources_df = resource_df
                    else:
                        resources_df = pd.concat([resources_df, resource_df])
                elif rs_result.type == 401:
                    raise RuntimeError("Not Authorized: Invalid credentials")
            except Exception as e:
                print(f"No Resource Data: {e}")

        # Processing data as a time series dataframe:
        # 1) converting time feature to datetime.
        # 2) sorting values based on time.
        # 3) resetting the indices for the dataframe.
        try:
            if len(resources_df) != 0:
                resources_df["observationDateTime"] = pd.to_datetime(
                    resources_df["observationDateTime"]
                    )
                resources_df = resources_df.sort_values(by="observationDateTime")
            else:
                print("No Data available during the timeframe.")
        except Exception as e:
            print(f"Data format issue: {e}")

        resources_df = resources_df.reset_index(drop=True)
        self.resources_df = resources_df
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
        for resource in self.resources:
            resource_query = ResourceQuery()
            resource_query.add_entity(resource["id"])

            # TODO: temporal(during) query is required for property search.
            query = resource_query.property_search(
                key=key,
                value=value,
                operation=operation
            )
            queries.append(query)
        rs_results: List[ResourceResult] = self.rs.get_data(queries)

        for rs_result in rs_results:
            try:
                if rs_result.type == 200:
                    resource_df = pd.json_normalize(rs_result.results)

                    if len(resources_df) == 0:
                        resources_df = resource_df
                    else:
                        resources_df = pd.concat([resources_df, resource_df])
                elif rs_result.type == 401:
                    raise RuntimeError("Not Authorized: Invalid credentials")
            except Exception as e:
                print(f"No Resource Data: {e}")

        # Processing data as a time series dataframe:
        # 1) converting time feature to datetime.
        # 2) sorting values based on time.
        # 3) resetting the indices for the dataframe.
        try:
            if len(resources_df) != 0:
                resources_df["observationDateTime"] = pd.to_datetime(
                    resources_df["observationDateTime"]
                    )
                resources_df = resources_df.sort_values(by="observationDateTime")
            else:
                print("No Data available during the timeframe.")
        except Exception as e:
            print(f"Data format issue: {e}")

        resources_df = resources_df.reset_index(drop=True)
        self.resources_df = resources_df
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
        for resource in self.resources:
            resource_query = ResourceQuery()
            resource_query.add_entity(resource["id"])

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

        for rs_result in rs_results:
            try:
                if rs_result.type == 200:
                    resource_df = pd.json_normalize(rs_result.results)

                    if len(resources_df) == 0:
                        resources_df = resource_df
                    else:
                        resources_df = pd.concat([resources_df, resource_df])
                elif rs_result.type == 401:
                    raise RuntimeError("Not Authorized: Invalid credentials")
            except Exception as e:
                print(f"No Resource Data: {e}")

        # Processing data as a time series dataframe:
        # 1) converting time feature to datetime.
        # 2) sorting values based on time.
        # 3) resetting the indices for the dataframe.
        try:
            if len(resources_df) != 0:
                resources_df["observationDateTime"] = pd.to_datetime(
                    resources_df["observationDateTime"]
                    )
                resources_df = resources_df.sort_values(by="observationDateTime")
            else:
                print("No Data available during the timeframe.")
        except Exception as e:
            print(f"Data format issue: {e}")

        resources_df = resources_df.reset_index(drop=True)
        self.resources_df = resources_df
        return resources_df

    def download(self, file_name:str=None, file_type:str="csv") -> Entity:
        """Method to use the dataframe generated using generated queries 
            and download it in form of a zip file.

        Args:
            file_name (String): Custom file name for downloading.
            file_type (String): The format in which data is downloaded.
        """
        supported_file_types = ["csv", "json"] 
        try:    
            file_type = file_type.lower()       
        except:
            pass

        if file_name is not None:
            file_name = file_name.split(".")[0]
        else:
            file_name = f"{self.entity_id.split('/')[-1]}_{self.start_time}_{self.end_time}"

        compression_opts = dict(
            method='zip',
            archive_name=f"{file_name}.{file_type}"
        )

        if self.resources_df is not None:
            if file_type == "csv":
                self.resources_df.to_csv(
                    f"{file_name}.zip", 
                    index=False, 
                    compression=compression_opts
                )
                print(f"File downloaded successfully: '{file_name}.zip'")
            elif file_type == "json":
                self.resources_df.to_json(
                    f"{file_name}.zip", 
                    orient="records",
                    compression=compression_opts
                )
                print(f"File downloaded successfully: '{file_name}.zip'")
            else:
                raise RuntimeError(f"File type is not supported. \
                    \nPlease choose a file type: \
                    \n{supported_file_types}")            
        else:
            raise RuntimeError("Temporal query is required to download data.")
        return self

    @click.command()
    @click.pass_context
    @click.option('--entity', 'entity_id', 
        default=None, required=True, type=str, 
        help='Entity Id to query.')
    @click.option('--token', 'token', 
        default=None, type=str, 
        help='Consumer Token for Resource.')
    @click.option('--start', 'start_time', 
        default=None, type=str, 
        help='Starting time for query.')
    @click.option('--end', 'end_time', 
        default=None, type=str, 
        help='Ending time for query.')
    @click.option('--download', 'file_name', 
        default=None, type=str, 
        help='Download file with custom name.')
    @click.option('--type', 'file_type', 
        default=None, type=str, 
        help='Format in which file is downloaded.')    
    @click.option('--latest', 
        is_flag=True, default=None, type=str, 
        help='Get latest data')
    def cli(self, entity_id, token,
            start_time, end_time, 
            file_name, file_type, latest) -> Entity:
        """Method to implement the command line interface for the
        sdk for getting termporal query and download files.

        Args:
            entity_id (String): Id of the entity to be queried.
            token (String): Consumer token to access Resources.
            start_time (String): The starting timestamp for the query.
            end_time (String): The ending timestamp for the query.
            file_name (String): Custom file name for downloading.
            file_type (String): The format in which data is downloaded.
            latest (Boolean): Flag to query latest entity data.
        """
        entity = None
        if entity_id is not None and token is not None:
            entity = Entity(entity_id=entity_id, token=token)
        else:
            raise RuntimeError("Some arguments are missing. \nUse: iudx --help")

        if latest == False or latest == None:
            if entity_id is not None and \
                token is not None and \
                start_time is not None and \
                end_time is not None and \
                file_name is not None and \
                file_type is not None :

                entity.during_search(
                    start_time=start_time,
                    end_time=end_time
                )
                entity.download(file_name, file_type)
            else:
                raise RuntimeError("Some arguments are missing. \nUse: iudx --help")
        else:
            df = entity.latest()
            try:
                df.drop(["id"], axis=1, inplace=True)
            except:
                pass

            print("Displaying top few rows of latest data:")
            print("="*50)
            print(df.head(10))

            print("="*50)
            print(f"Latest Data has {df.shape[0]} rows and {df.shape[1]} columns.")
        return self
