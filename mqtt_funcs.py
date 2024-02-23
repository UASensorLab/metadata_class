import sql_funcs
import json
import paho.mqtt.client as mqtt
import sqlite3

# TODO retrieving data from SQL funcs
# TODO on disconnect, commit and close sql for both sender and receiver
# TODO sending functions, instead of client.publish, have function for each

# VARIABLES
mqtt_topic_prefix = "test/topic/"

# SENDER FUNCS

def sender_on_connect(client: mqtt.Client,
                      userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))

    client.subscribe(mqtt_topic_prefix + 'sql/send_data')

def sender_on_message(client: mqtt.Client,
                        userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")

    try:
        data = json.loads(msg.payload)

        if msg.topic == mqtt_topic_prefix + 'sql/send_data':
            print(f'\nretreived from server: {data}\n')

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# RECEIVER FUNCS

# receiver handler for temp data
def handle_temperature_data(client: mqtt.Client, data, userdata):
    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['temp_id'], 
                                userdata['study_id'], userdata['location_id'], data['sensor1'])
    
    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['temp_id'], 
                                userdata['study_id'], userdata['location_id'], data['sensor2'])

    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['temp_id'], 
                                userdata['study_id'], userdata['location_id'], data['sensor3'])
    
    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['temp_id'], 
                                userdata['study_id'], userdata['location_id'], data['sensor4'])

# receiver handler for teer data
def handle_teer_data(client: mqtt.Client, data, userdata):
    sql_funcs.create_data_entry(userdata['sql_cursor'], userdata['teer_id'], 
                                userdata['study_id'], userdata['location_id'], data['barrierResistance'])

# TODO expand
# receiver handler for sql data request
def retreive_data(client: mqtt.Client, data, userdata):

    sqlretrieved = sql_funcs.search_data(userdata['sql_cursor'], data['sensor_id'], userdata['study_id'])

    client.publish(mqtt_topic_prefix + 'sql/send_data', json.dumps(sqlretrieved))

# relates topic receiver gets to function to run
topic_func_dict = {'test/topic/sensor_data/temperature': handle_temperature_data,
                   'test/topic/evom_data/teer': handle_teer_data,
                   'test/topic/sql/retrieve_data': retreive_data}

# receiver connection initialization
def receiver_on_connect(client: mqtt.Client, 
                        userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))

    #for topic in topic_func_dict:
    #    client.subscribe(mqtt_topic_prefix + topic)
    
    client.subscribe(mqtt_topic_prefix + 'sensor_data/temperature')
    client.subscribe(mqtt_topic_prefix + 'evom_data/teer')
    client.subscribe(mqtt_topic_prefix + 'sql/retrieve_data')

# TODO
# receiver creating funcs
def create_table():
    pass

# receiver all data handler
def receiver_on_message(client: mqtt.Client,
                        userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")

    try:
        data = json.loads(msg.payload)

        # run function according to topic
        topic_func_dict[f'{msg.topic}'](client, data, userdata)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


