FILENAME = "posts.txt"

with open(FILENAME, "r", encoding="utf8") as f:
    lines = f.readlines()


posts: list[dict[str, str]] = []
curr_post = {}

for line in lines:
    patterns = [
        ('title', 'Tytuł:'),
        ('photos', 'Nazwa zdjęcia:'),
        ('description', 'Opis:'),
        ('date', 'Data:'),
        ('photos_count', 'Liczba zdjęć:'),
    ]
    for (dict_name, pattern) in patterns:
        if line.strip().startswith(pattern):
            if pattern == "Tytuł:":
                posts.append(curr_post)
                curr_post = {}
            curr_post[dict_name] = line.strip().removeprefix(pattern).strip()
    # print([line.startswith(pattern) for (_, pattern) in patterns])
    if not any([line.startswith(pattern) for (_, pattern) in patterns]):
        # print(line)
        curr_post['description'] += "\n\n" + line.strip()

posts = posts[1:]

def format_title(date, title):
    alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
    replace_dict = {
        ' ': '-',
        '.': '',
        ',': '',
        'ł': 'l',
        'ą': 'a',
        'ę': 'e',
        'ś': 's',
        'ć': 'c',
        'ż': 'z',
        'ź': 'z',
        'ó': 'o',
        '_': '-'
    }
    for alpha in alphabet:
        replace_dict[alpha] = alpha
    title = "".join([replace_dict[c] if c in replace_dict else '' for c in title.lower()])

    return date + '-' + title.lower().replace(' ', '-')

# print(posts)

# print([('date' in post, post['title']) for post in posts])
POST_DIR = '_posts/'

# Tytuł: Kongres Studentów i Absolwentów Psychologii w Murzasichle.
for post in posts:
    filename = format_title(post['date'], post['title']) + ".md"
    title = post['title']
    date = post['date']
    description = post['description']
    if 'photos' in post:
        photos = post['photos']
        photos_count = post['photos_count']
    else:
        photos = ''
        photos_count = 0
    content = f"""\
---
layout: post
title: {title}
image:
photos: "{photos}, count {photos_count}"
date: "{date}"
---
{description}
    """
    with open(POST_DIR + "/" + filename, "w") as f:
        f.write(content)
