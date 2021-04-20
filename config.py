CONFIG = """
{
	"settings": {
		"hashtags": "#news",
		"interval": "30",
		"randomization": "50",
		"waketime": "5",
		"bedtime": "20",
		"timezone": "America/Los_Angeles",
		"min_pop": "100",
		"character": "default",
		"mode": "interval",
		"username": "@GenomeOrganizer",
		"userid": "294438257"
	},
	"sources": [{
            "name": "twitter",
            "type": "twitter",
            "frequency": "10",
            "terms": "@nytimestech OR @WIRED OR @isc2 OR @MalwareJake OR #science OR #cybersecurity OR #infosec OR #security OR #ransomware OR #hack OR #appsec OR #devsecops OR #devops OR  #ccsp OR #cissp OR #MSExchange OR #encryption OR OWASP OR #udemy OR udemy OR #udemyfreebies OR #udemycoupon OR #udemyfreebie OR #udemyfree OR #udemysale OR #udemyflashsale",
            "addtags": "#genomics OR #genetics OR #science OR #python OR cybersecurity OR infosec OR bitcoin OR crypto OR cryptocurrency OR monero OR  #retweet OR #like OR #follow OR #love  OR #twitter OR #repost OR #instagram OR #followme OR #share OR #tweet OR #likeforlikes OR #followback OR #k OR #likes OR #viral OR #tweets OR #likeforfollow"
        },
		{
			"name": "quote",
			"type": "quote",
            "frequency":"1",
            "terms":" ",
            "addtags":"#quotes"
		},
		{
			"name": "news",
			"type": "news",
            "frequency":"5",
            "terms":"tech or technology",
            "addtags":"#news"
		},
		{
			"name": "reddit",
			"type": "reddit",
            "frequency":"45",
            "terms":"science technology cybersecurity",
            "addtags":"#tech"
		},
		{
			"name": "genomics",
			"type": "rss",
            "frequency":"0",
            "terms":"genomics",
            "addtags":"#science #genomics"
		},
		{
			"name": "covid19",
			"type": "rss",
            "frequency":"0",
            "terms":"covid19",
            "addtags":"#covid19"
		},
		{
			"name": "techcrunch",
			"type": "rss",
            "frequency":"20",
            "terms":"techcrunch",
            "addtags":"#tech"
		},
		{
			"name": "techstartups",
			"type": "rss",
            "frequency":"10",
            "terms":"techstartups",
            "addtags":"#tech"
		},
		{
			"name": "udemy",
			"type": "udemy",
            "frequency":"16",
            "terms":"udemy",
            "addtags":"#udemy #udemyfreebies"
		}
	]
}
"""

HASHTAGS="#news"
INTERVAL=30
RANDOMIZATION=50
WAKETIME=5
BEDTIME=20
TIMEZONE='America/Los_Angeles'
MIN_POP=100
CHARACTER='default'
MODE='interval'
USERNAME="@GenomeOrganizer"
USERID="294438257"

QUERY_STRING="#genomics OR #genetics OR #science OR #python OR cybersecurity OR infosec OR bitcoin OR crypto OR cryptocurrency OR monero OR  #retweet OR #like OR #follow OR #love  OR #twitter OR #repost OR #instagram OR #followme OR #share OR #tweet OR #likeforlikes OR #followback OR #k OR #likes OR #viral OR #tweets OR #likeforfollow"
QUOTES_PERCENT=1
NEWS_PERCENT=1
NEWS_TOPIC='cybersecurity OR security OR infosec OR ransomware OR tech'
REDDIT_PERCENT=90
SUBREDDIT= 'science technology cybersecurity'
GENOMICS_PERCENT=1
COVID19_PERCENT=1
TECHCRUNCH_PERCENT=1
TECHSTARTUP_PERCENT=1
UDEMY_PERCENT=1

#old:
FOLLOW="294438257"
RESULT_TYPE="mixed"
TWITTER_LANG="en"
TWITTER_RETWEET_RATE=.1
TWITTER_SEARCH_COUNT=20
TWITTER_LIKE_RATE=1
TWITTER_QUOTE_RATE=1
TWITTER_SEARCH_COUNT=1
# BEARER_TOKEN=`AAAAAAAAAAAAAAAAAAAAAIXSNwEAAAAAW7Wf5RncBEhx1pwMhVeEDQtHX2c%3DpIgtzwPNRUA1BEmJnqpHzZvJXyRwPMCp1AMBtpr0Zgc2jGYgnV`

