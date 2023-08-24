from flask import Flask, render_template
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# MQTT settings
MQTT_BROKER_HOST = "192.168.0.40"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_PREFIX = "worker/"  # Subscribe to all worker topics

# Simple in-memory data structure to store worker nodes
worker_nodes = []

# Callback when a message is received
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    topic_parts = message.topic.split("/")
    if len(topic_parts) == 3 and topic_parts[0] == "worker":
        node_id = topic_parts[1]
        if topic_parts[2] == "status":
            update_worker_status(node_id, payload)
        elif topic_parts[2] == "stats":
            update_worker_stats(node_id, payload)

# Update or add the node to the list
def update_worker_status(node_id, status):
    for node in worker_nodes:
        if node["id"] == node_id:
            node["status"] = status
            break
    else:
        worker_nodes.append({"id": node_id, "status": status})

# Update worker stats (to be implemented based on your data structure)
def update_worker_stats(node_id, stats_payload):
    pass

# Setup MQTT client
mqtt_client = mqtt.Client(client_id="worker_listener")
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC_PREFIX + "+/status")
mqtt_client.subscribe(MQTT_TOPIC_PREFIX + "+/stats")
mqtt_client.loop_start()

@app.route("/")
def index():
    return render_template("index.html", worker_nodes=worker_nodes)

if __name__ == "__main__":
    app.run(debug=True)