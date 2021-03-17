
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


def show_pastes(data):
    for d in data:
        link =  url + '/' + d['user']['canonical_name'] + '/' + d['sha']
        print(bcolors.CYAN,
                d['visibility'],
                bcolors.ENDC,
                link
                )
        
        print(' created: ', d['created'])
        print(' files:')
        for f in d['files']:
            print( ' - ', f['filename'])
            print( '     blob_id: ', f['blob_id'])


def show_paste(data):
    print(data['contents'])


def request(args):
    visibility = args.visibility if args.visibility else 'private'

    data = dict()
    data['visibility'] = visibility
    if args.file or args.add:
        files = list()

        if args.file:
            for f in args.file:
                with open(f, 'r') as reader:
                    content = reader.read()
                    name = f
                    files.append({"filename":name, "contents": content})

        if args.add:
            name = args.name if args.name else None
            content = args.add
            files.append({"filename":name, "contents": content})

        data['files'] = files
        data = json.dumps(data)
        r = requests.post(endpoint, headers=headers, data=data)

    elif args.delete:
        _endpoint = endpoint + "/{}".format(args.delete)
        r = requests.delete(_endpoint, headers=headers)
    elif args.show:
        _endpoint = url + "/api/blobs/{}".format(args.show)
        r = requests.get(_endpoint, headers=headers)
    else:
        r = requests.get(endpoint, headers=headers)

    return r




def main():
    arg_parser = argparse.ArgumentParser(description='paste.sr.ht cli')

    arg_parser.add_argument('-a', '--add', help='add contents',
            metavar='CONTENTS', type=str)

    arg_parser.add_argument('-n', '--name', help='file-name',
            metavar='NAME', type=str,)

    arg_parser.add_argument('-f', '--file', help='location of dest file/s',
            metavar='FILES', type=str, nargs='+')

    arg_parser.add_argument('-v', '--visibility', help='public, private, or unlisted',
            metavar='VISIBILITY', type=str)

    arg_parser.add_argument('-s', '--show', help='show paste',
            metavar='BLOB_ID', type=str)

    arg_parser.add_argument('-d', '--delete', help='delete paste',
            metavar='SHA', type=str)



    args = arg_parser.parse_args()

    try:
        r = request(args)
        if r.status_code == 200:
            if args.show:
                show_paste(r.json())
            else:
                show_pastes(r.json()["results"])
        elif r.status_code == 201:
            print(bcolors.CYAN , "created successfully", bcolors.ENDC)
        elif r.status_code == 204:
            print(bcolors.CYAN , "processed successfully", bcolors.ENDC)
        else:
            print("status code:", r.status_code)
            raise Exception(str(r.json()["errors"]))

    except Exception as e:
        err = format(bcolors.FAIL + "ERROR: " + bcolors.ENDC + str(e) )
        print(err)




if __name__ == '__main__':
    main()
