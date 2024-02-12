# import required module
#import sqlite3
import sql_funcs
 
sql_funcs.create_study_table("./sensorlab.db")

sql_funcs.create_study_entry("./sensorlab.db", 100, 102, PI="John", title="title", 
                       description="description", location_ids=["location1", "location2"], 
                       sensor_ids=["sensor1", "sensor2"], start_date="11.12.23")

print(sql_funcs.search_study("./sensorlab.db", 102))