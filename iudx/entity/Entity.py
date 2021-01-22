"""Module doc string. Leave empty for now.

Entity.py
"""
from typing import TypeVar, Generic, Any, List, Dict

from iudx.cat.Catalogue import Catalogue
from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery
from iudx.entity.IUDXEntity import IUDXEntity

import pandas as pd

Entity = TypeVar('T')
str_or_float = TypeVar('str_or_float', str, float)


class Entity():
    """Abstract class for Entity. Helps to create a modular interface
       for each inidividual Entity.
    """

    def __init__(self: Entity):
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        self.rs: ResourceServer = None
        self.resources: List[str] = None

        self._iudx_entity_type: str = None
        self._iudx_entity_id: str = None
        self._voc_url: str = None
        self._cat_doc: Dict = None
        self._data_descriptor: Dict = None
        self._geo_properties: List[Dict] = None
        self._time_properties: List[Dict] = None
        self._quantitative_properties: List[Dict] = None
        self._properties: List[Dict] = None
        return

    def set_rs(self, rs_url: str=None, token: str=None, 
               headers: Dict=None) -> Entity:
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        self.rs = ResourceServer(rs_url, token, headers)

        return self

    def latest(self) -> pd.DataFrame:
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        df = pd.DataFrame()
        self.resources = IUDXEntity.get_resources(self.iudx_entity_id)
        for resource in self.resources:
           query = ResourceQuery()
           query.add_entity(resource)
           result = self.rs.get_latest(query)
           
           if result.type==200:
               df_rs = pd.DataFrame(result.results)
               df.append(df_rs)
            #TODO: error handling

        return df

    def during_search(self, start_time: str=None,
                      end_time: str=None) -> pd.DataFrame:
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        df = pd.DataFrame()
        self.resources = IUDXEntity.get_resources(self._iudx_entity_id)
        for resource in self.resources:
            query = ResourceQuery()
            query.add_entity(resource)
            query.during_search(start_time, end_time)

            result = self.rs.get_during(query)
            if result.type==200:
                df_rs = pd.DataFrame(result.results)
                df.append(df_rs)
             #TODO: error handling

        return df

    def property_search(self, key: str=None, value: str_or_float=None, 
                        operation: str=None) -> pd.DataFrame:
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def geo_search(self, geoproperty: str=None, geometry: str=None,
                   georel: str=None, _max_distance: int=None,
                   coordinates: List[Any]=None) -> pd.DataFrame:
        """Pydoc heading.
        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self
