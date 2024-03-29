# DIRECTIONS FOR USE

**This Script downloads 100 of the User's most played beatmapsets**

## Downloading Chrome Driver

1. Go to this [link](https://sites.google.com/chromium.org/driver/downloads) and download the latest version's zip file according to your os.
2. Unzip it and run the exe file.

## Getting Mapset ids

1. In get_mapset_ids.py file, replace client id, client secret and player id to your own credentials and then run the file.
2. To get client id and client secret, go to you osu profile settings and scroll down to bottom and click on new OAuth Application.

## Downloading Beatmapsets from saved ids

1. In downloader.py change download_dir to where you want to download the mapsets, and change username and password to your osu account credentials and then run the file.
2. After about 150~200 downloads the website may say "Rate limit exceeded". If this happens, the webdriver will save your progress and exit the script. Run the script after a few hours to resume.

## Read Instructions below if only if you want to change the default behaviour of this script.

- By default this script saves ids of **most played** beatmapsets in descending order, to change this, change the **type** variable in the script.
- By default this script saves 100 ids, change the **total** variable to modify this.
- Run set_toDownload_mapsets.py to reset mapsets queued to download.

## Additional Info
- By default, this downloads mapsets with video whenever possible as this was my personal preference.
- I have added delays in the script to prevent unnecessarily stressing osu's servers.