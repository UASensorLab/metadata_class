import sqlite3

# creates whole table for studies within SQL database
def create_study_table(cursor: sqlite3.Cursor):

    if check_table(cursor, 'Study'):
        print(f"Study table already exists!")
        return

    # Creating table
    table = """ CREATE TABLE Study (
                investigator_id INT NOT NULL,
                study_id INT NOT NULL,
                PI TEXT,
                title TEXT,
                description TEXT,
                location_ids TEXT,
                sensor_ids TEXT,
                start_date TEXT); """

    cursor.execute(table)

    return



# creates whole table for locations within SQL database
def create_location_table(cursor: sqlite3.Cursor):

    if check_table(cursor, 'Location'):
        print(f"Location table already exists!")
        return

    # Creating table
    table = """ CREATE TABLE Location (
                location_id INT NOT NULL,
                description TEXT); """

    cursor.execute(table)

    return



# creates whole table for sensors within SQL database
def create_sensors_table(cursor: sqlite3.Cursor):

    if check_table(cursor, 'Sensors'):
        print(f"Sensors table already exists!")
        return

    # Creating table
    table = """ CREATE TABLE Sensors (
                sensor_id INT NOT NULL,
                unit TEXT,
                description TEXT,
                sampling INT); """

    cursor.execute(table)

    return



# creates whole table for data within SQL database
def create_data_table(cursor: sqlite3.Cursor):

    if check_table(cursor, 'Data'):
        print(f"Data table already exists!")
        return

    # Creating table
    table = """ CREATE TABLE Data (
                sensor_id INT NOT NULL,
                study_id INT NOT NULL,
                location_id INT NOT NULL,
                value TEXT NOT NULL,
                timestamp TEXT); """

    cursor.execute(table)

    return



# returns True if table exists, False if not
def check_table(cursor: sqlite3.Cursor, table_name: str):

    tablequery = f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';'''

    table_list = cursor.execute(tablequery).fetchall()

    return(table_list != []) 



# dict to be used by check_entry()
id_type_dict = {'Study': 'study_id',
                'Location': 'location_id',
                'Sensors': 'sensor_id'}

# returns True if entry exists, False if not
def check_entry(cursor: sqlite3.Cursor, 
                table_name: str, 
                entry_id: int):

    id_type = id_type_dict[table_name]

    entry_query = f'''SELECT {id_type} FROM {table_name} WHERE {id_type}='{entry_id}';'''

    entry = cursor.execute(entry_query).fetchall()

    return(entry != [])



# check function specifically for data entry, returns True if data exists, False if not
def check_data(cursor: sqlite3.Cursor,
               entry_id: int,
               id_type: str):
    pass

    data_query = f'''SELECT {id_type} FROM Data WHERE {id_type}='{entry_id}';'''

    data = cursor.execute(data_query).fetchall()

    return(data != [])



# Creates study entry if it does not exist under given study_id, if study_id does exist, does nothing
def create_study_entry(cursor: sqlite3.Cursor,
                 investigator_id: int, 
                 study_id: int, 
                 PI: str=None, 
                 title: str=None, 
                 description: str=None, 
                 location_ids: list=None, 
                 sensor_ids: list=None, 
                 start_date: str=None):

    if check_entry(cursor, 'Study', study_id):
        print(f"Study {study_id} already exists!")
        return
    
    study_query = f'''INSERT INTO Study (investigator_id, study_id, PI, title, 
    description, location_ids, sensor_ids, start_date) VALUES ({investigator_id}, 
    {study_id}, '{PI}', '{title}', '{description}', '{' '.join(str(x) for x in location_ids)}', 
    '{' '.join(str(x) for x in sensor_ids)}', '{start_date}');'''

    cursor.execute(study_query)

    return



# Creates location entry if it does not exist under given location_id, if location_id does exist, does nothing
def create_location_entry(cursor: sqlite3.Cursor,
                 location_id: int, 
                 description: str=None):

    if check_entry(cursor, 'Location', location_id):
        print(f"Location {location_id} already exists!")
        return
    
    location_query = f'''INSERT INTO Location (location_id, description) VALUES ({location_id}, 
    '{description}');'''

    cursor.execute(location_query)

    return



# Creates sensors entry if it does not exist under given sensor_id, if sensor_id does exist, does nothing
def create_sensors_entry(cursor: sqlite3.Cursor,
                 sensor_id: int, 
                 unit: str=None,
                 description: str=None,
                 sampling: int=None):

    if check_entry(cursor, 'Sensors', sensor_id):
        print(f"Sensor {sensor_id} already exists!")
        return
    
    sensor_query = f'''INSERT INTO Sensors (sensor_id, unit, 
    description, sampling) VALUES ({sensor_id}, '{unit}',
    '{description}', {sampling});'''

    cursor.execute(sensor_query)

    return



# Creates data entry
def create_data_entry(cursor: sqlite3.Cursor,
                 sensor_id: int, 
                 study_id: int,
                 location_id: int,
                 value: float,
                 timestamp: str=None):

    data_query = f'''INSERT INTO Data (sensor_id, 
    study_id, location_id, value, timestamp) 
    VALUES ({sensor_id}, {study_id}, {location_id},
    {str(value)}, '{timestamp}');'''

    cursor.execute(data_query)

    return



# returns all details of study as a list
def search_study(cursor: sqlite3.Cursor,
                 study_id: int):
    
    if not check_entry(cursor, 'Study', study_id):
        print(f"Study {study_id} does not exist!")
        return
    
    entry_query = f'''SELECT * FROM Study WHERE study_id='{study_id}';'''

    study = list(cursor.execute(entry_query).fetchone())

    # convert location_id string to list
    study[5] = study[5].split()

    # convert sensor_id string to list
    study[6] = study[6].split()

    return study

# returns all details of data as a list
# handles variable inputs as queries
def search_data(cursor: sqlite3.Cursor,
                sensor_id: int, 
                study_id: int,
                location_id: int=None,
                value: float=None,
                timestamp: str=None):
    
    entry_query = f'''SELECT * 
    FROM Data 
    WHERE study_id='{study_id}'
    AND sensor_id='{sensor_id}'
    AND (location_id IS NULL OR location_id = '{location_id}')
    AND (value IS NULL OR value = '{str(value)}')
    AND (timestamp IS NULL OR timestamp = '{timestamp}');'''

    data = list(cursor.execute(entry_query).fetchall())

    # convert string values back into floats
    for dp in data:
        dp = list(dp)
        dp[3] = float(dp[3])

    return data