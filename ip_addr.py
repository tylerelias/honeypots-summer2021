import argparse
import time
import read_json_log
import requests
import json

BATCH_SIZE = 100  # The maximum size of the batches that can be sent to the API
RESTRICTION_TIME = 4.1


def save_ip_addr(json_data):
    """
    Grouping IP addresses in batches of 100 each
    so it can be sent to an API for geo location
    information gathering
    :param json_data:
    :return: json object
    """
    url = 'http://ip-api.com/batch'
    res_list = []  # This will be the list of all of the responses from the API
    payload = []  # Contains the ip addresses that will be sent to the API
    counter = 0
    round_no = 0  # To keep track of the last batch that will probably not contain 100 ip addr's
    remainder = len(json_data) % 100  # The size of the last batch
    total_rounds = int(len(json_data) / BATCH_SIZE)

    print(f'Getting IP address geolocations, estimated time is: '
          f'{((total_rounds * RESTRICTION_TIME) + RESTRICTION_TIME) / 60} minutes')

    for item in json_data:
        counter += 1
        payload.append(item)
        if counter == BATCH_SIZE or (round_no == total_rounds and len(payload) == remainder):
            round_no += 1
            print(f'Getting IP address information: {round_no} / {total_rounds + 1}')

            response = requests.post(url, json=payload)
            if response.headers['X-Rl'] == '0':
                cooldown = int(response.headers['X-Ttl'])
                print(f'Rate limit exceeded, need to wait {cooldown} seconds')
                time.sleep(cooldown)
            tmp_res_list = json.loads(response.text)
            for info in tmp_res_list:
                res_list.append(info)
            time.sleep(RESTRICTION_TIME)  # API restrictions
            counter = 0
            payload = []
    return json.dumps(res_list)


def load_ip_addr():
    file = open('../ip_addr/ip_addr_info.json')
    json_data = json.load(file)
    file.close()
    return json_data


def get_top_countries(json_data):
    country_list = []
    country_dict = {}
    for item in json_data:
        if 'country' in item:
            country = item['country']
            if country in country_dict:
                val = country_dict[country]
                country_dict[country] = val + 1
            else:
                country_list.append(country)
                country_dict[country] = 1
    countries = sorted(country_list, key=lambda k: country_dict[k])
    return country_dict, reversed(countries)


def display_top10(ip_addr_top_country, top_list):
    print(f'Nation \t\t\t\t Total IP addr. connected')
    counter = 0
    for item in top_list:
        counter += 1
        print(f'{counter}. {item} : {ip_addr_top_country[item]:,}')
        if counter == 10:
            break


def filter_by_logtypes(logtypes, json_dict):
    """
    Filters the json_dict and only keeps the logtype id's
    that are passed into the function
    :param logtypes: list
    :param json_dict: list[dict, ..., dict]
    :return: list[dict, ..., dict]
    """
    filtered_dict = []
    for item in json_dict:
        if item['logtype'] in logtypes:
            filtered_dict.append(item)
    return filtered_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True)

    args = parser.parse_args()
    args = args.date

    json_dict = read_json_log.get_data(args)
    dict_count = len(json_dict)
    _, date_amount = read_json_log.group_dates(json_dict)
    _, logtype_amount = read_json_log.group_by_field(json_dict, 'logtype')

    json_dict = filter_by_logtypes([3000, 2000, 4002, 3001], json_dict)

    ip_addr_data, unique_ip_addr_amount = read_json_log.group_by_field(json_dict, 'src_host')
    json_ip_addr = save_ip_addr(ip_addr_data)

    file = open(f'../ip_addr/ip_addr_info.json', 'w')
    file.write(json_ip_addr)
    file.close()

    print('IP address file saved')
