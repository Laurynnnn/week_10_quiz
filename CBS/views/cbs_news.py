import json
from bs4 import BeautifulSoup
import requests
from flask import Blueprint, request, redirect, render_template
from CBS.models import CBSNews
from lmxl import *
import sqlite3 as sql

cbsviews = Blueprint('cbsviews', __name__)

def get_cbs_news():
    url = "https://www.cbsnews.com/latest/rss/main"
    response = requests.get(url)

    data = []

    doc = BeautifulSoup(page, 'html.parser' 'features="xml"')

    rows = doc.find_all('channel', class_ = 'line')

    for row in rows:
        #extract title, link,image_link and description
        title = row.find('span', class_ = 'opened').find('title').text
        link = row.find('span', class_ = 'opened').find('link')['href']
        description = row.find('span', class_ = 'opened').find('description').text
        image = row.find('span', class_ = 'opened').find('image')['href']

        data.append({
            'title': title,
            'link': link,
            'description': description,
            'image': image
        })

    return data

# get_cbs_news()

@cbsviews.route('/cbs_news', methods=['GET', 'POST', 'UPDATE'])
def cbs_news():
    if request.method == 'POST':
        conn = sql.connect('cbs.db')
        conn.execute('CREATE TABLE cbs_news(title TEXT, link STRING, description TEXT, image STRING')

        cur = conn.cursor()
        cur.execute("INSERT INTO cbs_news (title, link, description, image) VALUES (?, ?, ?, ?)", (title, link, description, image))

        conn.commit()
        
        return redirect('/')
        conn.close()

    # new data from cbs news
    data = get_cbs_news()

    # existing data from database
    cbsnews = CBSNews.get_all_news()

    # # loop through data
    # for news in data:
    #     # check if news already exists in database
    #     if news.get('title').lower() not in [cbsn.title.lower() for cbsn in cbsnews]:
    #         cbsnew = CBSNews(title=news['title'], link=news['link'])
    #         cbsnew.save()
    #     else:
    #         continue

    # return render_template('cbs_news.html', data=cbsnews)

    #getting data from database
    con = sql.connect("cbs.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * from cbs_news")

    rows = cur.fetchall()
    return render_template('cbs_news.html', rows=rows)







