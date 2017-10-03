# Discord Scraper [Beta]

Release Date: October 3, 2017 @ 10:13 UTC-0

Testing Version of Python: 2.7.14
Target Version of Python: >= 2.7.8

# Tutorial

Step 1:
Open/Login to your Discord app and press CTRL + SHIFT + I to open the Developer Tools panel.
Take the Server ID and Channel ID data from the URL in the title of the Developer Tools panel.
![x74PJvp.png](https://i.imgur.com/x74PJvp.png "Step 1")

Step 2:
Go to the Application tab in the Developer Tools panel.
Expand the Local Storage area on the left-side of the Developer Tools panel.
Select the discordapp URL in the list.
Highlight the data between the quotation marks in the token value and press CTRL + C to copy the token.
![hTsoSGd.png](https://i.imgur.com/hTsoSGd.png "Step 2")

Step 3:
Open the Discord.py script in any Python IDE of your choosing (IDLE was used in this example).
Replace the text '<TOKEN>' with the token value you grabbed from Step 2.
Replace the text '<SERVERID>' with the Server ID data that you grabbed from Step 1.
Replace the text '<CHANNELID>' with the Channel ID data that you grabbed from Step 1.
Alter the Query value as necessary (the default is set to grab all NSFW and non-NSFW images and videos).
![dqsYX8q.png](https://i.imgur.com/dqsYX8q.png "Step 3")

Step 4:
Make sure that you put the Discord.py script in its own folder since all contents will be placed in the same folder that the Discord.py file resides.
Run the Discord.py script and it should prompt you for the number of pages to grab (this coincides with the page number from the search query) the general rule is 25 contents per page, so 2 pages would equate to about 50 items.
Let the script run (it may take a while to finish) the beta version of this script is designed to halt upon error, but the final release of this script will ignore errors and continue grabbing data as demanded.

# Changelog (DD-MM-YYYY)

03-10-2017 - Beta Release:
* The first release of the script.
* Not meant for production use.
* Still has bugs to fix and features to implement.