import sqlite3

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



def create_study_table(database_file: str):

    connection = sqlite3.connect(database_file)
 
    # cursor object
    cursor = connection.cursor()
    
    if check_table(cursor, 'Study'):
        connection.commit() 
        connection.close()

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

    # Close the connection

    connection.commit()
    connection.close()

    return



# Creates study entry if it does not exist under given study_id, if study_id does exist, does nothing
def create_study_entry(database_file: str,
                 investigator_id: int, 
                 study_id: int, 
                 PI: str=None, 
                 title: str=None, 
                 description: str=None, 
                 location_ids: list=None, 
                 sensor_ids: list=None, 
                 start_date: str=None):
    
    connection = sqlite3.connect(database_file) 
    cursor = connection.cursor()

    if check_entry(cursor, 'Study', study_id):
        connection.commit() 
        connection.close()

        print(f"Study {study_id} already exists!")
        return
    
    study_query = f'''INSERT INTO Study (investigator_id, study_id, PI, title, 
    description, location_ids, sensor_ids, start_date) VALUES ({investigator_id}, 
    {study_id}, '{PI}', '{title}', '{description}', '{' '.join(str(x) for x in location_ids)}', 
    '{' '.join(str(x) for x in sensor_ids)}', '{start_date}');'''

    cursor.execute(study_query)

    connection.commit() 
    connection.close()

    return



def search_study(database_file: str,
                 study_id: int):
    
    connection = sqlite3.connect(database_file) 
    cursor = connection.cursor()

    if not check_entry(cursor, 'Study', study_id):
        connection.commit() 
        connection.close()

        print(f"Study {study_id} does not exist!")
        return
    
    entry_query = f'''SELECT * FROM Study WHERE study_id='{study_id}';'''

    study = list(cursor.execute(entry_query).fetchone())

    # convert location_id string to list
    study[5] = study[5].split()

    # convert sensor_id string to list
    study[6] = study[6].split()

    return study