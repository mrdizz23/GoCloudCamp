#!/usr/bin/env python3

import json
from re import S
from flask import Flask, jsonify, request, make_response, cli

data_file = '/code/data.json'

app = Flask(__name__)
cli.show_server_banner = lambda *_: None

def get_service(service):
    with open(data_file, 'r') as openfile:
        data = json.load(openfile)
    
    if service not in data:
        return ('404 Not Found\n', 403)
    
    return data[service]["data"]
    
def add_service(service_imp, data_imp):
    with open(data_file, 'r') as openfile:
        data = json.load(openfile)
    
    if service_imp not in data:
        
        data[service_imp] = {
            'data': data_imp,
            'status': 0
        }
    
        result_code = 201
    
    else:
        data[service_imp]['data'] = data_imp
        result_code = 200
    
    with open(data_file, "w") as outfile:
        json.dump(data, outfile, indent=2)
    
    return result_code

def delete_service(service):
    with open(data_file, 'r') as openfile:
        data = json.load(openfile)
        
    if service not in data:
        return ('404 Not Found\n', 403)

    if data[service]['status'] == 1:
        return ('403 Servise is blocked\n', 403)
    
    result = data.pop(service)
    
    with open(data_file, "w") as outfile:
        json.dump(data, outfile, indent=2)
    
    return result

if __name__ == '__main__':

    @app.route('/config', methods=['GET'])
    def get():
        service = request.args.get('service')
        if not service:
            return make_response('400 Bad Request\n', 400)
        data = get_service(service)
        if type(data) is tuple:
            return make_response(data)
        return jsonify(data)
    
    @app.route('/config', methods=['POST','PATCH'])
    def post():
        content = request.get_json(silent=True)
        if not content:
            return make_response('400 Bad Request\n', 400) 
        service = content.get("service", 0)
        data = content.get("data", 0)
        if service == 0 or data == 0:
            return make_response('400 Bad Request\n', 400) 
        
        result_code = add_service(service, data)
        
        return make_response(jsonify(content), result_code)
    
    @app.route('/config', methods=['DELETE'])
    def detete():
        service = request.args.get('service')
        if not service:
            return make_response('400 Bad Request\n', 400) 
               
        result = delete_service(service)
        
        if type(result) is tuple:
            return result
        return jsonify(result)

    app.run(host='0.0.0.0', port='8080')
