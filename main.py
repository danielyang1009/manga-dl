import os
import sys
import argparse
import urllib.request
from bs4 import BeautifulSoup



def main():
    """
    Download 

    """
    parser = argparse.ArgumentParser(description='Download from MangaPark')
    parser.add_argument('-m', '--manga-url', help='The url of the mangaprk manga to download')
    parser.add_argument('-c', '--chapter', help='The chapter number that you want to download.')
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()


