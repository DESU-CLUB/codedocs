
from flask import Flask, send_file, request, jsonify
import nbformat as nbf
import os
from relevance_ai import creator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/create_notebook', methods=['POST'])
@cross_origin()
def create_notebook():
    try:
        if request.is_json:
            data = request.get_json()
            print(data)
            url = data['url']

            creator(url)
            filename = 'new_exercise_notebook'
            # Save the notebook
            notebook_path = f'{filename}.ipynb'

            # Serve the notebook as a file download
            return send_file(notebook_path, as_attachment=True)
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred'}), 500
if __name__ == '__main__':
    app.run(debug=True)
