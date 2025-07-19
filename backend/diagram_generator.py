# # Placeholder for diagram_generator.py

# # diagram_generator.py

# diagram_generator.py (enhanced)
# backend/diagram_generator.py

import io
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

COLOR_MAP = {
    "router": "red", "switch": "blue", "server": "green", "firewall": "orange",
    "pc": "gray", "printer": "purple", "ipphone": "cyan", "cctv": "black"
}
LAYER_POS = {"L1": 0, "L2": 1, "L3": 2}


def build_graph(devices, connections):
    G = nx.DiGraph()
    pos = {}
    labels = {}

    for dev in devices:
        name = dev["name"]
        dtype = dev["type"].lower()
        layer = dev.get("layer", "L2")
        y = LAYER_POS.get(layer.upper(), 1)
        x = hash(name) % 10

        G.add_node(name, color=COLOR_MAP.get(dtype, "gray"))
        pos[name] = (x, y)
        labels[name] = name

    for conn in connections:
        G.add_edge(conn["from"], conn["to"])

    return G, pos, labels


@app.route("/generate-diagram", methods=["POST"])
def generate():
    try:
        if "devices" in request.files and "connections" in request.files:
            devices_df = pd.read_csv(request.files["devices"])
            connections_df = pd.read_csv(request.files["connections"])
            devices = devices_df.to_dict(orient="records")
            connections = connections_df.to_dict(orient="records")
        else:
            return jsonify({"error": "Both 'devices' and 'connections' files required."}), 400
            img_io = generate_network_diagram(devices, connections)
            return send_file(img_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def generate_network_diagram(devices, connections):
    G, pos, labels = build_graph(devices, connections)
    node_colors = [G.nodes[n]["color"] for n in G.nodes]

    plt.figure(figsize=(12, 6))
    nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors,
            node_size=1000, font_size=10, edge_color="gray", font_weight="bold")
    plt.title("Network Diagram")
    plt.axis("off")

    img_io = io.BytesIO()
    plt.savefig(img_io, format="png", bbox_inches="tight")
    img_io.seek(0)
    plt.close()
    return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)


# import networkx as nx
# import matplotlib.pyplot as plt

# # Device type color palette
# DEVICE_COLORS = {
#     'Router': '#FF6B6B',
#     'Switch': '#4ECDC4',
#     'Firewall': '#F7B801',
#     'Server': '#1A535C',
#     'PC': '#5C5470',
#     'Printer': '#9C27B0',
#     'IPPhone': '#FF8A65',
#     'Camera': '#90CAF9',
#     'AccessPoint': '#81C784',
#     'Unknown': '#B0BEC5'
# }


# def generate_network_diagram(data, output_path, layer='L2'):
#     """
#     Generate a network topology diagram.

#     Args:
#         data (dict): Device list with connections.
#         output_path (str): Path to save the diagram image.
#         layer (str): 'L2' or 'L3' view selection.
#     """
#     G = nx.Graph()

#     # Add devices and edges
#     for device in data['devices']:
#         G.add_node(
#             device['name'],
#             device_type=device.get('type', 'Unknown')
#         )

#     for connection in data['connections']:
#         src = connection['source']
#         dst = connection['target']
#         G.add_edge(src, dst)

#     # Apply positions - spring layout for visual clarity
#     pos = nx.spring_layout(G, seed=42)

#     # Collect colors based on device type
#     node_colors = []
#     for node in G.nodes(data=True):
#         dtype = node[1].get('device_type', 'Unknown')
#         node_colors.append(DEVICE_COLORS.get(dtype, DEVICE_COLORS['Unknown']))

#     # Layer separation - optional (simple grouping)
#     if layer == 'L2':
#         title = "Layer 2 (Data Link Layer) View"
#     elif layer == 'L3':
#         title = "Layer 3 (Network Layer) View"
#     else:
#         title = "Network Diagram"

#     plt.figure(figsize=(12, 8))
#     nx.draw(
#         G,
#         pos,
#         with_labels=True,
#         node_color=node_colors,
#         node_size=1500,
#         font_size=10,
#         font_color='white',
#         edge_color='#BBBBBB',
#         linewidths=2
#     )
#     plt.title(title)
#     plt.axis('off')
#     plt.tight_layout()
#     plt.savefig(output_path)
#     plt.close()


# # Example Test
# if __name__ == "__main__":
#     test_data = {
#         "nodes": [
#             {"id": "R1", "label": "Main Router", "type": "Router"},
#             {"id": "S1", "label": "Core Switch", "type": "Switch"},
#             {"id": "FW1", "label": "Firewall", "type": "Firewall"},
#             {"id": "SRV1", "label": "App Server", "type": "Server"},
#             {"id": "C1", "label": "Client PC", "type": "Client"},
#             {"id": "AP1", "label": "WiFi AP", "type": "Access Point"},
#             {"id": "CL1", "label": "Cloud ISP", "type": "Cloud"}
#         ],
#         "edges": [
#             {"source": "CL1", "target": "R1", "connection": "WAN"},
#             {"source": "R1", "target": "FW1", "connection": "Trunk"},
#             {"source": "FW1", "target": "S1", "connection": "VLAN 10"},
#             {"source": "S1", "target": "SRV1", "connection": "LAN"},
#             {"source": "S1", "target": "C1", "connection": "LAN"},
#             {"source": "S1", "target": "AP1", "connection": "LAN"}
#         ]
#     }
#     generate_diagram(test_data)
