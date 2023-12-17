from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/registry/api/v1/model/register/tarball', methods=['POST'])
def register_model():
    tar_file = request.files.get('tar_file')
    base_id = request.form.get('base_id')
    flavour = request.form.get('flavour')
    name = request.form.get('name')
    description = request.form.get('description')

    # Do something with the uploaded file and form data
    # ...

    response_data = {
        'status': 'success',
        'message': 'Model registered successfully'
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
