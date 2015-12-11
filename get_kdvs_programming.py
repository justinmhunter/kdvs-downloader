from __future__ import print_function

import argparse
import re
import requests
from shutil import copyfileobj
import signal
from socket import gethostbyname
import sys
from urllib2 import urlopen
from urlparse import urljoin, urlparse

from BeautifulSoup import BeautifulSoup


def signal_handler(signal, frame):
    """Generic signal handler to catch CTRL+C."""
    print()
    sys.exit(0)


def to_lower_camel_case(str):
    """Take in a string, and return a lower camelcased version of it.

      Args:
        - str: A string representing the name of the show we're downloading.

      Returns:
        - A lower camelcased string ex: 'Raise The Dead' becomes 'raiseTheDead'.
    """
    words = str.split()
    return words[0].lower() + "".join(x.title() for x in words[1:])


def main(args):
    """Parse the KDVS.org home page, looking for the URL of the show we want to
      download. Once found, and from the archive address, pull down the show
      from that exact day using the date argument.

    Args:
      - args.date: A string representing the date in YYYY-MM-DD format.
      - args.show: A string representing the name of the show ('Apartment 5').

    Returns:
      - A downloaded copy of the show name from the date specified.
    """
    date = args.date
    show_name = args.show

    home_url = 'http://kdvs.org/programming/schedule-grid/'
    archive_hostname = 'archives.kdvs.org'
    archive_address = gethostbyname(archive_hostname)

    base_page = urlopen(home_url)
    bs = BeautifulSoup(base_page)

    for link in bs.findAll('a', href=True):
        show_title = link.contents
        if show_title:
            title = str(show_title[0])
            if re.match(show_name, title, re.IGNORECASE):
                past_show_playlists = link.get('href')
                break

    if past_show_playlists:
        past_show_url_path = urlparse(past_show_playlists).path
        show_id = past_show_url_path.split('/')[-1]
        archive_path = '/'.join(['archives', '{}_{}_320kbps.mp3'.format(date, show_id)])
        show_download_url = urljoin('http://{}'.format(archive_address), archive_path)
        print('Grabbing: {} (#{}): {}'.format(show_name.title(), show_id, show_download_url))

        response = requests.get(show_download_url, stream=True)
        if response.status_code == requests.codes.ok:
            downloaded_show_name = '{}_{}.mp3'.format(to_lower_camel_case(show_name), date)
            with open(downloaded_show_name, 'w') as f:
                copyfileobj(response.raw, f)
            del response
        else:
            print('ERR: {} returned non-200. Is your date correct?'.format(show_download_url))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='KDVS Downloader 3000')
    parser.add_argument('-d', '--date', help='Date to download (YYYY-MM-DD)', required=True)
    parser.add_argument('-s', '--show', help='Name of show', required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGINT, signal_handler)
    main(args)
