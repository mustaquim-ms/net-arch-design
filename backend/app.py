# Placeholder for app.py


from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)


@app.route('/generate', methods=['POST'])
def generate_diagram():
    try:
        data = request.get_json()
        print("Received data:", data)

        if not isinstance(data, dict):
            return jsonify({'error': 'JSON must be an object with "devices" and "connections"'}), 400

        devices = data.get('devices', [])
        connections = data.get('connections', [])

        if not devices or not connections:
            return jsonify({'error': 'Missing "devices" or "connections" data'}), 400

        # ✅ Your diagram generation logic here (stubbed for now)
        return jsonify({
            'status': 'success',
            'device_count': len(devices),
            'connection_count': len(connections)
        })

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5050)
