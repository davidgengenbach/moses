#!/usr/bin/env python

import mechanicalsoup
import os
import glob
import base64

USER = 'MOSES'
PASSWORD = 'TUD_MOSES_16'

domain = 'http://www.mais.informatik.tu-darmstadt.de/'
start_page = domain + 'moses-ws16-int'


def main():
    basic_auth_token = get_auth_token(USER, PASSWORD)
    headers = {'Authorization': '{}'.format(basic_auth_token)}

    browser = mechanicalsoup.Browser()

    page = browser.get(start_page, headers=headers)
    links = [domain + link.attrs['href'] for link in page.soup.select('table tbody tr td a')]

    for folder in ['exercises', 'exercises/solutions', 'modules']:
        try:
            os.mkdir(folder)
        except:
            pass

    for link in links:
        filename = link.split('/')[-1]
        if 'solutions' in filename:
            target_folder = 'exercises/solutions'
        elif 'Exercise' in filename:
            target_folder = 'exercises'
        else:
            target_folder = 'modules'

        filename = '{}/{}'.format(target_folder, filename)
        if os.path.exists(filename):
            print('Already downloaded: {}'.format(filename))
            continue

        print('Downloading: {}\n({})\n'.format(filename, link))
        with open(filename, 'wb') as f:
            f.write(browser.get(link, headers=headers).content)
    # Delete old versions
    files = glob.glob('**/*.pdf')
    for file in files:
        if 'all.pdf' in file:
            continue
        base, version = get_filedata(file)
        for file_ in files:
            if base in file_ and file is not file_:
                _, version_ = get_filedata(file_)
                target = file if version < version_ else file_
                if os.path.exists(target):
                    os.remove(target)


def get_auth_token(user, password):
    return 'Basic {}'.format(b64_encode('{}:{}'.format(user, password)))


def b64_encode(s):
    return base64.b64encode(str.encode(s)).decode('utf-8')


def get_filedata(file):
    # Get version and basefilename
    parts = file.split('/')[-1].split('-v')
    return (parts[0], float(parts[1].replace('.pdf', '')))


if __name__ == '__main__':
    main()
