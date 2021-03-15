
import requests
import json
import argparse


class bcolors:
    CYAN = '\033[96m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


access_token = '#######'
url = 'https://paste.sr.ht'
endpoint = url + '/api/pastes'

headers = {"Authorization":"token {}".format(access_token), "Content-Type": "application/json"}


def print_data(data):
    for d in data:
        link =  url + '/' + d['user']['canonical_name'] + '/' + d['sha']
        print(bcolors.CYAN,
                d['visibility'],
                bcolors.ENDC,
                link
                )
        print("  files:")
        for f in d['files']:
            print( ' - ', f['filename'])


def request(args):
    if args.add:
        visibility = args.visibility if args.visibility else 'private'
        file_name = args.file_name if args.file_name else None

        data = {
                "visibility": visibility,
                "files": [
                    {
                        "filename": file_name,
                        "contents": args.add
                        }
                    ]
                }

        data = json.dumps(data)
        try:
            r = requests.post(endpoint, headers=headers, data=data)
        except requests.exceptions.RequestException as e:
            raise Exception(e)

    else:
        try:
            r = requests.get(endpoint, headers=headers)
        except requests.exceptions.RequestException as e:
            raise Exception(e)

    return r




def main():
    arg_parser = argparse.ArgumentParser(description='paste.sr.ht cli')

    arg_parser.add_argument('-a', '--add', help='add contents',
            metavar='CONTENTS', type=str)


    arg_parser.add_argument('-n', '--file-name', help='file name',
            metavar='NAME', type=str,)

    arg_parser.add_argument('-v', '--visibility', help='public, private, or unlisted',
            metavar='VISIBILITY', type=str)


    args = arg_parser.parse_args()

    try:
        r = request(args)
        if r.status_code == 200:
            print_data(r.json()["results"])
        elif r.status_code == 201:
            print(bcolors.CYAN , "created successfully", bcolors.ENDC)
        else:
            print("status code:", r.status_code)
            raise Exception(str(r.json()["errors"]))

    except Exception as e:
        err = format("ERROR: " +bcolors.FAIL + str(e) + bcolors.ENDC)
        print(err)




if __name__ == '__main__':
    main()
