# League of Legends Items Script

This script is to create item sets for every character based on champion.gg 's Most Frequent Core Build and Highest Win Percentage Core Build.

The script parses the website for every champion and every lane for that champion. It grabs the item codes from the pictures of the builds and generates a folder and json file for every champion and every lane.

These builds are monitored and updated daily, so this script is meant be run daily.

### Crontab setup

30 2 * * * nice /path/to/update.sh

### TODO

Add Most Frequest Skill Order and Highest Win Percentage Skill Order to item set headers.

Beauitfy json files
