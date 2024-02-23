import paho.mqtt.client as mqtt
import json
import sqlite3
import sql_funcs
import mqtt_funcs

# MQTT VARIABLES
mqtt_broker = "149.165.159.142"
mqtt_port = 1883
mqtt_topic_prefix = "test/topic/"

# SQL VARIABLES
db_path = "./your_database.db"
study_id = 101
location_id = 102
teer_id = 103
temp_id = 104

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql_funcs.create_data_table(cursor)

    conn.commit()

    # TODO integrate login
    # TODO get study info from login information right here

    #client_userdata = {'sql_cursor': cursor, 'study_id': study_id, 'teer_id': teer_id,
    #                   'location_id': location_id, 'temp_id': temp_id}
    
    client_userdata = {'sql_cursor': cursor, 'study_id': study_id, 'teer_id': teer_id,
                       'location_id': location_id, 'temp_id': temp_id}
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=client_userdata)
    client.on_connect = mqtt_funcs.receiver_on_connect
    client.on_message = mqtt_funcs.receiver_on_message

    client.connect(mqtt_broker, mqtt_port, 60)

    client.loop_forever()

if __name__ == "__main__":
    main()