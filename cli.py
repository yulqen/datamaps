import multiprocessing
import sys

from datamaps.main import cli

if __name__ == '__main__':
    multiprocessing.freeze_support()
    cli(sys.argv[1:])