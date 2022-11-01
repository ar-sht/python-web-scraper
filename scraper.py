import requests
import string
from bs4 import BeautifulSoup
import os

num_pages, article_classification = int(input()), input()

for i in range(1, num_pages + 1):
    url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i}"
    response = requests.get(url)

    if response:
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = [[article_type, link] for (article_type, link) in zip(soup.find_all('span', {'data-test': 'article.type'}), soup.find_all('a', {'data-track-action': 'view article'})) if article_type.text.strip() == article_classification]

        dir_name = f"Page_{i}"

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        os.chdir(dir_name)

        file_names = []
        for article in articles:
            file_title = article[1].text.strip().replace('’', '')
            for punctuation in string.punctuation:
                file_title = file_title.replace(punctuation, '')
            file_title = file_title.replace(' ', '_')
            file_title += '.txt'
            file_names.append(file_title)

            article_page = requests.get('https://nature.com' + article[1].get('href'))
            article_soup = BeautifulSoup(article_page.content, 'html.parser')

            article_body = article_soup.find('div', {'class': 'c-article-body main-content'})
            if article_body:
                article_body = article_body.text.strip()
                with open(file_title, 'w', encoding='utf-8') as article_file:
                    article_file.write(article_body)
        os.chdir('..')
    else:
        print(f"The URL returned {response.status_code}!")

print('Saved all articles.')
