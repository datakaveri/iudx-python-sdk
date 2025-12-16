"""Module doc string. Leave empty for now.

Entity.py
"""

from typing import TypeVar, Generic, Any, List, Dict, Optional
import time
import requests
import sys

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

    def async_search(
        self,
        start_time: str = None,
        end_time: str = None,
    ) -> Dict:
        """Initiate an asynchronous search request for large datasets.
        
        This method starts an async download job on the server and returns
        a searchId that can be used to track progress and retrieve results.

        Args:
            start_time (String): The starting timestamp for the query.
            end_time (String): The ending timestamp for the query.

        Returns:
            Dict: Response containing searchId and status information.
        """
        self.start_time = start_time
        self.end_time = end_time
        
        start_date = datetime.strptime(self.start_time, self.time_format)
        end_date = datetime.strptime(self.end_time, self.time_format)

        if end_date <= start_date:
            raise RuntimeError("'end_time' should be greater than 'start_time'")

        # Get the resource ID
        resource_id = self.resources[0]["id"]
        
        # Build the async search URL
        async_url = f"{self.rs_url}/async/search"
        params = {
            "id": resource_id,
            "timerel": "during",
            "time": start_time,
            "endtime": end_time
        }
        
        # Get token
        token = self.token_obj.request_token()
        headers = {"token": token}
        
        # Make the async search request
        response = requests.get(async_url, params=params, headers=headers)
        
        if response.status_code not in [200, 201]:
            raise RuntimeError(f"Async search request failed: {response.status_code} - {response.text}")
        
        result = response.json()
        return result

    def async_status(
        self,
        search_id: str = None,
    ) -> Dict:
        """Check the status of an asynchronous search request.

        Args:
            search_id (String): The searchId returned from async_search.

        Returns:
            Dict: Status information including progress and download URLs when ready.
        """
        if search_id is None:
            raise RuntimeError("search_id is required")
        
        # Build the status URL
        status_url = f"{self.rs_url}/async/status"
        params = {"searchId": search_id}
        
        # Get token
        token = self.token_obj.request_token()
        headers = {"token": token}
        
        # Make the status request
        response = requests.get(status_url, params=params, headers=headers)
        
        if response.status_code not in [200, 201]:
            raise RuntimeError(f"Async status request failed: {response.status_code} - {response.text}")
        
        result = response.json()
        return result

    def _format_time(self, seconds: int) -> str:
        """Format seconds into human-readable time string."""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            mins, secs = divmod(seconds, 60)
            return f"{mins}m {secs}s"
        else:
            hours, remainder = divmod(seconds, 3600)
            mins, secs = divmod(remainder, 60)
            return f"{hours}h {mins}m {secs}s"

    def _render_progress_bar(self, progress_pct: int, width: int = 30) -> str:
        """Render a text-based progress bar."""
        filled = int(width * progress_pct / 100)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        return f"[{bar}]"

    def async_download(
        self,
        start_time: str = None,
        end_time: str = None,
        file_name: str = None,
        poll_interval: int = 5,
        max_poll_time: int = 3600,
        progress: bool = True,
    ) -> Optional[str]:
        """Perform an asynchronous download with polling for completion.
        
        This method initiates an async search, polls for completion,
        and downloads the result file when ready. Displays a continuous
        progress bar until download is complete.

        Args:
            start_time (String): The starting timestamp for the query.
            end_time (String): The ending timestamp for the query.
            file_name (String): Custom file name for downloading (without extension).
            poll_interval (int): Seconds between status checks (default: 5).
            max_poll_time (int): Maximum seconds to wait for completion (default: 3600).
            progress (bool): Show progress updates (default: True).

        Returns:
            Optional[str]: Path to downloaded file, or None if download failed.
        """
        if progress:
            print("=" * 60)
            print("  IUDX Async Download")
            print("=" * 60)
            print(f"  Entity: {self.entity_id.split('/')[-1]}")
            print(f"  Period: {start_time} to {end_time}")
            print("-" * 60)
            print("  [1/3] Initiating async search request...")
        
        # Initiate async search
        search_result = self.async_search(start_time=start_time, end_time=end_time)
        
        if "result" not in search_result or len(search_result["result"]) == 0:
            raise RuntimeError(f"Async search failed: {search_result}")
        
        search_id = search_result["result"][0]["searchId"]
        
        if progress:
            print(f"        SearchId: {search_id}")
            print("-" * 60)
            print("  [2/3] Processing data on server...")
            print()
        
        # Poll for completion
        elapsed_time = 0
        download_url = None
        last_progress = -1
        
        while elapsed_time < max_poll_time:
            status_result = self.async_status(search_id=search_id)
            
            # Handle different response formats - check both "results" and "result"
            results_list = status_result.get("results") or status_result.get("result") or []
            
            if len(results_list) > 0:
                status_info = results_list[0]
                status = status_info.get("status", "UNKNOWN").upper()
                progress_pct = status_info.get("progress", 0)
                
                if progress and progress_pct != last_progress:
                    last_progress = progress_pct
                    progress_int = int(progress_pct)
                    bar = self._render_progress_bar(progress_int)
                    elapsed_str = self._format_time(elapsed_time)
                    status_line = f"\r        {bar} {progress_int:3d}%  |  Status: {status:<12}  |  Elapsed: {elapsed_str}"
                    print(status_line, end="", flush=True)
                
                # Check for completion - handle various status values
                if status in ["COMPLETE", "COMPLETED", "SUCCEEDED", "SUCCESS", "DONE"]:
                    # Try different keys for the download URL
                    download_url = (
                        status_info.get("file-download-url") or
                        status_info.get("file") or 
                        status_info.get("fileUrl") or 
                        status_info.get("downloadUrl") or
                        status_info.get("url") or
                        status_info.get("objectUrl")
                    )
                    if progress:
                        bar = self._render_progress_bar(100)
                        elapsed_str = self._format_time(elapsed_time)
                        print(f"\r        {bar} 100%  |  Status: COMPLETE      |  Elapsed: {elapsed_str}")
                        print()
                        print("-" * 60)
                        print("  [3/3] Downloading file...")
                    break
                elif status in ["FAILED", "ERROR", "FAILURE"]:
                    if progress:
                        print()
                    raise RuntimeError(f"Async download failed: {status_info}")
            
            time.sleep(poll_interval)
            elapsed_time += poll_interval
        
        if download_url is None:
            if progress:
                print()
                print(f"\n  Debug - Last status response: {status_result}")
            if elapsed_time >= max_poll_time:
                raise RuntimeError(f"Async download timed out after {max_poll_time} seconds")
            raise RuntimeError(f"No download URL received. Last status: {status_result}")
        
        # Determine file name
        if file_name is None:
            file_name = f"{self.entity_id.split('/')[-1]}_{self.start_time}_{self.end_time}_async"
        else:
            file_name = file_name.split(".")[0]
        
        # Get token for download
        token = self.token_obj.request_token()
        headers = {"token": token}
        
        # Download the file with progress
        response = requests.get(download_url, headers=headers, stream=True)
        
        if response.status_code not in [200, 201]:
            raise RuntimeError(f"Download failed: {response.status_code} - {response.text}")
        
        # Async downloads always return JSON
        output_file = f"{file_name}.json"
        
        # Get file size if available
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        
        # Write to file with download progress
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                
                if progress and total_size > 0:
                    pct = int(100 * downloaded / total_size)
                    bar = self._render_progress_bar(pct)
                    size_mb = downloaded / (1024 * 1024)
                    total_mb = total_size / (1024 * 1024)
                    print(f"\r        {bar} {pct:3d}%  |  {size_mb:.1f} / {total_mb:.1f} MB", end="", flush=True)
        
        if progress:
            if total_size > 0:
                print()
            print()
            print("=" * 60)
            print(f"  ✓ Download complete: {output_file}")
            if total_size > 0:
                print(f"  ✓ File size: {total_size / (1024 * 1024):.2f} MB")
            print("=" * 60)
        
        return output_file

    def async_search_only(
        self,
        start_time: str = None,
        end_time: str = None,
        output_file: str = None,
    ) -> str:
        """Initiate an async search and save the searchId to a file.
        
        Useful for batch processing where you want to start multiple 
        downloads and check their status later.

        Args:
            start_time (String): The starting timestamp for the query.
            end_time (String): The ending timestamp for the query.
            output_file (String): File to save the searchId (default: async_search_ids.json).

        Returns:
            str: The searchId for this request.
        """
        search_result = self.async_search(start_time=start_time, end_time=end_time)
        
        if "result" not in search_result or len(search_result["result"]) == 0:
            raise RuntimeError(f"Async search failed: {search_result}")
        
        search_id = search_result["result"][0]["searchId"]
        
        if output_file is None:
            output_file = "async_search_ids.json"
        
        # Append to existing file or create new
        try:
            with open(output_file, "r") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []
        
        existing.append({
            "searchId": search_id,
            "entity_id": self.entity_id,
            "start_time": start_time,
            "end_time": end_time,
            "created_at": datetime.now().isoformat()
        })
        
        with open(output_file, "w") as f:
            json.dump(existing, f, indent=2)
        
        print(f"Async search initiated. SearchId: {search_id}")
        print(f"SearchId saved to: {output_file}")
        
        return search_id

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
    @click.option(
        "--async",
        "async_mode",
        is_flag=True,
        default=False,
        help="Use async download for large datasets.",
    )
    @click.option(
        "--async-status",
        "async_status_id",
        default=None,
        type=str,
        help="Check status of async download with given searchId.",
    )
    @click.option(
        "--async-only",
        "async_only",
        is_flag=True,
        default=False,
        help="Start async download without waiting (saves searchId to file).",
    )
    @click.option(
        "--poll-interval",
        "poll_interval",
        default=5,
        type=int,
        help="Seconds between status checks for async download (default: 5).",
    )
    @click.option(
        "--max-poll-time",
        "max_poll_time",
        default=3600,
        type=int,
        help="Maximum seconds to wait for async download (default: 3600).",
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
        async_mode,
        async_status_id,
        async_only,
        poll_interval,
        max_poll_time,
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
            async_mode (Boolean): Flag to use async download.
            async_status_id (String): SearchId to check async status.
            async_only (Boolean): Flag to start async without waiting.
            poll_interval (int): Seconds between async status checks.
            max_poll_time (int): Maximum seconds to wait for async download.
        """
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

        # Handle async status check (can be done without start/end times)
        if async_status_id is not None:
            status = entity.async_status(search_id=async_status_id)
            print(json.dumps(status, indent=2))
            return self

        # Handle async download modes
        if async_mode and start_time is not None and end_time is not None:
            if async_only:
                # Just start the async download and save searchId
                entity.async_search_only(
                    start_time=start_time,
                    end_time=end_time,
                    output_file=file_name + "_searchids.json" if file_name else None,
                )
            else:
                # Full async download with polling
                entity.async_download(
                    start_time=start_time,
                    end_time=end_time,
                    file_name=file_name,
                    poll_interval=poll_interval,
                    max_poll_time=max_poll_time,
                )
            return self

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
