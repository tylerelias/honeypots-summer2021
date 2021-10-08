import argparse

FILEPATH = "/honeypot/canary_raw/"
CONVERTED_PATH = "/honeypot/canary_logs/"


def convert_data(path, date):
    data = add_commas(path)
    save_to_file(data, date)


def add_commas(path):
    with open(path) as f:
        lines = f.read().splitlines()
        newline = ','.join(lines)
        new_data = newline
    return new_data


def save_to_file(data, date):
    file = open(f'../canary_logs/{date}.json', 'w')
    file.write('{ "logs": [' + data + ']}')
    file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True)

    args = parser.parse_args()
    args = args.date

    convert_data(FILEPATH + args, args)

    print('Logs have been converted to JSON format')
