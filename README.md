# IUDX Python SDK

[![Documentation Status](https://readthedocs.org/projects/pyiudx/badge/?version=latest)](https://pyiudx.readthedocs.io/en/latest/?badge=latest)

<img src="https://github.com/iudx/pyIUDX/blob/master/docs/pyIUDX.png" alt="pyIUDX" width=150 height=150>

Simplifies using the India Urban Data Exchange [IUDX](https://iudx.org.in) platform. 
Provides an API interface to perform scientific computing over various 
smart city resources. 
Vist [the pune IUDX](https://pudx.catalogue.iudx.org.in) to get a glimpse of Pune City's IUDX implementation.

## Installation
```console
pip install git+https://github.com/datakaveri/iudx-python-sdk
```

## IPython Example
A simple IPython notebook going throught the entire process flow can be found here.
[Getting Started.ipynb](https://github.com/datakaveri/iudx-python-sdk/blob/master/examples/Getting%20Started.ipynb)

A sample notebook to download sensors' data is also available. [Download ITMS Dataset.ipynb](https://github.com/datakaveri/iudx-python-sdk/blob/master/examples/Download%20ITMS%20Dataset.ipynb)

### 1) Catalogue text search example
* Get the catalogue list of all sensors based on a text search query.

```python
from iudx.cat.Catalogue import Catalogue
from iudx.cat.CatalogueQuery import CatalogueQuery

# creating an object of Catalogue class using cat_url.
cat = Catalogue(
          cat_url="https://api.catalogue.iudx.io/iudx/cat/v1",
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
```

### 2) Resource server get latest example
* Get the latest data for specific entity id.

```python
from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery

# entity id for the pune env aqm sensor.
entity_id = "datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/f36b4669-628b-ad93-9970-f9d424afbf75"

# creating an object of ResourceServer class using rs_url.
rs = ResourceServer(
         rs_url="https://rs.iudx.org.in/ngsi-ld/v1",
         headers={"content-type": "application/json"}
     )

# creating a query for fetching latest data for the entity_id.
rs_query = ResourceQuery()
rs_entity = rs_query.add_entity(entity_id)

# fetch results for a list of entities.
results = rs.get_latest([rs_entity])

# printing results
print(f"RESULTS: {results[0].results}")        # get the result data of the resource query.
print(f"STATUS: {results[0].type}")            # get the status code for the response.
```

### 3) Resource server during example
* Get the during data for specific entity id.

```python
from iudx.rs.ResourceServer import ResourceServer
from iudx.rs.ResourceQuery import ResourceQuery

# entity id for the pune env aqm sensor.
entity_id = "datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/f36b4669-628b-ad93-9970-f9d424afbf75"

# creating an object of ResourceServer class using rs_url.
rs = ResourceServer(
         rs_url="https://rs.iudx.org.in/ngsi-ld/v1",
         headers={"content-type": "application/json"}
     )

# creating a query for fetching latest data for the entity_id.
rs_query = ResourceQuery()
rs_entity = rs_query.add_entity(entity_id)

# create a during query for a time interval.
during_query = rs_entity.during_search(
                   start_time="2021-01-01T14:20:00Z",
                   end_time="2021-01-09T14:20:00Z"
               )

# fetch results for the list of during queries.
results = rs.get_data([during_query])

# printing results
print(f"RESULTS: {results[0].results}")        # get the result data of the resource query.
print(f"STATUS: {results[0].type}")            # get the status code for the response.
```

### 4) Entity data download example
* Get the data for the specific entity and download the generated pandas.dataframe as a .CSV zipped file.

```python
from iudx.entity.Entity import Entity

# entity id for the pune env aqm sensor.
entity_id = "datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/f36b4669-628b-ad93-9970-f9d424afbf75"

# Creating an entity for the sensor.
entity = Entity(entity_id)

# create a during query for a time interval.
df = entity.during_search(
         start_time="2021-01-01T14:20:00Z",
         end_time="2021-01-09T14:20:00Z"
     )

display(df.head())

# To download the dataset 
file_name = "IUDX_data"    # custom name of the file
file_type = "csv"          # can be CSV or JSON

# download method for saving data to zip file.
entity.download(file_name=file_name)
```

## CLI

### 1) Download the data based on a during entity query.
```
# Sample command
iudx 
  --entity <entity_id> 
  --token <token_id> (only for private resources which requires auth)
  --start <start_timestamp> 
  --end <end_timestamp> 
  --download <file_name>
  --type <file_type_csv_or_json>

# Example
iudx --entity datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/f36b4669-628b-ad93-9970-f9d424afbf75 --start 2021-01-01T14:20:00Z --end 2021-01-07T14:20:00Z --download test_file --type csv
```

### 2) Print the latest entity data in the console.
```
# Sample command
iudx 
  --entity <entity_id> 
  --token <token_id> (only for private resources which requires auth)
  --latest

# Example
iudx --entity datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/f36b4669-628b-ad93-9970-f9d424afbf75 --latest
```
NOTE: `--token` is required for the entities which are not public.<br>
Use: `iudx --help` to know more about all possible options.

## API Docs
Further documentation on low level apis and their usage can be found here. [Docs]()


## Usage Examples
The [Tests](tests/) directory and the examples directory contain further usage examples. [Examples](examples/).
