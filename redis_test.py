import serial 
import redis_test 
import json  
 
REDIS_HOST = "redis-11142.c8.us-east-1-3.ec2.redns.redis-cloud.com" 
REDIS_PORT = 11142
REDIS_PASSWORD = "2uLfOFNlL6T8Gxxxz4WiI2LxhTLaECGS" 
 
r = redis_test.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, 
decode_responses=True) 
 
SERIAL_PORT = "COM10"   
BAUD_RATE = 115200 
 
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) 
 
print("Connected to Arduino! Reading gyroscope data...") 
 
try: 
    while True: 
        line = ser.readline().decode().strip() 
 
        if line: 
            try: 
                if line.startswith('{') and line.endswith('}'): 
                    gyro_data = json.loads(line)   
                else: 
                    data = line.replace("{", "").replace("}", "").replace('"', "").split(',') 
                    gyro_data = { 
                        "x": float(data[0].split(":")[-1]),   
                        "y": float(data[1].split(":")[-1]), 
                        "z": float(data[2].split(":")[-1]) 
                    } 
 
                r.set("gyro_data", json.dumps(gyro_data)) 
                print(f"Stored in Redis: {gyro_data}") 
 
            except (ValueError, IndexError, json.JSONDecodeError) as e: 
                print(f"Data format error: {e} | Received: {line}") 
 
except KeyboardInterrupt: 
    print("\nStopping script.") 
    ser.close() 