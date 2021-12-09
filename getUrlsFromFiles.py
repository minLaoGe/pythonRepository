# return all urls from files in currentDir. ;

# for example exec this command  in this dir: python3 getUrlsFromFiles.py ./com.antourong


# when you execute the command above this line, you will get a "txt" file, same name that you type in;

import os
import sys
import re

urls = set()


def recurisiveFindUrl(dirname):
    if os.path.isdir(dirname):
        list = os.listdir(dirname)
        for name in list:
            recurisiveFindUrl(os.path.join(dirname, name))


    elif os.path.isfile(dirname) & dirname.endswith(".xml"):
        getFileUrls(dirname)


def getFileUrls(filename):
    with open(filename, 'r') as f:

        line = f.readline()

        while line:

            url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', line)

            if len(url) > 0:
                urls.update(url)

            line = f.readline()


if __name__ == '__main__':
    args = sys.argv

    for name in args:
        recurisiveFindUrl(name);

    firstFileName=args[1];

    fileindex = firstFileName.rfind("/");

    filename = firstFileName[fileindex + 1:len(firstFileName)]

    file = open(filename + ".txt", 'w')

    file.write("\t\t\n\n".join(urls))

    file.close()
