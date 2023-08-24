# python_code_data = {
#     "type": "python",
#     "data": {
#         "code": "print('Hello, world!')"
#     }
# }

# command_data = {
#     "type": "command",
#     "data": {
#         "command": "ls",
#         "args": ["host":"","username":"","password":"","command":"",],
#         "working_dir": null
#     }
# }
# deploy_data = {
#     "type": "deploy",
#     "data": {
#         "commands": "ls",
#         "args": ["-l", "-a"],
#         "working_dir": null
#     }
# }

import os
import subprocess
import psutil
import json
import uuid
import socket
import netifaces
import paramiko
import paho.mqtt.client as mqtt
from pynvml import nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetName, nvmlDeviceGetUtilizationRates

GPU_enabled = True

# Unique ID for this instance
CLIENT_ID = str(uuid.uuid4())

#CLIENT_ID = str(uuid.uuid4()) # generate the unique id
# MQTT settings
MQTT_BROKER_HOST = "192.168.0.40"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_REGISTER = "worker/register"
MQTT_TOPIC_COMMANDS = "worker/"+CLIENT_ID +"/commands"
MQTT_TOPIC_STATS = "worker/"+CLIENT_ID + "/stats"
MQTT_TOPIC_RESULTS = "worker/"+CLIENT_ID +"/results"

MAX_STORED_RESULTS = 10
stored_results = []

# Callback when a message is received
# def on_message(client, userdata, message):
#     try:
#         command_data = json.loads(message.payload.decode("utf-8"))
#         command = command_data.get("command")
#         args = command_data.get("args")
#         working_dir = command_data.get("working_dir")
        
#         print(f"Received command: {command}")
        
#         if working_dir:
#             os.chdir(working_dir)
        
#         result = subprocess.check_output([command] + args, shell=True, stderr=subprocess.STDOUT, text=True)
#         print(f"Command output:\n{result}")
        
#         result_data = {"output": result}
#         client.publish(MQTT_TOPIC_RESULTS, json.dumps(result_data))
#     except subprocess.CalledProcessError as e:
#         error_msg = f"Error running command: {e.output}"
#         print(error_msg)
#         error_data = {"error": error_msg}
#         client.publish(MQTT_TOPIC_RESULTS, json.dumps(error_data))
# Load the unique ID from a file if it exists


#def deployfiletransmit():
    # echo "import paho.mqtt.client as mqtt" > mqtt_writer.py
    # echo "" >> mqtt_writer.py
    # echo "MQTT_BROKER_HOST = \"192.168.0.40\"" >> mqtt_writer.py
    # echo "MQTT_BROKER_PORT = 1883" >> mqtt_writer.py
    # echo "" >> mqtt_writer.py
    # echo "CLIENT_ID = \"my_unique_id\"" >> mqtt_writer.py
    # echo "" >> mqtt_writer.py
    # echo "def on_message(client, userdata, message):" >> mqtt_writer.py
    # echo "    payload = message.payload.decode(\"utf-8\")" >> mqtt_writer.py
    # echo "    with open(\"message_log.txt\", \"a\") as file:" >> mqtt_writer.py
    # echo "        file.write(payload + \"\\n\")" >> mqtt_writer.py
    # echo "    print(f\"Received and written: {payload}\")" >> mqtt_writer.py
    # echo "" >> mqtt_writer.py
    # echo "client = mqtt.Client(client_id=CLIENT_ID)" >> mqtt_writer.py
    # echo "client.on_message = on_message" >> mqtt_writer.py
    # echo "" >> mqtt_writer.py
    # echo "client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)" >> mqtt_writer.py
    # echo "client.subscribe(f\"topic/{CLIENT_ID}\")" >> mqtt_writer.py
    # echo "" >> mqtt_writer.py
    # echo "client.loop_start()" >> mqtt_writer.py
    # echo "" >> mqtt_writer.py
    # echo "try:" >> mqtt_writer.py
    # echo "    while True:" >> mqtt_writer.py
    # echo "        pass" >> mqtt_writer.py
    # echo "except KeyboardInterrupt:" >> mqtt_writer.py
    # echo "    pass" >> mqtt_writer.py
    # echo "" >> mqtt_writer.py
    # echo "client.loop_stop()" >> mqtt_writer.py
    # echo "client.disconnect()" >> mqtt_writer.py


def create_requirements_file(package_list, file_path="requirements.txt"):
    with open(file_path, "w") as file:
        for package in package_list:
            file.write(package + "\n")
    print(f"Requirements file '{file_path}' created.")

def deploy_agent(message):
    #cCode = message.get("code")
    #hHost = message.get("host")
    #print(f"received message with data {cCode }")
    #print(f"received message with data {hHost }")
    # SSH connection details
    host = message.get("host")
    port = 22
    username = message.get("username")
    password = message.get("password")
    commands = message.get("commands")#"python agent_script.py"  # Replace with actual agent script
    
    # Create an SSH client instance
    sshclient = paramiko.SSHClient()
    
    # Automatically add the server's host key (this is not secure for production use)
    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Connect to the remote host
    print(f"received message with data {host }")
    print(f"received message with data {port }")
    print(f"received message with data {username }")
    print(f"received message with data {password}")
    hostuser = username+"@"+host
    try:
        sshclient.connect(host, username=username, password=password, disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})
        
    except Exception as e:
        print(f"An error occurred: {e}")

    # Run the command
    for command in commands:
            stdin, stdout, stderr = sshclient.exec_command(command)
            command_output = stdout.read().decode("utf-8")
            print(f"Command: {command}\nOutput:\n{command_output}")
            results_with_history = {"current_result": command, "history": stored_results}
            client.publish(MQTT_TOPIC_RESULTS, json.dumps(results_with_history))
            # You can write the command output to a file or send it via MQTT if needed    
    #deployfiletransmit()
    # Print the command output
    print("Command output:")
    print(stdout.read().decode())
    
    # Close the SSH connection
    sshclient.close()
    
    # List of packages used in the script
    packages = ["paramiko"]
    
    # Create a requirements.txt file
    create_requirements_file(packages)

