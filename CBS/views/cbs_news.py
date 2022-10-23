import json
from bs4 import BeautifulSoup
import requests
from flask import Blueprint, request, redirect, render_template
from CBS.models import CBSNews

cbsviews = Blueprint('cbsviews', __name__)

def get_cbs_news():
    url = "https://www.cbsnews.com/latest/rss/main"
    response = requests.get(url)

    data = []

    doc = BeautifulSoup(response.text, 'features="xml"')

    rows = doc.find_all('item', class_ = 'line')

    for row in rows:
        #extract title, link,image_link and description
        title = row.find('span', class_ = 'html-tag').find('title').text
        link = row.find('span', class_ = 'html-tag').find('link')['href']
        description = row.find('span', class_ = 'html-tag').find('description').text
        image = row.find('span', class_ = 'html-tag').find('image')['href']

        data.append({
            'title': title,
            'link': link,
            'description': description,
            'image': image
        })

    return data

# get_cbs_news()

@cbsviews.route('/cbs_news', methods=['GET', 'POST', 'PUT'])
def cbs_news():
    if request.method == 'POST':      
        return redirect('/')

    # new data from cbs news
    data = get_cbs_news()

    # existing data from database
    cbsnews = CBSNews.get_cbs_news()

    # loop through data
    for news in data:
        # check if news already exists in database
        if news.get('title').lower() not in [cbsn.title.lower() for cbsn in cbsnews]:
            cbsnew = CBSNews(title=news['title'], link=news['link'], description=news['description'], image = news['image'])
            cbsnew.save()
        else:
            continue

    return render_template('cbs_news.html', data=cbsnews)

    






