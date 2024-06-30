from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    # Your code to load and process data
    return jsonify({"data": "sample data"})

if __name__ == '__main__':
    app.run(debug=True)