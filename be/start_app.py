
from flask import Flask, send_file, request, jsonify
import nbformat as nbf
import os
from relevance_ai import creator

app = Flask(__name__)

@app.route('/', methods=['POST'])
def create_notebook():
    data = request.get_json()
    
    url = data['url']
    desc = data['desc']

    filename = creator(url)

    # Save the notebook
    notebook_path = f'{filename}.ipynb'

    # Serve the notebook as a file download
    return send_file(notebook_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
