CONFIG = """
{
"settings": {
"hashtags": "#science #news",
"interval": "30",
"randomization": "50",
"waketime": "5",
"bedtime": "20",
"timezone": "America/Los_Angeles",
"min_pop": "1000",
"character": "default",
"mode": "interval",
"username": "@GenomeOrganizer",
"userid": "294438257"
},
"sources": [{
"name": "twitter",
"type": "twitter",
"frequency": "10",
"terms": "#science OR #tech OR #googlecloud OR #genomics OR #genetics OR bioinformatics OR #dinosaurs OR #sequencing OR RNA OR ngs OR Illumina OR personalis OR natera OR pacbio OR wgs OR @genomeweb OR #medicine OR @sequencecentral",
"addtags": "#science #news"
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
"frequency":"15",
"terms":"covid19 or technology",
"addtags":"#news"
},
{
"name": "reddit",
"type": "reddit",
"frequency":"45",
"terms":"science memes datascience computerscience health UpliftingNews fascinating covid19",
"addtags":"#tech"
},
{
"name": "genomics",
"type": "rss",
"frequency":"10",
"terms":"genomics",
"addtags":"#science #genomics"
},
{
"name": "covid19",
"type": "rss",
"frequency":"20",
"terms":"covid19",
"addtags":"#covid19"
},
{
"name": "techcrunch",
"type": "rss",
"frequency":"5",
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
"frequency":"0",
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

