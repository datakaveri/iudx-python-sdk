"""Module doc string. Leave empty for now.

CatalogueQuery.py
"""

from typing import TypeVar, Generic, Any, List, Dict

CatalogueQuery = TypeVar('T')


class CatalogueQuery():
    """Abstract class for Catalogue Query. Helps to create a modular interface
       for the API to construct query in Python.
    """

    def __init__(self: CatalogueQuery):
        """CatalogueQuery base class constructor
        """
        self._geoproperty: str = None
        self._geometry: str = None
        self._georel: str = None
        self._max_distance: int = None
        self._coordinates: List[Any] = None
        self._key: List[str] = []
        self._value: List[List[str]] = []
        self._text_query: str = None
        self._filters: List[str] = None
        return

    def geo_search(self, geoproperty: str=None, geometry: str=None, 
                   georel: str=None, max_distance: int=None, 
                   coordinates: List[Any]=None) -> CatalogueQuery: 
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

    def property_search(self, key: str=None, 
                        value: List[str]=None) -> CatalogueQuery:
        """Method to instantiate query for property based search.

        Args:
            key (String): Property key to tag the values for search.
            value (List[str]): List of values to be searched.
        """
        self._key.append(key)
        self._value.append(value)
        return self

    def text_search(self, text_query: str=None) -> CatalogueQuery:
        """Method to instantiate query for text based search.

        Args:
            text_query (String): Text to be queried.
        """
        self._text_query: str = text_query
        return self

    def add_filters(self, filters: List[str]=None) -> CatalogueQuery:
        """Method to instantiate query for filter based search.

        Args:
            filters (List[str]): Filters to be filtered.
        """
        self._filters: List[str] = filters
        return self

    def get_query(self) -> str:
        """Method to build query for geo, text, propery and filter.

        Returns:
            opts (String): options as a string for the generated query.
        """
        geo_opts: str = ""
        property_opts: str = ""
        text_opts: str = ""
        filter_opts: str = ""
        opts: str = ""

        if self._geoproperty is not None:
            geo_opts = ("geoproperty=" + self._geoproperty + "&" +
                        "georel=" + self._georel + "&" +
                        "maxDistance=" + str(self._max_distance) + "&" +
                        "geometry=" + self._geometry + "&" +
                        "coordinates=" + str(self._coordinates)
                        )

            # if opts != "":
            #     opts += "&"
            opts += geo_opts

        if len(self._key) > 0:
            property_opts = ("property=" +
                             str(self._key)
                             .replace("\'", "")
                             .replace('\"', '')
                             + "&" +
                             "value=" + str(self._value)
                             .replace("\'", "")
                             .replace('\"', '')
                             )

            if opts != "":
                opts += "&"
            opts += property_opts

        if self._text_query is not None:
            text_opts = ("q=" + self._text_query)

            if opts != "":
                opts += "&"
            opts += text_opts

        if self._filters is not None:
            filter_opts = ("filter=" +
                           str(self._filters)
                           .replace("\'", "")
                           .replace('\"', ''))

            if opts != "":
                opts += "&"
            opts += filter_opts

        return opts
