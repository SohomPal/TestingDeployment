from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Define the path to your Apache access log file
LOG_FILE_PATH = '/var/log/apache2/access.log'  # Adjust this path if necessary

@app.route('/getIPs', methods=['GET'])
def get_ips():
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Token parameter is required'}), 400

    try:
        # Use grep to search for lines containing the token
        result = subprocess.check_output(['grep', '-F', token, LOG_FILE_PATH], text=True)
        # Split the result into individual lines
        lines = result.strip().split('\n')
        # Extract IP addresses from the lines
        ip_addresses = []
        for line in lines:
            # Assuming the IP address is the first element in each line
            ip = line.split()[0]
            ip_addresses.append(ip)
        # Remove duplicates
        ip_addresses = list(set(ip_addresses))
        return jsonify({'ip_addresses': ip_addresses})
    except subprocess.CalledProcessError as e:
        # grep returns exit code 1 if no matches are found
        if e.returncode == 1:
            return jsonify({'ip_addresses': []})
        else:
            return jsonify({'error': 'An error occurred while processing the logs'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/clearLogs', methods=['POST'])
def clear_logs():
    try:
        # Clear the log file
        open(LOG_FILE_PATH, 'w').close()
        # Alternatively, you can truncate the file using shell command
        # subprocess.run(['truncate', '-s', '0', LOG_FILE_PATH], check=True)
        return jsonify({'message': 'Apache logs have been cleared'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
