import os
import re
from datetime import datetime
from common import get_hashtag_hyperlink, get_mention_hyperlink, get_hyperlink_tag, hyperlink_text, add_classes

THUMBNAIL_SUFFIX = '_thumb'

def get_hashtag_hyperlinks(text):
    links = {}
    hashtags = re.findall(r'#(\w+)', text)
    for hashtag in hashtags:
        links[f'#{hashtag}'] = get_hashtag_hyperlink(hashtag)
    return links
        
def get_mention_hyperlinks(text):
    links = {}
    mentions = re.findall(r'@(\w+)', text)
    for mention in mentions:
        links[f'@{mention}'] = get_mention_hyperlink(mention)
    return links

def get_tweet_hyperlink(tid):
    return f'https://twitter.com/Kanolive_/status/{tid}'

def get_url_hyperlinks(text, urls):
    links = {}
    for url in urls:
        link = text[url['start']:url['end']]
        links[link] = url['expanded_url']
    return links

def get_img_tag(path, description, classes=[]):
    return f'<img src="{path}" alt="{description}"{add_classes(classes)}>'

def get_heading(text, size=1, classes=[]):
    tag = f'h{size}'
    return f'<{tag}{add_classes(classes)}>{text}</{tag}>'

def get_div_tag(text, classes=[]):
    return f'<div{add_classes(classes)}>\n{text}\n</div>'

def is_thumbnail(filename):
    return filename.endswith(THUMBNAIL_SUFFIX)

def hyperlink_img(img_path, media_hyperlink, classes=[]):
    img_tag = get_img_tag(img_path, media_hyperlink, classes=classes)
    inner_text = img_tag
    div_classes = []

    name, ext = os.path.splitext(os.path.normpath(img_path))
    if is_thumbnail(name):
        heading = get_heading('▶')
        inner_text += f'\n{heading}'
        div_classes = ['thumbnail']
    hyperlink_tag = get_hyperlink_tag(media_hyperlink, inner_text)
    return get_div_tag(hyperlink_tag, classes=div_classes)

def hyperlink_imgs(imgs, classes=[]):
    if not imgs:
        return []

    img_path, media_hyperlink = imgs[0]
    divs = [hyperlink_img(img_path, media_hyperlink, classes)]
    if len(imgs) > 1:
        classes.append('mt-3')
        for img_path, media_hyperlink in imgs[1:]:
            divs.append(hyperlink_img(img_path, media_hyperlink, classes))
    return divs

class Tweet:
    def __init__(self, tid, data):
        self.tid = tid
        self.link = get_hyperlink_tag(get_tweet_hyperlink(tid), f'#{tid}', classes=['float-right'])
        self.date = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') \
                            .strftime('%b %d, %Y %H:%M')
        text = data['text']
        hyperlinks = get_url_hyperlinks(text, data['urls'])
        hyperlinks.update(get_hashtag_hyperlinks(text))
        hyperlinks.update(get_mention_hyperlinks(text))
        self.text = hyperlink_text(text, hyperlinks)
        self.imgs = hyperlink_imgs(data['media'], classes=['img-fluid', 'rounded', 'border'])
