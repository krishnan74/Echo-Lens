import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the base URL of your Flask app
FLASK_APP_BASE_URL = "https://tidb-hackathon.vercel.app/"  # Replace with your Flask app's URL

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def reverse_proxy(path):
    try:
        # Construct the full URL for the request to the Flask app
        full_url = f"{FLASK_APP_BASE_URL}/{path}"
        
        # Forward the request to the Flask app and get the response
        response = requests.request(
            method=request.method,
            url=full_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
        )
        
        # Construct the Flask-like response object for the serverless function
        headers = [(key, value) for (key, value) in response.headers.items()]
        return jsonify(response.json()), response.status_code, headers
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request to the Flask app
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
