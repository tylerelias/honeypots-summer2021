import argparse
import json
from datetime import datetime
import logtype
import ip_addr

FILEPATH = "/honeypot/canary_raw/"
CONVERTED_PATH = "/honeypot/canary_logs/"


def get_data(date):
    file = open(CONVERTED_PATH + date + '.json')
    json_data = json.load(file)
    json_data = json_data['logs']
    json_data = add_timestamps(json_data)
    file.close()
    return json_data


def group_dates(data):
    """
    needs to be a special function because of
    the .split() call to clean the date format
    :param data:
    :return: dict, unique date amount
    """
    date_dict = {}
    for item in data:
        item_date = item['local_time'].split(' ', 1)[0]

        if item_date in date_dict:
            date_dict[item_date].append(item)
        else:
            date_dict[item_date] = []
            date_dict[item_date].append(item)
    return date_dict, len(date_dict)


def group_by_field(data, field_name):
    _dict = {}
    for item in data:
        field = item[field_name]

        if field in _dict:
            _dict[field].append(item)
        elif field != '':
            _dict[field] = []
            _dict[field].append(item)
    return _dict, len(_dict)


def display_logtype_statistics(percentage_count):
    print_bar()
    print(f'\tLOGTYPE STATISTICS')
    print_bar()
    logtype.print_percentage_overview(percentage_count)
    print_bar()


def print_bar():
    print('=====================================')


def add_timestamps(json_dict):
    for item in json_dict:
        timestamp = convert_to_timestamp(item['local_time'])
        item['timestamp'] = timestamp
    return json_dict


def convert_to_timestamp(time):
    dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    return int(dt.timestamp())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True)

    args = parser.parse_args()
    args = args.date

    json_dict = get_data(args)

    dict_count = len(json_dict)
    # Do stuffs with data
    print_bar()
    date_data, unique_dates_amount = group_dates(json_dict)
    print(f'There are {unique_dates_amount:,} days worth of logs')
    # Logtype
    logtype_data, unique_logtype_amount = group_by_field(json_dict, 'logtype')
    print(f'There are {unique_logtype_amount:,} different log types')
    percentage_count = logtype.get_percentage_overview(logtype_data, dict_count)
    # Ip Addresses
    ip_addr_data, unique_ip_addr_amount = group_by_field(json_dict, 'src_host')
    print(f'There are {unique_ip_addr_amount:,} unique IP addresses recorded')
    print(f'There are {dict_count:,} requests that have been made to the server')
    display_logtype_statistics(percentage_count)
    # TODO: Test filter
    filtered_json_dict = ip_addr.filter_by_logtypes([3000, 2000, 4002, 3001], json_dict)

    print_bar()
    print(f'IP ADDRESS STATISTICS')
    print_bar()
    ip_addr_json = ip_addr.load_ip_addr()
    ip_addr_top_country, top_list = ip_addr.get_top_countries(ip_addr_json)
    print("Top 10 countries that have made contact to the honeypot:")
    print_bar()
    ip_addr.display_top10(ip_addr_top_country, top_list)
