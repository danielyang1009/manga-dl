import os
import re
import sys
import argparse
import img2pdf
import urllib.request
from bs4 import BeautifulSoup


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


def convert_to_pdf(file_len, chapter):
    """
    Convert imgs of local folder to pdf
    """
    file_list = ['{:0>3d}.jpg'.format(i) for i in range(1, file_len+1)]
    print(file_list)
    pdf_bytes = img2pdf.convert(*file_list)

    file = open(chapter+'.pdf', "wb")
    file. write(pdf_bytes)
    print("{} has converted to PDF".format(chapter+'.pdf'))


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
        img_name = '{:0>3d}.jpg'.format(int(file_name.split('.')[0]))
        print("Downloading {} - {}...".format(chapter, img_name))
        urllib.request.urlretrieve(img_url, img_name)

    convert_to_pdf(len(imgs), chapter)
    os.chdir('../')


def find_chapters(url, chap=None):
    """
    Finding the manga chapters
    :param url: string url of the manga
    :param chap: specific chapters to download
    """
    print("Download from {}, chapters {}".format(url, chap))
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    volumes = soup.find_all('ul', {'class':'chapter'})
    volume_lens = []
    for volume in volumes:
        chapters = volume.find_all('li')
        volume_lens += [len(chapters)]
    
    max_len = max(volume_lens)
    best_volume = volumes[volume_lens.index(max_len)]
    print("Best volume found is {}, and total chapters is {}".format(volume_lens.index(max_len), max_len))

    chapters = best_volume.find_all('li')[::-1]
    if chap is not None:
        bgn, end = [int(i) for i in chap.split('-')]
        bgn = bgn - 1
    else:
        bgn, end = [None]*2
    
    for c in chapters[bgn:end]:
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
    print(args)

    if args.manga_url is None:
        print("Please specify the URL of the manga on mangapark.me")
        return
    else:
        _, _, title, = parse_url_to_chapter_info(args.manga_url)
        make_directory(title)
        print("Title: ", title)
        os.chdir(title)
        find_chapters(args.manga_url, args.chapter)

if __name__ == "__main__":
    main()


