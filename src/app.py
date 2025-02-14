from flask import Flask, jsonify, request
from resolver import function_parameters

# Create Flask app instance
app = Flask(__name__)

# Request a function signature
@app.route('/api/signature', methods=['POST'])
def post_data():
    print('here')
    data = request.get_json()
    name = data.get('name')
    signatures = function_parameters(name)
    result = {
        "name": name,
        "signatures": signatures
    }
    return jsonify(result), 200

# Handle exceptions
@app.errorhandler(Exception)
def handle_generic_error(error):
    response = {
        "error": "Internal Server Error",
        "message": str(error)
    }
    return jsonify(response), 500  # Return 500 Internal Server Error


# Start the server
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=4444)