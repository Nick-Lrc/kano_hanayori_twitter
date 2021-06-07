import os
from data_loader import load_user, load_tweets
from common import add_classes, get_hyperlink_tag
from user import User
from tweet import Tweet

BANNER_PATH = 'data/media/banner.jpeg'
AVATAR_PATH = 'data/media/avatar.jpg'
EXPORT_PATH = os.path.join('..', 'kano_hanayori_twitter.html')

def write_doctype(file):
    file.write('<!DOCTYPE html>\n')

def write_html_start(file):
    file.write('<html>\n')

def write_html_end(file):
    file.write('</html>\n')

def write_head_start(file):
    file.write('<head>\n')

def write_head_end(file):
    file.write('</head>\n')

def write_charset(file, charset='utf-8'):
    file.write(f'<meta charset="{charset}">\n')

def write_viewport(file):
    file.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')

def write_stylesheet(file, path):
    file.write(f'<link rel="stylesheet" href="{path}">\n')

def write_script(file, path):
    file.write(f'<script src="{path}"></script>\n')

def write_title(file, title):
    file.write(f'<title>{title}</title>\n')

def write_head(file, title):
    write_head_start(file)
    write_charset(file)
    write_viewport(file)
    write_stylesheet(file, 'src/style/css/bootstrap.min.css')
    write_stylesheet(file, 'src/style/css/custom.css')
    write_script(file, 'src/style/js/jquery.min.js')
    write_script(file, 'src/style/js/popper.min.js')
    write_script(file, 'src/style/js/bootstrap.min.js')
    write_title(file, title)
    write_head_end(file)

def write_body_start(file, classes=[]):
    file.write(f'<body{add_classes(classes)}>\n')

def write_body_end(file):
    file.write('</body>\n')

def write_div_start(file, classes=[]):
    file.write(f'<div{add_classes(classes)}>\n')

def write_div_end(file):
    file.write('</div>\n')

def write_img(file, path, description, classes=[]):
    file.write(f'<img src="{path}" alt="{description}"{add_classes(classes)}>\n')

def write_heading(file, text, size=1, classes=[]):
    tag = f'h{size}'
    file.write(f'<{tag}{add_classes(classes)}>{text}</{tag}>\n')

def write_span(file, text, classes=[]):
    file.write(f'<span{add_classes(classes)}>{text}</span>\n')

def write_paragraph(file, text, classes=[]):
    file.write(f'<p{add_classes(classes)}>{text}</p>\n')

def write_horizontal_rule(file):
    file.write('<hr>\n')

def write_user(file, user):
    write_div_start(file, classes=['shadow'])
    write_img(file, BANNER_PATH, 'kano hanayori banner', classes=['img-fluid', 'border-bottom'])
    write_div_start(file, classes=['media', 'p-3'])
    write_img(file, AVATAR_PATH, 'kano hanayori avatar', 
              classes=['rounded-circle', 'border', 'mr-3', 'avatar-profile'])
    write_div_start(file, classes=['media-body'])
    write_heading(file, user.name, size=2, classes=['font-weight-bold'])
    write_span(file, user.profile, classes=['text-secondary'])
    write_paragraph(file, user.description)
    write_div_end(file)
    write_div_end(file)
    write_div_end(file)

def write_tweet(file, user, tweet):
    write_div_start(file, classes=['media', 'p-3'])
    write_img(file, AVATAR_PATH, 'kano hanayori avatar', 
              classes=['rounded-circle', 'border', 'mr-3', 'avatar'])
    write_div_start(file, classes=['media-body'])
    write_span(file, user.name, classes=['font-weight-bold'])
    write_span(file, f' / {tweet.date}{tweet.link}', classes=['text-secondary'])
    write_paragraph(file, tweet.text)
    for img in tweet.imgs:
        file.write(f'{img}\n')
    write_div_end(file)
    write_div_end(file)

def write_ending(file):
    write_div_start(file)
    write_paragraph(file, get_hyperlink_tag('https://twitter.com/kanomahoro', 'つづく'), classes=['text-center'])
    write_div_end(file)

if __name__ == '__main__':
    out = open(EXPORT_PATH, 'w', encoding='utf-8')
    user = User(load_user())
    tweets = load_tweets()

    write_doctype(out)
    write_html_start(out)
    write_head(out, user.name)

    write_body_start(out)
    write_div_start(out, classes=['container'])
    write_user(out, user)
    write_div_start(out, classes=['mt-4'])

    for tid, data in sorted(tweets.items()):
        tweet = Tweet(tid, data)
        write_tweet(out, user, tweet)
        write_horizontal_rule(out)
    write_ending(out)

    write_div_end(out)
    write_div_end(out)
    write_body_end(out)

    write_html_end(out)
    out.close()
    