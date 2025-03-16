import paho.mqtt.client as mqtt 
import pymongo 
import json 
import datetime 
import ssl  # Secure MQTT

# MongoDB Connection
MONGO_URI = "mongodb+srv://Hardika:<db_password>@cluster0.oomed.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Change if using MongoDB Atlas
mongo_client = pymongo.MongoClient(MONGO_URI)  
db = mongo_client["DCT"] 
collection = db["5.2D"] 

# MQTT Connection Details
MQTT_BROKER = "339e799eb4894032aa9ec261b0d791c9.s1.eu.hivemq.cloud"  
MQTT_PORT = 8883  
MQTT_USERNAME = "Hardika"  
MQTT_PASSWORD = "Hardika1"  
MQTT_TOPIC = "gyro/data"  

# Callback when a message is received
def on_message(client, userdata, message):  
    try:
        payload = message.payload.decode("utf-8")  
        print(f"Received MQTT message: {payload}")  

        # Parse JSON safely
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            print("Error: Received invalid JSON data!")
            return
        
        # Add timestamp
        data["timestamp"] = datetime.datetime.utcnow().isoformat()

        # Insert into MongoDB
        result = collection.insert_one(data)  
        print(f"✅ Inserted into MongoDB with ID: {result.inserted_id}")  

    except Exception as e:  
        print(f"Error inserting into MongoDB: {e}")  

# MQTT Client Setup
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  
mqtt_client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)  
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)  
mqtt_client.on_message = on_message  

# Connect and Subscribe
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)  
mqtt_client.subscribe(MQTT_TOPIC)  

print(f"📡 Subscribed to {MQTT_TOPIC}, waiting for messages...")  

# Start MQTT loop
mqtt_client.loop_forever()  
