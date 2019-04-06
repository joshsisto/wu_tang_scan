
import os
import sys
import time
import fnmatch
import datetime


try:
    OUTPUT_DIR = os.path.abspath(os.getenv('OUTPUT_DIR'))
    OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'output')
    # print(OUTPUT_DIR)
except Exception as e:
    OUTPUT_DIR = None
    # print(f'Exception: {e}')

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
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


def compare_tstamp(time_1, time_2):
    """compare two timestamps and return the difference in seconds and human readable (days, hours, minutes, seconds)"""
    t1 = datetime.datetime.strptime(time_1, '%Y-%m-%d_%H-%M-%S')
    t2 = datetime.datetime.strptime(time_2, '%Y-%m-%d_%H-%M-%S')
    t_diff = t1 - t2
    day = t_diff.seconds // (24 * 3600)
    t_time = t_diff.seconds % (24 * 3600)
    hour = t_time // 3600
    t_time %= 3600
    minutes = t_time // 60
    t_time %= 60
    seconds = t_time
    return t_diff.seconds, f'{day} day(s) {hour} hour(s) {minutes} minute(s) {seconds} second(s)'


def ensure_dir(file_path):
    try:
        # print(f'checking if {file_path} exists\n')
        if not os.path.exists(file_path):
            # print(f'directory {file_path} does not exist. Creating...')
            os.makedirs(file_path)
    except Exception as x:
        print(f"something fucked up {x}")


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

