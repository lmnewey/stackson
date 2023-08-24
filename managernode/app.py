from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# MQTT settings
MQTT_BROKER_HOST = "192.168.0.40"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_STATUS = "worker/+/status"  # Subscribe to status announcements from all nodes
MQTT_TOPIC_STATS = "worker/{}/stats"   # Subscribe to stats from specific nodes

# Simple in-memory data structure to store worker nodes
worker_nodes = []

# Callback when a message is received on the status topic
def on_status_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    status_data = json.loads(payload)
    
    node_id = status_data["node_id"]
    status = status_data["status"]

    # Update or add the node to the list
    for node in worker_nodes:
        if node["id"] == node_id:
            node["status"] = status
            break
    else:
        worker_nodes.append({"id": node_id, "status": status})

# Callback when a message is received on the stats topic
def on_stats_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    stats_data = json.loads(payload)
    
    node_id = message.topic.split("/")[1]  # Extract the node_id from the topic
    # Update the stats data for the corresponding node (you can handle this based on your data structure)
    # ...

# Setup MQTT client for status messages
status_client = mqtt.Client(client_id="status_listener")
status_client.on_message = on_status_message
status_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
status_client.subscribe(MQTT_TOPIC_STATUS)
status_client.loop_start()

# Setup MQTT client for stats messages
stats_client = mqtt.Client(client_id="stats_listener")
stats_client.on_message = on_stats_message
stats_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
stats_client.subscribe(MQTT_TOPIC_STATS.format("+"))  # Subscribe to stats from all nodes
stats_client.loop_start()

@app.route("/")
def index():
    return render_template("index.html", worker_nodes=worker_nodes)

if __name__ == "__main__":
    app.run(debug=True)
