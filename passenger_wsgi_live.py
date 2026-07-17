import sys, os

INTERP = os.path.expanduser("/home/terapkco/virtualenv/xcomic_backend/3.11/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from main import app as application
