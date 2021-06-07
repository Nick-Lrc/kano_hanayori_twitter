import urllib.parse

def get_hashtag_hyperlink(hashtag):
    escaped_hashtag = urllib.parse.quote_plus(hashtag)
    return f'https://twitter.com/search?q={escaped_hashtag}&src=hashtag_click'

def get_mention_hyperlink(mention):
    username = mention.replace('@', '', 1)
    return f'https://twitter.com/{username}'

def get_hyperlink_tag(hyperlink, text, classes=[]):
    return f'<a href="{hyperlink}" target="_blank"{add_classes(classes)}>{text}</a>'

def hyperlink_text(text, hyperlinks):
    for key, hyperlink in hyperlinks.items():
        hyperlink_tag = get_hyperlink_tag(hyperlink, key)
        text = text.replace(key, hyperlink_tag)
    return text

def add_classes(classes):
    if classes:
        return f' class="{" ".join(classes)}"'
    return ''