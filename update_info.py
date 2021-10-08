import ip_addr
import json
from datetime import date
import read_json_log
import logtype


def update_map_data():
    ip_addr_dict = ip_addr.load_ip_addr()
    data = []

    for item in ip_addr_dict:
        data.append({
            'key': item['query'],
            'latitude': item['lat'],
            'longitude': item['lon'],
            'country': item['countryCode'],
            'metric': 1
        })

    file = open('../info/map_data', 'w')
    file.write(json.dumps(data))
    file.close()


def update_sorted_ip_addr():
    data_dict = ip_addr.load_ip_addr()
    number, country = ip_addr.get_top_countries(data_dict)
    json_list = []
    for item in country:
        json_list.append({
            'country': item,
            'no': number[item]
        })

    file = open('../info/sorted_ip_addr', 'w')
    file.write(json.dumps(json_list))
    file.close()


def update_logtype_statistics(json_dict):
    dict_count = len(json_dict)

    logtype_data, unique_logtype_amount = read_json_log.group_by_field(json_dict, 'logtype')
    percentage_count = logtype.get_percentage_overview(logtype_data, dict_count)

    file = open('../info/logtype_statistics', 'w')
    file.write(json.dumps(percentage_count))
    file.close()


def update_general_statistics(json_dict):
    len_file = open(f'../info/general', 'w')

    dict_count = len(json_dict)
    _, date_amount = read_json_log.group_dates(json_dict)
    _, logtype_amount = read_json_log.group_by_field(json_dict, 'logtype')
    _, unique_ip_addr_amount = read_json_log.group_by_field(json_dict, 'src_host')

    len_file.write(json.dumps({
        'dict': dict_count,
        'date': date_amount,
        'logtype': logtype_amount,
        'ip_addr': unique_ip_addr_amount
    }))
    len_file.close()


def update_daily_statistics(json_dict):
    data, _ = read_json_log.group_dates(json_dict)
    counter_list = []

    for item in data:
        counter_list.append({
            'date': item[5:],  # Removing the year for a prettier dashboard
            'no': len(data[item])
        })

    file = open('../info/daily_statistics', 'w')
    file.write(json.dumps(counter_list))
    file.close()


if __name__ == '__main__':
    today = date.today()
    args = today.strftime("%Y-%m-%d")
    json_dict = read_json_log.get_data(args)

    update_daily_statistics(json_dict)
    update_map_data()
    update_sorted_ip_addr()
    update_logtype_statistics(json_dict)
    update_general_statistics(json_dict)