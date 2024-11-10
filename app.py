import collections
from flask import Flask, request, jsonify
from datetime import datetime
import subprocess

app = Flask(__name__)

tokenMap = collections.defaultdict(set)

@app.route('/dcv', methods=['POST'])
def recordIP():
    timestamp = datetime.utcnow().isoformat()
    print("request received")

    # Retrieve JSON data from the request body
    data = request.get_json()
    print("data received")
    if not data:
        return jsonify({'error': 'Request body must contain JSON data'}), 400

    token = data.get('token')
    print("token received")
    if not token:
        return jsonify({'error': 'Token parameter is required'}), 400
    # if not data_center:
    #     return jsonify({'error': 'Data-center parameter is required'}), 400

    ip_address = request.remote_addr
    print("IP received")
    # Create an entry with the required structure
    entry = {
        "IP_ADDRESS": ip_address,
        "TIMESTAMP": timestamp,
        # "DATA_CENTER": data_center
    }

    # Add the entry to the tokenMap
    tokenMap[token].add(entry)
    print("logging received")

    # Optionally, return a response
    return jsonify({'message': 'Token, IP, and data center logged successfully'}), 200


@app.route('/getIPs', methods=['GET'])
def get_ips():
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Token parameter is required'}), 400
    ip_list = [entry["IP_ADDRESS"] for entry in tokenMap[token]]
    #ip_list = list(tokenMap[token])
    return jsonify({'ip_addresses': ip_list})


# @app.route('/getIPs', methods=['GET'])
# Currently not using this method
# def get_ips_deprecated():
#     token = request.args.get('token')
#     if not token:
#         return jsonify({'error': 'Token parameter is required'}), 400
#
#     try:
#         # Use grep to search for lines containing the token
#         result = subprocess.check_output(['grep', '-F', token, LOG_FILE_PATH], text=True)
#         # Split the result into individual lines
#         lines = result.strip().split('\n')
#         # Extract IP addresses from the lines
#         ip_addresses = []
#         for line in lines:
#             # Assuming the IP address is the first element in each line
#             ip = line.split()[0]
#             ip_addresses.append(ip)
#         # Remove duplicates
#         ip_addresses = list(set(ip_addresses))
#         return jsonify({'ip_addresses': ip_addresses})
#     except subprocess.CalledProcessError as e:
#         # grep returns exit code 1 if no matches are found
#         if e.returncode == 1:
#             return jsonify({'ip_addresses': []})
#         else:
#             return jsonify({'error': 'An error occurred while processing the logs'}), 500
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/clearLogs', methods=['POST'])
# Currently not using this method
# def clear_logs():
#     try:
#         # Clear the log file
#         open(LOG_FILE_PATH, 'w').close()
#         # Alternatively, you can truncate the file using shell command
#         # subprocess.run(['truncate', '-s', '0', LOG_FILE_PATH], check=True)
#         return jsonify({'message': 'Apache logs have been cleared'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)
