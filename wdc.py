
from config import (
    OUTPUT_DIR,
    get_platform,
    get_tstamp
)
from web_runner import download_url

download_url("https://joshsisto.com")

print(OUTPUT_DIR)
platform = get_platform()
print(platform)
tstamp = get_tstamp()
print(tstamp)

