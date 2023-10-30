"""Module doc string. Leave empty for now.

Catalogue.py
"""

from typing import TypeVar, Generic, Any, List, Dict

from iudx.common.HTTPEntity import HTTPEntity
from iudx.common.HTTPResponse import HTTPResponse

from iudx.cat.CatalogueQuery import CatalogueQuery
from iudx.cat.CatalogueResult import CatalogueResult


class Catalogue():
    """Abstract class for Catalogue. Helps to create a modular interface
       for the API to implement queries.
    """

    def __init__(self, cat_url: str=None, token: str=None,
                 headers: Dict[str, str]=None):
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        if (cat_url is not None):
            self.url: str = cat_url
        else:
            self.url = "https://cos.iudx.org.in/iudx/cat/v1"
        self.token: str = token
        self.headers: Dict[str, str] = headers
        return

    def status(self) -> bool:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def search_entity(self, query: CatalogueQuery) -> CatalogueResult:
        """Method to get the search response for entities, based on a query.

        Args:
            query (CatalogueQuery): A query object of CatalogueQuery class.
        Returns:
            cat_result (CatalogueResult): returns a CatalogueResult object.
        """
        url = self.url + "/search"
        url = url + "?" + query.get_query()
        http_entity = HTTPEntity()
        response: HTTPResponse = http_entity.get(url, self.headers)
        result_data = response.get_json()

        cat_result = CatalogueResult()
        if response.get_status_code() == 200:
            cat_result.documents = result_data["results"]
            cat_result.total_hits = result_data["totalHits"]
            cat_result.status = result_data["type"]
        return cat_result

    def count_entity(self, query: CatalogueQuery) -> CatalogueResult:
        """Method to get the count response for entities, based on a query.

        Args:
            query (CatalogueQuery): A query object of CatalogueQuery class.
        Returns:
            cat_result (CatalogueResult): returns a CatalogueResult object.
        """
        url = self.url + "/count"
        url = url + "?" + query.get_query()
        http_entity = HTTPEntity()
        response: HTTPResponse = http_entity.get(url, self.headers)
        result_data = response.get_json()

        cat_result = CatalogueResult()
        if response.get_status_code() == 200:
            cat_result.documents = result_data["results"]
            cat_result.total_hits = result_data["totalHits"]
            cat_result.status = result_data["type"]
        return cat_result

    def list_entity(self, entity_type: str) -> CatalogueResult:
        """Method to get the list response for entities, based on an entity type.

        Args:
            entity_type (String): type must be either resource,
                resourceGroup, resourceServer.
        Returns:
            cat_result (CatalogueResult): returns a CatalogueResult object.
        """
        url = self.url + "/list"
        url = url + "/" + entity_type
        http_entity = HTTPEntity()
        response: HTTPResponse = http_entity.get(url, self.headers)
        result_data = response.get_json()

        cat_result = CatalogueResult()
        if response.get_status_code() == 200:
            cat_result.documents = result_data["results"]
            cat_result.total_hits = result_data["totalHits"]
            cat_result.status = result_data["type"]
        return cat_result

    def get_related_entity(self, iid: str, rel: str) -> CatalogueResult:
        """Method to get the relationship response for entities,
                based on their id and relation.

        Args:
            iid (String): Id of the entity.
            rel (String): Relationship attribute of the entity
                whose id is provided.
        Returns:
            cat_result (CatalogueResult): returns a CatalogueResult object.
        """
        url = self.url + "/relationship"
        url = url + "?" + "id=" + iid + "&" + "rel=" + rel
        http_entity = HTTPEntity()
        response: HTTPResponse = http_entity.get(url, self.headers)
        result_data = response.get_json()

        cat_result = CatalogueResult()
        if response.get_status_code() == 200:
            cat_result.documents = result_data["results"]
            cat_result.total_hits = result_data["totalHits"]
            cat_result.status = result_data["type"]
        return cat_result

    def rel_search(self, query: CatalogueQuery) -> CatalogueResult:
        """Pydoc heading.
        TODO: Implement the query for relationship search in CatalogueQuery
        before this function defination.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def get_item(self, iid: str) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        url = self.url + "/item"
        url = url + "?" + "id=" + iid
        http_entity = HTTPEntity()
        response: HTTPResponse = http_entity.get(url, self.headers)
        result_data = response.get_json()

        cat_result = CatalogueResult()
        if response.get_status_code() == 200:
            cat_result.documents = result_data["results"]
            cat_result.total_hits = result_data["totalHits"]
            cat_result.status = result_data["type"]
        return cat_result

    def create(self, item: Dict[str, Any]) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def update(self, item: Dict[str, Any]) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def delete(self, iid: str) -> CatalogueResult:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return self

    def validate(self, item: Dict[str, Any]) -> bool:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return False

    def update_token(self, token: str) -> None:
        """Pydoc heading.

        Args:
            argument (argument-type): argument-description
        Returns:
            returned-varaible (returned-varaible-type): return-variable-description
        """
        return None
