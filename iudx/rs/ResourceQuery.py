"""Module doc string. Leave empty for now.

ResourceQuery.py
"""

from typing import TypeVar, Generic, Any, List, Dict
import json

ResourceQuery = TypeVar('T')
str_or_float = TypeVar('str_or_float', str, float)


class ResourceQuery():
    """Abstract class for Resource Query. Helps to create
        a modular interface for the API to construct query in Python.
    """

    def __init__(self: ResourceQuery):
        """ResourceQuery base class constructor
        """
        self._geoproperty: str = None
        self._geometry: str = None
        self._georel: str = None
        self._max_distance: int = None
        self._coordinates: List[Any] = None
        self._start_time: str = None
        self._end_time: str = None
        self._key: str = None
        self._value: str_or_float = None
        self._operation: str = None
        self._text_query: str = None
        self._filters: List[str] = []
        self._entities: List[str] = []
        return

    def add_entity(self, iid: str) -> ResourceQuery:
        """Method to add ids to the entity list.

        Args:
            iid (String): Resource Id for a resource.
        """
        self._entities.append(iid)
        return self

    def geo_search(self, geoproperty: str=None, geometry: str=None,
                   georel: str=None, max_distance: int=None,
                   coordinates: List[Any]=None) -> ResourceQuery:
        """Method to instantiate query for geo based search.
            TODO: Need to validate input params here.

        Args:
            geoproperty (String): Which geoproperty to query.
            geometry (String): GeoJson geometries.
            georel (String): Geo-relationship.
            max_distance (Integer): Radius from the center in meters.
            coordinates (List[Any]): The Coordinates of the geometry.
        """
        self._geoproperty = geoproperty
        self._geometry = geometry
        self._georel = georel
        self._max_distance = max_distance
        self._coordinates = coordinates
        return self

    def during_search(self, start_time: str=None,
                      end_time: str=None) -> ResourceQuery:
        """Method to instantiate query for temporal based search.

        Args:
            start_time (String): The starting timestamp for the search.
            end_time (String): The ending timestamp for the search.
        """
        self._start_time = start_time
        self._end_time = end_time
        return self

    def property_search(self, key: str=None, value: str_or_float=None,
                        operation: str=None) -> ResourceQuery:
        """Method to instantiate query for property based search.

        Args:
            key (String): Property key to query.
            value (str/float): Values for the comparision with the key.
            operation (String): Operation to be performed
                between key and value.
        """
        self._key = key
        self._value = value
        self._operation = operation
        return self

    def add_filters(self, filters: List[str]=None) -> ResourceQuery:
        """Method to instantiate query for filter based search.

        Args:
            filters (List[str]): Filters to be applied to query for search.
        """
        self._filters = filters
        return self

    def latest_search(self) -> str:
        """Method to instantiate query for latest resource search
                based on the resource entities (Ids).

        Returns:
            latest_opts (String): query string for latest resource.
        """
        latest_opts: str = ""

        if len(self._entities) == 1:
            latest_opts = ("/" + self._entities[0])
        elif len(self._entities) > 1:
            raise RuntimeError("Multiple entities not supported.")
        else:
            raise RuntimeError("Latest search requires at least one entity.")
        return latest_opts

    def get_query(self) -> str:
        """Method to build query for geo, temporal, propery and add filter.

        Returns:
            opts (String): options as a string for the generated query.
        """
        entities_opts: List[Dict] = []
        geo_opts: Dict = {}
        temporal_opts: Dict = {}
        property_opts: str = ""
        filter_opts: str = ""
        opts: Dict = {}

        if self._entities is not None and len(self._entities) > 0:
            opts["type"] = "Query"

            for entity in self._entities:
                entities_opts.append({"id": entity})

            opts["entities"] = entities_opts

            # during search query
            if self._start_time is not None:
                if self._end_time is not None:
                    temporal_opts["timerel"] = "during"
                    temporal_opts["time"] = self._start_time
                    temporal_opts["endtime"] = self._end_time
                    temporal_opts["timeProperty"] = "observationDateTime"

                    opts["temporalQ"] = temporal_opts
                else:
                    raise RuntimeError("Temproral search requires end time.")

            # geo search query
            if self._geoproperty is not None:
                if bool(temporal_opts):
                    geo_opts["geometry"] = self._geometry
                    geo_opts["coordinates"] = self._coordinates
                    geo_opts["georel"] = self._georel + ";" + \
                        "maxDistance=" + str(self._max_distance)
                    geo_opts["geoproperty"] = self._geoproperty

                    opts["geoQ"] = geo_opts
                else:
                    raise RuntimeError("Geo search needs temporal components.")

            # property search query
            if self._key is not None:
                if bool(temporal_opts):
                    property_opts = (
                        self._key +
                        self._operation +
                        str(self._value)
                        )

                    opts["q"] = property_opts

                else:
                    raise RuntimeError("Property search needs temporal components.")

            # adding filters to query.
            if self._filters is not None and len(self._filters) > 0:
                for f in self._filters:
                    if filter_opts != "":
                        filter_opts += ","
                    filter_opts += f

                opts["attrs"] = filter_opts
        else:
            raise RuntimeError("Minimum one entity is requred.")

        return json.dumps(opts)
