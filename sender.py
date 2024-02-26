import paho.mqtt.client as mqtt
import json
import random
import time
import mqtt_funcs

# sender subscribes to sql/send_data channel
# receiver subscribes to sql/retrieve_data
# sender publishes to sql/retrieve_data channel as well as publishing its sensor data
# in receiver on_message function, receiver sees topic, gets data from sql
# receiver then publishes sql data to sql/send_data channel
# sender on_message prints out data

# TODO retrieve user data through log in (study, etc.) and send to receiver, which will then set its userdata to same?

# VARIABLES
mqtt_broker = "149.165.159.142"
mqtt_port = 1883
mqtt_topic_prefix = "test/topic/"
send_count = 0
total_send_count = 60

def main():
    global send_count

    a = 1

    client_userdata = {'a': a}

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=client_userdata)

    client.on_connect = mqtt_funcs.sender_on_connect
    client.on_message = mqtt_funcs.sender_on_message

    client.connect(mqtt_broker, mqtt_port, 60)

    # specifics for data search query
    sensor_data = {'sensor_id': 103} # teer sensor

    client.loop_start()

    while send_count < total_send_count:
        temperature_data = {
            "sensor1": round(random.uniform(20, 25), 2),
            "sensor2": round(random.uniform(18, 22), 2),
            "sensor3": round(random.uniform(22, 28), 2),
            "sensor4": round(random.uniform(25, 30), 2)
        }

        teer_data = {
            "barrierResistance": round(random.uniform(10000, 15000), 2)
        }

        print("Sending Temperature Data:", temperature_data)

        client.publish(mqtt_topic_prefix + 'sensor_data/temperature', json.dumps(temperature_data))

        print("Sending TEER Data:", teer_data)

        client.publish(mqtt_topic_prefix + 'evom_data/teer', json.dumps(teer_data))

        print("Retrieving Teer Data")

        client.publish(mqtt_topic_prefix + 'sql/retrieve_data', json.dumps(sensor_data))

        send_count += 1

        time.sleep(1)

    client.disconnect()
    client.loop_stop()

if __name__ == "__main__":
    main()

