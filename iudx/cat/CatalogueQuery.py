"""Module doc string. Leave empty for now.

CatalogueQuery.py
"""

from typing import TypeVar, Generic, Any, List, Dict

CatalogueQuery = TypeVar('T')


class CatalogueQuery():
    """Class documentation. Be a little descriptive here.

    Args:
        argument (argument-type): argument-description
    Returns:
        returned-varaible (returned-varaible-type): return-variable-description
    """

    def __init__(self: CatalogueQuery):
        """CatalogueQuery base class constructor
        """
        self._groproperty: str = None
        self._geometry: str = None
        self._georel: str = None
        self._max_distance: int = None
        self._coordinates: List[Any] = None
        self._key: List[str] = None
        self._value: List[List[str]] = None
        self._text_query: str = None
        self._filters: List[str] = None
        return

    def geo_search(self, geoproperty: str=None, geometry: str=None, 
                   georel: str=None, max_distance: int=None, 
                   coordinates: List[Any]=None) -> CatalogueQuery: 
        """Method to instantiate query for geo based search.

        Args:
            geoproperty (String): Which geoproperty to query.
            geometry (String): GeoJson geometries.
            georel (String): Geo-relationship.
            max_distance (Integer): Radius from the center in meters.
            coordinates (List[Any]): The Coordinates of the geometry
        """
        self._groproperty = geoproperty
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
        self._key: List[str] = key
        self._value: List[List[str]] = value
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
            filterOpts (CatalogueQuery): options as a string for a GET method.
        """
        geoOpts: str = ""
        propertyOpts: str = ""
        textOpts: str = ""
        filterOpts: str = ""
        opts: str = ""

        if self._groproperty is not None:
            geoOpts = ("geoproperty=" + self._groproperty + "&" +
                       "georel=" + self._georel + "&" +
                       "maxDistance=" + str(self._max_distance) + "&" +
                       "geometry=" + self._geometry + "&" +
                       "coordinates=" + str(self._coordinates)
                       )

            # if opts != "":
            #     opts += "&"
            opts += geoOpts

        if self._key is not None:
            propertyOpts = ("property=[" + self._key + "]"
                            + "&" +
                            "value=[" + str(self._value)
                            .replace("\'", "")
                            .replace('\"', '')
                            + "]")

            if opts != "":
                opts += "&"
            opts += propertyOpts

        if self._text_query is not None:
            textOpts = ("q=" + self._text_query)

            if opts != "":
                opts += "&"
            opts += textOpts

        if self._filters is not None:
            filterOpts = ("filter=" +
                          str(self._filters)
                          .replace("\'", "")
                          .replace('\"', ''))

            if opts != "":
                opts += "&"
            opts += filterOpts

        return opts
