# Placeholder for app.py

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import tempfile
import os
from diagram_generator import generate_network_diagram

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/')
def index():
    return jsonify({
        "message": "Network Diagram Generator API is running.",
        "endpoints": {
            "POST /generate": "Accepts network JSON and returns a network diagram image (PNG)."
        }
    })


@app.route('/generate', methods=['POST'])
def generate_diagram():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided."}), 400

        # Create a temporary file to save the diagram image
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmpfile.close()

        # Generate the network diagram
        generate_network_diagram(data, tmpfile.name)

        return send_file(tmpfile.name, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Optional cleanup: You could schedule temp file deletion if needed
        pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# import {useState} from 'react'
# import React
# import axios from 'axios'
# from diagram_generator import generate_network_diagram
# import tempfile
# from flask_cors import CORS
# from flask import Flask, request, send_file
# import matplotlib.pyplot as plt
# import networkx as nx
# import json


# def generate_network_diagram(data, output_file='network_diagram.png'):
#     G = nx.DiGraph()

#     # Define color by device type
#     color_map = {
#         'Router': '#FF5733',
#         'Switch': '#33C1FF',
#         'Firewall': '#C70039',
#         'Server': '#2ECC71',
#         'Client': '#F1C40F',
#         'Access Point': '#9B59B6'
#     }

#     node_colors = []
#     for device in data['devices']:
#         label = f"{device['name']}\n{device['ip']}"
#         G.add_node(label, layer=device.get('layer', 2))
#         node_colors.append(color_map.get(device['type'], '#BDC3C7'))

#     for link in data['connections']:
#         from_label = f"{link['from_name']}\n{link['from_ip']}"
#         to_label = f"{link['to_name']}\n{link['to_ip']}"
#         G.add_edge(from_label, to_label)

#     pos = nx.multipartite_layout(G, subset_key="layer")

#     plt.figure(figsize=(14, 8))
#     nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=3000,
#             font_size=10, font_weight='bold', edge_color='#7f8c8d')
#     plt.title("Auto-Generated Network Architecture Diagram")
#     plt.tight_layout()
#     plt.savefig(output_file)
#     plt.close()

# # Example Usage:
# # data = json.load(open('network_data.json'))
# # generate_network_diagram(data)


# # App.jsx (React Frontend)


# export default function App() {
#     const[theme, setTheme] = useState('light')
#     const[networkData, setNetworkData] = useState('')
#     const[image, setImage] = useState(null)

#     const toggleTheme = () = > setTheme(theme === 'light' ? 'dark': 'light')

#     const handleSubmit = async () = > {
#         try {
#             const response = await axios.post('http://localhost:5000/generate', JSON.parse(networkData), {
#                 responseType: 'blob',
#             })
#             const url = URL.createObjectURL(new Blob([response.data]))
#             setImage(url)
#         } catch(err) {
#             alert("Failed to generate diagram")
#         }
#     }

#     return (
#         < div className={`app-container ${theme}`} >
#         < button onClick={toggleTheme} > Switch to {theme === 'light' ? 'Dark': 'Light'} Mode < /button >
#         < textarea
#         placeholder="Paste JSON or CSV parsed JSON here"
#         value={networkData}
#         onChange={e= > setNetworkData(e.target.value)}
#         rows={15}
#         style={{width: '100%', marginTop: '1rem'}}
#         / >
#         < button onClick={handleSubmit} > Generate Diagram < /button >
#         {image & & < img src = {image} alt = "Network Diagram" style = {{marginTop: '1rem', maxWidth: '100%'}} / >}
#         < /div >
#     )
# }


# # Flask API (app.py)


# app = Flask(__name__)
# CORS(app)


# @app.route('/generate', methods=['POST'])
# def generate():
#     data = request.json
#     tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
#     generate_network_diagram(data, tmpfile.name)
#     return send_file(tmpfile.name, mimetype='image/png')


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