def get_network_info():
    network_info = []

    # Get host name
    hostname = socket.gethostname()

    # Get network interfaces
    interfaces = netifaces.interfaces()
    
    for interface in interfaces:
        interface_info = {"interface": interface}
        
        # Get IP addresses
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ip_address = addresses[netifaces.AF_INET][0]['addr']
            interface_info["ip_address"] = ip_address
        
        # Get MAC address
        if netifaces.AF_LINK in addresses:
            mac_address = addresses[netifaces.AF_LINK][0]['addr']
            interface_info["mac_address"] = mac_address
        
        network_info.append(interface_info)
    
    return {
        "hostname": hostname,
        "network_interfaces": network_info
    }

def load_client_id():
    try:
        with open("client_id.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Save the unique ID to a file
def save_client_id(client_id):
    with open("client_id.txt", "w") as file:
        file.write(client_id)

def on_message(client, userdata, message):
    global CLIENT_ID
    
    try:
        message_data = json.loads(message.payload.decode("utf-8"))
        if message_data.get("client_id_in_use"):
            # If the client ID is in use, generate a new one
            CLIENT_ID = str(uuid.uuid4())
            print(f"Generated new client ID: {CLIENT_ID}")
            register(client)  # Re-register with the new ID            
            save_client_id(CLIENT_ID)
        else:
            print(f"Client ID '{CLIENT_ID}' is registered successfully.")
            save_client_id(CLIENT_ID)
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        message_data = json.loads(message.payload.decode("utf-8"))
        message_type = message_data.get("type")
        message_data = message_data.get("data")
        error_msg = ""
        result_data = {"output": error_msg, "success": False}
        
        print(f" {message_type}")
        if message_type == "deploy":  
            print(f"Received command: {message_data}")          
            deploy_agent(message_data)
            result_data = {"output": error_msg, "success": False}
        
        elif message_type == "command":
            command = message_data.get("command")
            args = message_data.get("args")
            working_dir = message_data.get("working_dir")
            if working_dir is None:
                working_dir = "/tmp"

            print(f"Received command: {command}")
        
            if working_dir:
                os.chdir(working_dir)
        
            try:
                result = subprocess.check_output([command] + args, shell=True, stderr=subprocess.STDOUT, text=True)
                print(f"Command output:\n{result}")
                result_data = {"output": result, "success": True}
                stored_results.append(result_data)
                if len(stored_results) > MAX_STORED_RESULTS:
                    stored_results.pop(0)  # Remove oldest result if exceeding limit
            except subprocess.CalledProcessError as e:
                error_msg = f"Error running command: {e.output}"
                print(error_msg)
                result_data = {"output": error_msg, "success": False}
                stored_results.append(result_data)
                if len(stored_results) > MAX_STORED_RESULTS:
                    stored_results.pop(0)  # Remove oldest result if exceeding limit
            # command_data = json.loads(message.payload.decode("utf-8"))
            # command = command_data.get("command")
            # args = command_data.get("args")
            # working_dir = command_data.get("working_dir")
            
               # Set default working directory if not specified
        elif message_type == "python":
            python_code = message_data.get("code")
            exec(python_code)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
        # Publish the results including the stored_results array
    results_with_history = {"current_result": result_data, "history": stored_results}
    client.publish(MQTT_TOPIC_RESULTS, json.dumps(results_with_history))
    
    

def send_stats(client):
    global GPU_enabled
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    network_info = get_network_info()
    #print(json.dumps(network_info, indent=4))
    
    gpu_stats = []
    try:
        if GPU_enabled:
            nvmlInit()
            device_count = nvmlDeviceGetCount()
            for i in range(device_count):
                handle = nvmlDeviceGetHandleByIndex(i)
                gpu_name = nvmlDeviceGetName(handle).decode("utf-8")
                utilization = nvmlDeviceGetUtilizationRates(handle)
                gpu_stats.append({"gpu": gpu_name, "utilization": utilization.gpu})
    # except NVMLError_LibraryNotFound:
    #     print("NVIDIA GPU library not found. Skipping GPU stats.")
    except Exception as e:
        print(f"An error occurred while gathering GPU stats: {e}")
        GPU_enabled = False
    
    stats_data = {
        "client_ID" : CLIENT_ID,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "gpu_stats": gpu_stats,
        "network_info": network_info
    }
    
    client.publish(MQTT_TOPIC_STATS, json.dumps(stats_data))

def register(client):
    global CLIENT_ID
    register_data = {"client_id": CLIENT_ID}
    client.publish(MQTT_TOPIC_REGISTER, json.dumps(register_data))

# Use the loaded ID or generate a new one
loaded_client_id = load_client_id()
if loaded_client_id:
    CLIENT_ID = loaded_client_id
#else:
    #leave as it is
    #CLIENT_ID = str(uuid.uuid4())
    #save_client_id(CLIENT_ID)

# Setup MQTT client
client = mqtt.Client(client_id=CLIENT_ID)
client.on_message = on_message

# Connect to the broker and subscribe to the relevant topics
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
client.subscribe(MQTT_TOPIC_COMMANDS)

# Start the MQTT loop
client.loop_start()

# Register the client
register(client)

# Keep sending stats as keep-alive
GPU_enabled = True
try:
    while True:
        send_stats(client)
except KeyboardInterrupt:
    pass

# Disconnect from the broker
client.loop_stop()
client.disconnect()