# twitter-bot
This project runs a social media bot that interacts with twitter. It is designed to facilitate the generation of content on social media. At regular intervals it randomly selects from a set of defined behaviors. These include the following:
- Twitter: 
  - Twitter post: searches current posts using a defined query string (including #tags or @usernames)
  - Twitter DMs: responds to recent DMs by sending a response DM. The bot maintains a list of recent DMs and sends a response to any new messages 
- RSSwidget: retrieves post from an RSS feed and composes a twitter post based on the title, content and article link. The RSSWidget contains a general parsing function as well as a range of predefined parsing functions for specific feeds (i.e., Pubmed). It attempts to identify feeds through url matching and uses the general RSSWidget if no match is made.
- News Widget: performs search of Google News for specified terms and returns post
- Reddit Widget: performs search of specified subreddit for articles. * Note that this functionality requires obtaining Reddit API credentials.
- Udemy Widget: specialized form of Redit widget which identifies links to Udemy courses with discount coupons. It will follow link to identify the Udemy url and coupon code. It also requires Reddit API credentials.
- QuoteWidget: POC functionality to post random quotes from random people.

# installation
Follow these steps to install and run the bot:

1. Clone the repository
```
git clone git@github.com:sequencecentral/twitter-bot.git
cd twitter-bot
```

1. Setup a virtual environment (recommended)
```pythons
python3 -m venv env
```

3. Activate the virtual environment
```
. ./env/bin/activate
```

4. Install the requirements
```python
pip3 install -r requirements.txt
```

5. Run the bot
```python
python go_bot.py
```

# use


# dependencies
- Synchron
- AverageJoe
- BasicBot