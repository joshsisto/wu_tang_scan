
import os

try:
    OUTPUT_DIR = os.path.abspath(os.getenv('OUTPUT_DIR'))
    print(OUTPUT_DIR)
except Exception as e:
    OUTPUT_DIR = None
    print(f'Exception: {e}')

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
print(f'Repo DIR {REPO_DIR}')
if not OUTPUT_DIR:
    OUTPUT_DIR = os.path.join(REPO_DIR, 'output')
    print(f'Output DIR {OUTPUT_DIR}')

ARCHIVE_DIR_NAME = 'archive'
SOURCES_DIR_NAME = 'sources'
ARCHIVE_DIR = os.path.join(OUTPUT_DIR, ARCHIVE_DIR_NAME)
SOURCES_DIR = os.path.join(OUTPUT_DIR, SOURCES_DIR_NAME)