from flask import Flask, json, Response, jsonify, request
from datetime import date
import ip_addr
import logtype
import update_info
import read_json_log
from datetime import date

api = Flask(__name__)


@api.route('/', methods=['GET'])
def get_response():
    return Response(status=200)


@api.route('/get-map-data', methods=['POST'])
def get_map_data():
    """
    Fetches the data required to display the map on the Grafana dashboard
    :return: json object
    """
    file = open('../info/map_data')
    data = json.load(file)
    return json.dumps(data)


@api.route('/ip-addr/sorted', methods=['POST'])
def get_sorted_ip_addr():
    file = open('../info/sorted_ip_addr')
    data = json.load(file)
    return json.dumps(data)


@api.route('/logtype-statistics', methods=['POST'])
def get_logtype_statistics():
    file = open('../info/logtype_statistics')
    data = json.load(file)
    return data


@api.route('/general-stats', methods=['POST'])
def get_general_stats():
    file = open('../info/general')
    general_dict = json.load(file)
    return json.dumps(general_dict)


@api.route('/daily-stats', methods=['POST'])
def get_daily_stats():
    file = open('../info/daily_statistics')
    daily_dict = json.load(file)
    return json.dumps(daily_dict)


if __name__ == '__main__':
    host = 'FILL_OUT'
    port = 4242
    api.run(host=host, port=port)