import os
import argparse
import img2pdf


def convert_to_pdf(loc):
    """
    Convert to pdf
    """
    os.chdir(loc)
    file_list = os.listdir()
    file_list.remove('.DS_Store')
    for folder in file_list:
        os.chdir(folder)
        imgs = os.listdir('.')
        if '.DS_Store' in imgs:
            imgs.remove('.DS_Store')
        imgs.sort()
        pdf_bytes = img2pdf.convert(*imgs)
        file = open(folder+".pdf", "wb")
        file.write(pdf_bytes)
        print("{} converted to PDF".format(folder))
        os.chdir('../')


def main():
    """
    Create pdf from folders of imgs
    base structure: manga_name/chapter_name/img.jpg
    :param: folder address
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--location', help="the location of the folder")
    args = parser.parse_args()

    if args.location is None:
        print("Please enter the location of manga with -l.")
    else:
        convert_to_pdf(args.location)

if __name__ == '__main__':
    main()