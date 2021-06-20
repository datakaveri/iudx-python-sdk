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
