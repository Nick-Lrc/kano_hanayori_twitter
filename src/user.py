import urllib.parse
from common import get_hashtag_hyperlink, get_mention_hyperlink, get_hyperlink_tag, hyperlink_text

def get_hashtag_hyperlinks(description, hashtags):
    links = {}
    for hashtag in hashtags:
        hashtag = description[hashtag['start']:hashtag['end']]
        links[hashtag] = get_hashtag_hyperlink(hashtag)
    return links
        
def get_mention_hyperlinks(description, mentions):
    links = {}
    for mention in mentions:
        mention = description[mention['start']:mention['end']]
        links[mention] = get_mention_hyperlink(mention)
    return links

class User:
    def __init__(self, data):
        self.uid = next(iter(data))
        user = data[self.uid]
        self.name = user['name']
        self.username = user['username']
        self.profile = get_hyperlink_tag(get_mention_hyperlink(self.username), f'@{self.username}')
        description = user['description']
        hyperlinks = get_hashtag_hyperlinks(description, user['urls']['hashtags'])
        hyperlinks.update(get_mention_hyperlinks(description, user['urls']['mentions']))
        self.description = hyperlink_text(description, hyperlinks)
