# AMQ-Expand-Library-Scraper

Expand Library Scraper cheat for https://animemusicquiz.com/

## Prerequisites

Python 3

pandas (comes with anaconda or use ``` pip install pandas ``` )

selenium (install geckodriver https://github.com/mozilla/geckodriver)

## Scrape

1. Before running the amqscrape.py ensure that your account has the list you want to use e.g. https://myanimelist.net/profile/purplepinapples
2. Simply alter the file contents to your AMQ username and password then run it and wait 19 hours (approx for 7000 anime)

## Read Saved Database

1. When in AMQ browser page, press F12 and navigate to network tab
2. Right click on the file that is 6 characters + '.mp3' or '.webm'
3. Copy Link Address
4. Paste into the search box of the Read AMQ Database window and press enter
5. Anime is automatically copied to clipboard for easy pasting

### Additional Notes

Code is written entirely by me and I am not an expert so if you have any suggestions please feel free to give me suggestions.

I will update the combined.csv regularly (maybe once a month) so it is not out of date.

Dupes section might contain some that doesn't work so please be careful before you flex 💪
