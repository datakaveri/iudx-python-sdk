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
