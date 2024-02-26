import sql_funcs
import json
import paho.mqtt.client as mqtt

# TODO on disconnect, commit and close sql for both sender and receiver?

# MQTT Topics, Functions, and Messages

# Topic: 'test/topic/sensor_data/temperature' 
# Function: handle_temperature_data()
# Message: dict {'sensor1': int, 'sensor2': int, sensor3': int, 'sensor4': int}

# Topic: 'test/topic/evom_data/teer'
# Function: handle_teer_data()
# Message: dict {'barrierResistance': int}

# Topic: 'test/topic/sql/retrieve_data'
# Function: retreive_data()
# Message: dict {'sensor_id': int, 'value': int/float, 'timestamp': str}

# Topic: 'test/topic/sql/create_table'
# Function: create_table()
# Message: dict {'tableType': str (Data or Location or Study or Sensors)}


# VARIABLES
mqtt_topic_prefix = "test/topic/"

# SENDER FUNCS

def sender_on_connect(client: mqtt.Client,
                      userdata: dict, flags, rc, properties):
    print("Connected with result code "+str(rc))

    client.subscribe(mqtt_topic_prefix + 'sql/send_data')



def sender_on_message(client: mqtt.Client,
                        userdata, msg):
    #print(f"Received message on topic {msg.topic}: {msg.payload}")

    try:
        data = json.loads(msg.payload)

        if msg.topic == mqtt_topic_prefix + 'sql/send_data':
            print(f'\nretreived from server: {data}\n')

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")



# RECEIVER FUNCS

# receiver handler for temp data
def handle_temperature_data(client: mqtt.Client, data, userdata: dict):
    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['temp_id'], 
                                userdata['study_id'], userdata['location_id'], data['sensor1'])
    
    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['temp_id'], 
                                userdata['study_id'], userdata['location_id'], data['sensor2'])

    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['temp_id'], 
                                userdata['study_id'], userdata['location_id'], data['sensor3'])
    
    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['temp_id'], 
                                userdata['study_id'], userdata['location_id'], data['sensor4'])



# receiver handler for teer data
def handle_teer_data(client: mqtt.Client, data, userdata: dict):
    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['teer_id'], 
                                userdata['study_id'], userdata['location_id'], data['barrierResistance'])



# receiver handler for sql data request
def retreive_data(client: mqtt.Client, data, userdata: dict):

    sqlretrieved = sql_funcs.search_data(userdata['sql_cursor'], data['sensor_id'], userdata['study_id'],
                                         userdata['location_id'])

    client.publish(mqtt_topic_prefix + 'sql/send_data', json.dumps(sqlretrieved))



table_func_dict = {'Study': sql_funcs.create_study_table,
                   'Location': sql_funcs.create_location_table,
                   'Data': sql_funcs.create_data_table,
                   'Sensors': sql_funcs.create_sensors_table}

# receiver creating table functions
def create_table(client: mqtt.Client, data, userdata: dict):

    table_func_dict[f'{data}'](userdata['sql_cursor'])



# relates topic receiver gets to function to run
topic_func_dict = {'test/topic/sensor_data/temperature': handle_temperature_data,
                   'test/topic/evom_data/teer': handle_teer_data,
                   'test/topic/sql/retrieve_data': retreive_data,
                   'test/topic/sql/create_table': create_table}

# receiver connection initialization
def receiver_on_connect(client: mqtt.Client, 
                        userdata: dict, flags, rc, properties):
    print("Connected with result code "+str(rc))

    for topic in topic_func_dict.keys():
        client.subscribe(topic)



# receiver all data handler
def receiver_on_message(client: mqtt.Client,
                        userdata: dict, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")

    try:
        data = json.loads(msg.payload)

        # run function according to topic
        topic_func_dict[f'{msg.topic}'](client, data, userdata)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


