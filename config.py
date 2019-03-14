
import os
import sys
import time
import datetime


try:
    OUTPUT_DIR = os.path.abspath(os.getenv('OUTPUT_DIR'))
    # print(OUTPUT_DIR)
except Exception as e:
    OUTPUT_DIR = None
    # print(f'Exception: {e}')

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# print(f'Repo DIR {REPO_DIR}')
if not OUTPUT_DIR:
    OUTPUT_DIR = os.path.join(REPO_DIR, 'output')
    # print(f'Output DIR {OUTPUT_DIR}')

ARCHIVE_DIR_NAME = 'archive'
SOURCES_DIR_NAME = 'sources'
ARCHIVE_DIR = os.path.join(OUTPUT_DIR, ARCHIVE_DIR_NAME)
SOURCES_DIR = os.path.join(OUTPUT_DIR, SOURCES_DIR_NAME)

# print(f'Output DIR {OUTPUT_DIR}')
# print(f'Repo DIR {REPO_DIR}')
# print(f'Archive DIR {ARCHIVE_DIR}')
# print(f'Sources DIR {SOURCES_DIR}')


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        # print(f'Platform: {sys.platform}')
        return sys.platform

    # print(f'Platform: {platforms[sys.platform]}')
    return platforms[sys.platform]


platform = get_platform()
if platform == 'OS X' or 'Linux':
    logs_dir = './logs/'
if platform == 'Windows':
    logs_dir = '.\\logs\\'


def get_tstamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
    return st

