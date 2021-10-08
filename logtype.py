def get_percentage_overview(json_dict, count):
    logtype_count = {}
    for item in json_dict:
        logtype_count[item] = (len(json_dict[item]) / count) * 100
    return logtype_count


def print_percentage_overview(json_dict):
    print(f'The request percentage is as follows: ')
    print('Req. Type\tPercentage')
    for item in json_dict:
        print(f'{item} :\t\t{json_dict[item]:.4f}%')
