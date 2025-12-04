"""Module doc string. Leave empty for now.

Entity.py
"""

from typing import TypeVar, Generic, Any, List, Dict

from iudx.auth.Token import Token
from iudx.cat.Catalogue import Catalogue
from iudx.cat.CatalogueQuery import CatalogueQuery

from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery
from iudx.rs.ResourceResult import ResourceResult

import pandas as pd
from datetime import date, datetime, timedelta
import click
import copy
import tqdm
import json


Entity = TypeVar("T")
str_or_float = TypeVar("str_or_float", str, float)


class Entity:
    """Abstract class for Entity. Helps to create a modular interface
    for each inidividual Entity.
    """

    # TODO: need to check for better ways to load urls.
    def __init__(
        self: Entity,
        entity_id: str = None,
        cat_url: str = "https://cos.iudx.org.in/iudx/cat/v1",
        rs_url: str = "https://rs.cos.iudx.org.in/ngsi-ld/v1",
        headers: Dict = {"content-type": "application/json"},
        token: str = None,
        token_obj: Token = None,
    ):
        """Entity base class constructor for getting the resources from
                catalogue server.

        Args:
            entity_id (String): Id of the entity to be queried.
        """

        # public variables
        self.catalogue: Catalogue = Catalogue(
            cat_url=cat_url, headers=headers, token=token
        )

        self.token_obj = token_obj

        self.rs: ResourceServer = None
        self.rs_url = rs_url
        self.resources: List[Dict] = []
        self.entity_id = entity_id
        self.resources_df = None
        self.resources_json = []
        self.start_time = None
        self.end_time = None
        self.time_format = "%Y-%m-%dT%H:%M:%S+05:30"
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
            try:
                self._data_descriptor = documents_result.documents[0]["dataDescriptor"]
            except Exception as e:
                # TODO: Populate data descriptors for all resources
                self._data_descriptor = {}

            if (
                "accessPolicy" in documents_result.documents[0].keys()
                and documents_result.documents[0]["accessPolicy"] == "OPEN"
            ):
                token_obj.set_item(rs_url.split("/")[2], "resource_server", "consumer")

            # TODO: Parse the data schema from the data descriptor
            for key in self._data_descriptor.keys():
                pass

            # Fetch all Resources for the entity from Catalogue.
            cat_query = CatalogueQuery()
            param1 = {"key": "resourceGroup", "value": [self.entity_id]}
            param2 = {"key": "type", "value": ["iudx:Resource"]}

            query = cat_query.property_search(
                key=param1["key"], value=param1["value"]
            ).property_search(key=param2["key"], value=param2["value"])

            # update resources list with the resources retrieved
            # from Catalogue query.
            cat_result = self.catalogue.search_entity(query)

            self.resources = cat_result.documents

            # for res in cat_result.documents:
            #     self.resources.append(res["id"])

        elif "iudx:Resource" in documents_result.documents[0]["type"]:
            cat_query = CatalogueQuery()
            param1 = {"key": "id", "value": [self.entity_id]}
            query = cat_query.property_search(key=param1["key"], value=param1["value"])
            cat_result = self.catalogue.search_entity(query)
            self.resources = cat_result.documents
            rg = self.catalogue.get_related_entity(self.entity_id, rel="resourceGroup")
            if (
                "accessPolicy" in documents_result.documents[0].keys()
                and documents_result.documents[0]["accessPolicy"] == "OPEN"
            ):
                token_obj.set_item(rs_url.split("/")[2], "resource_server", "consumer")
            if (
                "accessPolicy" in rg.documents[0].keys()
                and rg.documents[0]["accessPolicy"] == "OPEN"
            ):
                token_obj.set_item(rs_url.split("/")[2], "resource_server", "consumer")

        # Request access token
        if token is None and token_obj is not None:
            token = token_obj.request_token()

        if "iudx:Resource" in documents_result.documents[0]["type"]:
            self.rs: ResourceServer = ResourceServer(
                rs_url=rs_url, headers=headers, token=token
            )
        else:
            self.rs: ResourceServer = ResourceServer(
                rs_url=rs_url, headers=headers, token_obj=token_obj
            )
        return

    """ Deprecated """

    def set_slot_hours(self, hours: int = 24) -> Entity:
        """Setter Method to change the query slot time for fetching data.

        Args:
            hours (Integer): Interger slot value in hours.
        """
        self.slot_hours = hours
        return self

    def set_time_format(self, format_str: str = "%Y-%m-%dT%H:%M:%S+05:30") -> Entity:
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
            resource_query.set_header(
                "token",
                self.token_obj.set_item(
                    resource["id"], "resource", "consumer"
                ).request_token(),
            )
            query = resource_query.add_entity(resource["id"])
            queries.append(query)

        rs_results: List[ResourceResult] = self.rs.get_latest(queries)

        for rs_result in rs_results:
            try:
                if rs_result.type == "urn:dx:rs:success":
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

    def make_query_batches(self, q: ResourceQuery, batch_queries: List[ResourceQuery]):
        res = []
        q_count = copy.deepcopy(q)
        q_count.count()
        res = self.rs.get_data([q_count])
        for r in res:
            if r.results[0]["totalHits"] > 5000:
                mid_time = (
                    q._start_time_datetime
                    + (q._end_time_datetime - q._start_time_datetime) / 2
                )
                mid_time_str = mid_time.strftime(self.time_format)
                qa = copy.deepcopy(q)
                qa.during_search(start_time=q._start_time, end_time=mid_time_str)
                qb = copy.deepcopy(q)
                qb.during_search(
                    start_time=mid_time.strftime(self.time_format), end_time=q._end_time
                )
                self.make_query_batches(qa, batch_queries)
                self.make_query_batches(qb, batch_queries)
            else:
                return batch_queries.append(q)

    def make_date_bins(self, start_date, end_date, date_bins):
        if end_date - start_date > timedelta(days=10):
            next_date = start_date + timedelta(days=10)
            date_bins.append(start_date.strftime(self.time_format))
            self.make_date_bins(next_date, end_date, date_bins)
        else:
            date_bins.append(start_date.strftime(self.time_format))
            date_bins.append(end_date.strftime(self.time_format))
            return

    def during_search(
        self,
        start_time: str = None,
        end_time: str = None,
        offset: int = None,
        limit: int = None,
    ) -> pd.DataFrame:
        """Method to fetch resources for temporal based search
            and generate a dataframe.

        Args:
            start_time (String): The starting timestamp for the query.
            end_time (String): The ending timestamp for the query.
            offset (Integer): The offset from the first result to fetch.
            limit (Integer): The maximum results to be returned.

        Returns:
            resources_df (pd.DataFrame): Pandas DataFrame with temporal data.
        """
        print("Downloading data. This may take a while")
        self.start_time = start_time
        self.end_time = end_time

        start_date = datetime.strptime(self.start_time, self.time_format)
        end_date = datetime.strptime(self.end_time, self.time_format)

        if end_date <= start_date:
            raise RuntimeError("'end_time' should be greater than 'start_time'")

        date_bins = []
        self.make_date_bins(start_date, end_date, date_bins)

        resources_df = pd.DataFrame()

        """ Make batch queries """
        queries = []
        for i in range(0, len(date_bins) - 1):
            resource_query = ResourceQuery()
            resource_query.set_header("token", self.token_obj.request_token())
            resource_query.set_offset_limit(offset, limit)
            resource_query.add_entity(self.resources[0]["id"])
            resource_query.during_search(
                start_time=date_bins[i], end_time=date_bins[i + 1]
            )
            batch_queries = []
            self.make_query_batches(resource_query, batch_queries)
            queries += batch_queries

        rs_results: List[ResourceResult] = self.rs.get_data(queries)

        for rs_result in rs_results:
            try:
                if rs_result.type == "urn:dx:rs:success":
                    resource_df = pd.json_normalize(rs_result.results)
                    self.resources_json = self.resources_json + rs_result.results
                    if len(resources_df) == 0:
                        resources_df = resource_df
                    else:
                        resources_df = pd.concat([resources_df, resource_df])
                elif rs_result.type == 401:
                    raise RuntimeError("urn:dx:rs:invalidAuthorizationToken")
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

    def property_search(
        self, key: str = None, value: str_or_float = None, operation: str = None
    ) -> pd.DataFrame:
        """Method to fetch resources for static datasources
            and generate a dataframe.

        Args:
            key (String): Property key to query.
            value (str/float): Values for the comparision with the key.
            operation (String): Operation to be performed
                between key and value.

        Returns:
            resources_df (pd.DataFrame): Pandas DataFrame with property data.
        """
        """ Make batch queries """
        queries = []
        limit = 5000
        curr_offset = 0
        # Max documents currently retrievable
        max_total_hits = 1e6
        curr_total_hits = 1e6
        resources_df = pd.DataFrame()
        total_results = []

        for resource in self.resources:
            while (curr_offset + 1 < curr_total_hits) and (
                curr_offset + 1 < max_total_hits
            ):
                resource_query = ResourceQuery()
                resource_query.set_offset_limit(curr_offset, limit)
                resource_query.add_entity(resource["id"])
                resource_query.property_search(
                    key="id", value=resource["id"], operation=operation
                )
                rs_results = self.rs.get_data_using_get([resource_query])
                curr_offset += 5000
                curr_total_hits = rs_results[0].totalHits
                if rs_results[0].type == "urn:dx:rs:success":
                    self.resources_json = self.resources_json + rs_results[0].results
                    resource_df = pd.json_normalize(rs_results[0].results)
                    resources_df = pd.concat([resources_df, resource_df])

        resources_df = resources_df.reset_index(drop=True)
        self.resources_df = resources_df
        return resources_df

    def geo_search(
        self,
        geoproperty: str = None,
        geometry: str = None,
        georel: str = None,
        _max_distance: int = None,
        coordinates: List[Any] = None,
    ) -> pd.DataFrame:
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
                coordinates=coordinates,
            )
            queries.append(query)
        rs_results: List[ResourceResult] = self.rs.get_data(queries)

        for rs_result in rs_results:
            try:
                if rs_result.type == "urn:dx:rs:success":
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

    def download(self, file_name: str = None, file_type: str = "csv") -> Entity:
        """Method to use the dataframe generated using generated queries
            and download it in form of a zip file.

        Args:
            file_name (String): Custom file name for downloading.
            file_type (String): The format in which data is downloaded.
        """
        supported_file_types = ["csv", "json", "parquet"]
        try:
            file_type = file_type.lower()
        except:
            pass

        if file_name is not None:
            file_name = file_name.split(".")[0]
        else:
            file_name = (
                f"{self.entity_id.split('/')[-1]}_{self.start_time}_{self.end_time}"
            )

        compression_opts = dict(method="zip", archive_name=f"{file_name}.{file_type}")

        if self.resources_df is not None:
            if file_type == "csv":
                self.resources_df.to_csv(
                    f"{file_name}.csv",
                    index=False,
                    # compression=compression_opts
                )
                print(f"File downloaded successfully: '{file_name}")
            elif file_type == "json":
                with open(file_name + ".json", "w") as f:
                    json.dump(self.resources_json, f)
                print(f"File downloaded successfully: '{file_name}.json'")
            elif file_type == "parquet":
                self.resources_df.to_parquet(f"{file_name}.parquet")
            else:
                raise RuntimeError(
                    f"File type is not supported. \
                    \nPlease choose a file type: \
                    \n{supported_file_types}"
                )
        else:
            raise RuntimeError("Temporal query is required to download data.")
        return self

    @click.command()
    @click.pass_context
    @click.option(
        "--entity",
        "entity_id",
        default=None,
        required=True,
        type=str,
        help="Entity Id to query.",
    )
    @click.option(
        "--auth_url",
        "auth_url",
        default=None,
        type=str,
        help="{domain_name}/{auth}/{v1}",
    )
    @click.option(
        "--cat_url",
        "cat_url",
        default=None,
        type=str,
        help="{domain_name}/{iudx}/{cat}/{v1}",
    )
    @click.option(
        "--rs_url",
        "rs_url",
        default=None,
        type=str,
        help="{domain_name}/{ngsi-ld}/{v1}",
    )
    @click.option(
        "--token", "token", default=None, type=str, help="Consumer Token for Resource."
    )
    @click.option(
        "--start", "start_time", default=None, type=str, help="Starting time for query."
    )
    @click.option(
        "--end", "end_time", default=None, type=str, help="Ending time for query."
    )
    @click.option(
        "--download",
        "file_name",
        default=None,
        type=str,
        help="Download file with custom name.",
    )
    @click.option(
        "--type",
        "file_type",
        default=None,
        type=str,
        help="Format in which file is downloaded.",
    )
    @click.option(
        "--latest", is_flag=True, default=None, type=str, help="Get latest data"
    )
    @click.option(
        "--meta",
        is_flag=True,
        default=None,
        type=str,
        help="Get meta information of resource(s)",
    )
    @click.option(
        "--offset",
        "offset",
        default=None,
        type=str,
        help="The offset from the first result to fetch.",
    )
    @click.option(
        "--limit",
        "limit",
        default=None,
        type=str,
        help="The maximum results to be returned.",
    )
    @click.option(
        "--clientid",
        "client_id",
        default=None,
        type=str,
        help="Client Id for requesting token.",
    )
    @click.option(
        "--secret",
        "client_secret",
        default=None,
        type=str,
        help="Client Secret for requesting token.",
    )
    @click.option(
        "--entity-type", "entity_type", default=None, type=str, help="Type of the item"
    )
    @click.option(
        "--role", "role", default="consumer", type=str, help="Role of the user"
    )
    def cli(
        self,
        auth_url,
        cat_url,
        rs_url,
        entity_id,
        token,
        start_time,
        end_time,
        file_name,
        file_type,
        latest,
        meta,
        client_id,
        client_secret,
        entity_type,
        role,
        offset,
        limit,
    ) -> Entity:
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
            client_id (String): Client Id for requesting token.
            client_secret (String): Client Secret for requesting token.
            entity_type (String): Type of the Entity.
            role (String):  Role of the User.
            offset (String): The offset from the first result to fetch.
            limit (String): The maximum results to be returned.
        """

        print(meta, start_time, end_time, latest)
        entity = None
        if entity_id is not None:
            if token is None and client_id is not None and client_secret is not None:
                token_obj = Token(client_id=client_id, client_secret=client_secret)
                if auth_url is not None:
                    token_obj.auth_url = auth_url
                if entity_type is not None and role is not None:
                    token_obj.set_item(
                        item_id=entity_id, item_type=entity_type, role=role
                    )
                if cat_url is None and rs_url is None:
                    entity = Entity(entity_id=entity_id, token_obj=token_obj)
                else:
                    entity = Entity(
                        cat_url=cat_url,
                        rs_url=rs_url,
                        entity_id=entity_id,
                        token_obj=token_obj,
                    )
            else:
                entity = Entity(entity_id=entity_id, token=token)

        else:
            raise RuntimeError("Some arguments are missing. \nUse: iudx --help.")

        if (
            entity_id is not None
            and start_time is not None
            and end_time is not None
            and file_name is not None
            and file_type is not None
        ):
            entity.during_search(
                start_time=start_time, end_time=end_time, offset=offset, limit=limit
            )
            entity.download(file_name, file_type)

        elif (
            meta is None and start_time is None and end_time is None and latest is None
        ):
            entity.property_search(key="id", value=entity_id, operation="==")
            entity.download(file_name, file_type)

        elif meta:
            entity = Entity(entity_id=entity_id)
            with open(entity_id.split("/")[-1] + ".txt", "w") as f:
                f.write(json.dumps(entity.resources, indent=4))
                print("File saved as " + entity_id.split("/")[-1] + ".txt")

        elif latest:
            df = entity.latest()
            try:
                df.drop(["id"], axis=1, inplace=True)
            except:
                pass
            print("Displaying top few rows of latest data:")
            print("=" * 50)
            print(df.head(10))

            print("=" * 50)
            print(f"Latest Data has {df.shape[0]} rows and {df.shape[1]} columns.")

        else:
            raise RuntimeError("Some arguments are missing. \nUse: iudx --help")

        return self
