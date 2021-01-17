from options import getOpts
import requests
import json
from bs4 import BeautifulSoup
options = getOpts()

limit = options['limit']
base_url = options['domain_name']
output_dir = options['out_dir']


class NyaaTorrent:
    def __init__(self, link):
        self.link = link
        self.html = requests.get(
            self.link, headers={'User-Agent': 'NyaaDatabaseIndexer/1.0'}).text
        self.soup = BeautifulSoup(self.html, 'html.parser')

    @property
    def title(self):
        return self.soup.select_one('h3.panel-title').text.strip()

    @property
    def submitter(self):
        return self.soup.select_one(
            "a[title='User']").text

    @property
    def categories(self):
        return [{'name': x.text, 'link': x['href']} for x in self.soup.find('div', class_='row').find_next(
            'div', class_='col-md-5').select('a')]

    @property
    def information(self):
        return self.soup.select('div.row')[2].find('a').text

    @property
    def file_size(self):
        return self.soup.select('div.row')[3].select('div')[1].text

    @property
    def date_added(self):
        return self.soup.select_one('div.row').select('div')[-1]['data-timestamp']

    @property
    def seeders(self):
        return self.soup.find('span', style='color: green;').text

    @property
    def leechers(self):
        return self.soup.find('span', style='color: red;').text

    @property
    def completed(self):
        return self.soup.select('div.row')[3].select('div')[-1].text

    @property
    def infohash(self):
        return self.soup.find('kbd').text

    @property
    def torrent_file(self):
        return 'https://nyaa.si' + self.soup.select_one('div.panel.panel-default').select('a')[-2]['href']

    @property
    def magnet(self):
        return self.soup.select_one('div.panel.panel-default').select('a')[-1]['href']

    @property
    def description(self):
        return self.soup.select_one('div#torrent-description').text

    @property
    def comments(self):
        comments = self.soup.select_one('div#comments').select(
            'div.panel.panel-default.comment-panel')
        comments = [
            {
                'UserObject': {
                    'name': x.find('p').text.replace('(uploader)', '').strip(),
                    'link': 'https://nyaa.si' + x.find('p').a['href'],
                    'avatar': x.select_one('img.avatar')['src'],
                    'timestamp': x.select_one('small')['data-timestamp'],
                    'is_uploader': True if '(uploader)' in x.find('p').text else False
                },
                'Comment': {
                    'content': x.select_one('div.comment-content').text,
                    'commentId': x.select_one('div.comment-content')['id']
                }
            }
            for x in comments
        ]
        return comments

    @property
    def comments_count(self):
        return len(self.comments)


g = NyaaTorrent('https://nyaa.si/view/1328642')
print(json.dumps(g.comments, indent=4))
