import serial 
import paho.mqtt.client as mqtt 
import json 
import csv 
import time 
 
# Serial Port Configuration 
SERIAL_PORT = "COM16"  # Change based on your setup 
BAUD_RATE = 115200 
 
# MQTT Broker Details 
MQTT_BROKER = "339e799eb4894032aa9ec261b0d791c9.s1.eu.hivemq.cloud" 
MQTT_PORT = 8883 
MQTT_TOPIC = "gyro/data" 
 
# Your HiveMQ Cloud Credentials 
MQTT_USERNAME = "Hardika" 
MQTT_PASSWORD = "Hardika1" 
 
# Initialize Serial Connection 
ser = serial.Serial(SERIAL_PORT, BAUD_RATE) 
 
# Initialize MQTT Client with Authentication 
client = mqtt.Client() 
client.tls_set()  # Enable TLS (secure connection) 
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)  # Set username and password 
client.connect(MQTT_BROKER, MQTT_PORT, 60)  # Timeout of 60 seconds 
 
# Open CSV File for Data Logging 
csv_filename = "gyroscope_data.csv" 
with open(csv_filename, mode="w", newline="") as file: 
    writer = csv.writer(file) 
    writer.writerow(["timestamp", "x", "y", "z"])  # Column headers 
 
    print("Listening for Serial Data and Saving to CSV...") 
 
    while True: 
        try: 
            line = ser.readline().decode("utf-8").strip()   
            data = json.loads(line)   
            print("Received:", data) 
 
            # Get current timestamp 
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S") 
 
            # Write data to CSV 
            writer.writerow([timestamp, data["x"], data["y"], data["z"]]) 
 
            # Publish to MQTT 
            client.publish(MQTT_TOPIC, json.dumps(data)) 
            print("Published to MQTT:", data) 
 
        except Exception as e: 
            print("Error:", e) 