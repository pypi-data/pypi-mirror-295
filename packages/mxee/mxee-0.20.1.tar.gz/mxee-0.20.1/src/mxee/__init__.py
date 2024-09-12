import configparser
import os


def config(k):
    p = configparser.ConfigParser()
    p.read(os.path.expanduser("~/.mxee.ini"))
    cols = k.split(".")
    s = p.sections()
    try:
        res = p[cols[0]][cols[1]]
    except:
        res = ""
    return res
