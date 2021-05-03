# twitter-bot
This project runs a social media bot that interacts with twitter. It is designed to facilitate the generation of content on social media. At regular intervals it randomly selects from a set of defined behaviors. These include the following:
- **Twitter**: 
  - Twitter post: searches current posts using a defined query string (including #tags or @usernames)
  - Twitter DMs: responds to recent DMs by sending a response DM. The bot maintains a list of recent DMs and sends a response to any new messages 
- **RSSwidget**: retrieves post from an RSS feed and composes a twitter post based on the title, content and article link. The RSSWidget contains a general parsing function as well as a range of predefined parsing functions for specific feeds (i.e., Pubmed). It attempts to identify feeds through url matching and uses the general RSSWidget if no match is made.
- **News Widget**: performs search of Google News for specified terms and returns post
- Reddit Widget: performs search of specified subreddit for articles. * Note that this functionality requires obtaining Reddit API credentials.
- **Udemy Widget**: specialized form of Redit widget which identifies links to Udemy courses with discount coupons. It will follow link to identify the Udemy url and coupon code. It also requires Reddit API credentials.
- **QuoteWidget**: POC functionality to post random quotes from random people.

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

# use and configuration
This bot runs on a continuous loop with actions occuring at randomized intervals. Run the bot with the command below. Note that parameters must be specified unless default filenames are used (*for example, if you include files with the names indicated, then parameters will be automatically loaded from these files.*)
```
python go_bot.py [parameters]
-af [auth file] env.json
-cf [config file] config.json
-sf [sources file] sources.json
```

## The following are required parameters:
- **auth file (env.json)**: This file inclues the credentials for twitter and (if applicable) reddit accounts. This will load automatically if named env.json, or it can be specified with the -af pamater in the following format:
```
{
"API_KEY":"***",
"API_SECRET_KEY":"***",
"ACCESS_TOKEN":"***-***",
"ACCESS_TOKEN_SECRET":"***",
"REDDIT_CLIENT_ID":"***",
"REDDIT_CLIENT_SECRET":"***"
}
```

- **config file (config.json)**: This file includes parameters for 
```
{
"hashtags": "#news",
"interval": "20",
"randomization": "50",
"waketime": "5",
"bedtime": "21",
"timezone": "America/Los_Angeles",
"min_pop": "1000",
"character": "default",
"mode": "interval",
"behaviors":"tweet chat",
"username": "@username",
"userid": "userid"
}
```

- **sources file (sources.json)**: This file includes all of the sources for behaviors in the following format.
```
[{
"name": "news",
"type": "news",
"frequency":"20",
"terms":"tech or technology",
"addtags":"#news"
}
...
]
```

# Getting credentials:
You will need to get credentials from Twitter for this bot to be able to analyze and send posts and messages. You will additionally need to obtain Reddit credentials for use of the Reddit and Udemy widgets.

## Twitter credentials
1. Visit this link to apply for developer credentials.
    - https://developer.twitter.com/en/apply-for-access
2. Once you receive access, visit the Developer dashboard and create an app 
    - https://developer.twitter.com/en/portal/dashboard
    - *Note that apps are just placeholders for apps with access to your account*
    - *Also note that the name you choose for your app will show up as your Twitter client on all of your tweets from this bot. So choose something fun*
3. Once your app is setup, visit the dashboard, go to the bot and click the key symbol next to the app name. This will take you to 'Keys and tokens'.
    - Under **Consumer Keys**, click the **Regenerate** button next to 'API Key and Secret'. This will open a dialog box where you can download your keys.
    - Under Authentication Tokens, click the 'Regenerate' button next to the Access Token and Secret. This will open a dialog box where you can download your access token and secret.

# dependencies
- Synchron - this library includes widgets for interacting with social media sources
- AverageJoe - this library includes scheduling functions. It is parameterized on load, including the waketime, bedtime, interval and randomization.
- BasicBot - this library includes basic functions for running bots.