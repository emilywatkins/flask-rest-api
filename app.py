from flask import Flask, request
import json
from data_retriever import get_records, get_record, validate_request_args

app = Flask(__name__)

@app.route('/compensation_data', methods=['GET'])
def list_compensation_data():
    try:
        validate_request_args(request.args)
    except ValueError as err:
        body = f'Invalid request argument(s): {err}'
        response = app.make_response((json.dumps(body), 400))
        response.headers['Content-Type'] = 'application/json'
        return response

    try:
        records = get_records(request.args)
    except Exception as err:
        body = f'Something went wrong: {err}'
        response = app.make_response((json.dumps(body), 500))
        response.headers['Content-Type'] = 'application/json'
        return response
    
    body = json.dumps(records)
    response = app.make_response((body, 200))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/compensation_data/<int:id>', methods=['GET'])
def get_compensation_data(id):
    record = get_record(id)

    if record is None:
        body = f'Record with id: "{id}" not found.'
        response = app.make_response((json.dumps(body), 404))
        response.headers['Content-Type'] = 'application/json'
        return response

    body = json.dumps(record)
    response = app.make_response((body, 200))
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run()
