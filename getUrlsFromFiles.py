# return all urls from files;

# for example exec this command  in this dir: python3 getUrlsFromFiles.py ./com.antourong


# when you execute the command above this line, you will get a file, same name that you type in;

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
        recurisiveFindUrl(args);

    fileindex = args.rfind("/");

    filename = args[fileindex + 1:len(args)]

    file = open(filename + ".txt", 'w')

    file.write("\t\t\n\n".join(urls))

    file.close()
