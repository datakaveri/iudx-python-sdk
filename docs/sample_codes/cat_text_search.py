from iudx.cat.Catalogue import Catalogue
from iudx.cat.CatalogueQuery import CatalogueQuery

# creating an object of Catalogue class using cat_url.
cat = Catalogue(
        cat_url="https://api.catalogue.iudx.org.in/iudx/cat/v1",
        headers={"content-type": "application/json"}
        )                                       

# creating a query for text search
cat_query = CatalogueQuery()
query = cat_query.text_search("aqm")

# fetching the search response for the query 
result = cat.search_entity(query)

print(f"RESULTS: {result.documents}")        # get all the search documents as json.
print(f"STATUS: {result.status}")            # get the status for the search response.
print(f"TOTAL HITS: {result.total_hits}")    # get the count of total results fetched. 
