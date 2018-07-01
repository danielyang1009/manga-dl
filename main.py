import os
import re
import sys
import argparse
import urllib.request
from bs4 import BeautifulSoup


def parse_url(url):
    """
    :param url:
    :return: title of manga
    """


def make_directory(directory):
    """
    Making directory if not exists
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        pass


def parse_url_to_chapter_info(url):
    """
    Extract manga info from the URL, namely: ()
    :param url: a string that denotes the URL
    :return: 4-tuple containing the manga's title, version, chapter and url
    """

    url = re.sub("http://", '', url)
    url = re.sub("mangapark.me", '', url)
    url = re.sub("/manga/", '', url)

    if len(url.split("/")) == 3:
        title, version, chapter = url.split("/")
    elif len(url.split("/")) == 4:
        title, _, version, chapter = url.split("/")
    else:
        raise ValueError("Couldn't parse URL", url)

    return title, version, chapter


def download_chapters(url):
    """
    Download the manga chapters
    :param url: string url of the manga
    """
    _, _, chapter = parse_url_to_chapter_info(url)
    print("Downloading chapter", chapter)
    make_directory(chapter)
    os.chdir(chapter)
    try:
        page = urllib.request.urlopen(url)
    except ValueError:
        page = urllib.request.urlopen("http://mangapark.me" + url)
    soup = BeautifulSoup(page, "html.parser")
    imgs = soup.find_all('a', {'class':'img-link'})
    for i in imgs:
        img_url = 'http:' + i.img.get('src')
        file_name = img_url.split('/')[-1]
        print("Downloading {} - {}...".format(chapter, file_name))
        print(os.getcwd())
        urllib.request.urlretrieve(img_url, file_name)
    os.chdir('../')


def find_chapters(url):
    """
    Finding the manga chapters
    :param url: string url of the manga
    """
    print("Download from {}".format(url))
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    volumes = soup.find_all('ul', {'class':'chapter'})
    volume_lens = []
    for volume in volumes:
        chapters = volume.find_all('li')
        volume_lens += [len(chapters)]
    
    max_len = max(volume_lens)
    best_volume = volumes[volume_lens.index(max_len)]

    chapters = best_volume.find_all('li')
    for c in chapters[::-1]:
        chapter_url = c.em.find_all("a")[-1]['href']
        download_chapters(chapter_url)
    
    
def main():
    """
    Download from mangapark
    """
    parser = argparse.ArgumentParser(description='Download from MangaPark')
    parser.add_argument('-m', '--manga_url', help='The url of the mangaprk manga to download')
    parser.add_argument('-c', '--chapter', help='The chapter number that you want to download.')
    args = parser.parse_args()

    if args.manga_url is None:
        print("Please specify the URL of the manga on mangapark.me")
        return
    else:
        _, _, title, = parse_url_to_chapter_info(args.manga_url)
        make_directory(title)
        print("Title: ", title)
        os.chdir(title)
        find_chapters(args.manga_url)

if __name__ == "__main__":
    main()


