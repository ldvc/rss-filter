#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 sw=4 ts=4 et :


from __future__ import (unicode_literals, absolute_import,
                        print_function, division)

import os
import re
import feedparser
import hashlib
import sqlite3
from PyRSS2Gen import RSS2, RSSItem
from datetime import datetime


XML = "https://www.dealabs.com/rss/hot.xml"
DATABASE = '/home/user/rss-filter/filtered-deals.sqlite'


def init_db():
    'DB initialization'
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deals(id INTEGER PRIMARY KEY,
        hash TEXT UNIQUE, title TEXT, url TEXT, description TEXT,
        pubDate TEXT)
    ''')
    conn.commit()
    conn.close()


def insert_item(t_hash, title, url, description, pubDate):
    'Insert elem in database'
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR IGNORE INTO
        deals(hash, title, url, description, pubDate)
        VALUES(?,?,?,?,?)''', (t_hash, title, url, description, pubDate))

    conn.commit()
    conn.close()
    return cursor


def create_rss():
    'Generate XML file'

    title = u'Dealabs, tous les deals hots - Filtrés'
    dest = "/var/www/example.org/lab/rss"
    url = "https://lab.example.org/rss/"
    filename = 'dealabs.xml'

    rss = RSS2(
        title = title.encode('utf-8'), link = os.path.join(url, filename),
        description = title.encode('utf-8'), lastBuildDate = datetime.now(),
        items = [ RSSItem(**article) for article in filter_deals() ]
    )
    rss.write_xml(open(os.path.join(dest, filename), "w"), encoding='utf-8')


def filter_deals():
    'Keep only some deals'

    feed = feedparser.parse(XML)
    c_deals = len(feed['entries'])
    print("%s items found in RSS feed." % c_deals)

    count = 0
    v_items = []
    filters = (
        u'Nintendo', u'T-Shirt enfant', u'XBOX One|360', u'jeux video',
        u'DVD', u'@ DX', u'onsole Xbox', u'@ Priceminister',
        u'Sélection de jeux', u'PS[34P]', u'Blu[\s-]?Ray', u'Steam',
        u'Wii', u'Playstation', u'@ Mcdonalds', u'@ Quick', u'@ action',
        u'@ Meccanodirect', u'sur 3DS??|PC', u'TV \d{2}"|\s?pouces')

    for elem in feed['entries']:
        is_match = False

        for f in filters:
            if re.search(f.encode('utf-8'), elem['title'].encode('utf-8'), re.I):
                is_match = True
                break

        if not is_match:
            deals = {}
            deals['title'] = elem['title']
            deals['description'] = elem['description']
            deals['link'] = elem['link']
            deals['pubDate'] = elem['published']

            t_hash = hashlib.md5(elem['title'].encode('utf-8')).hexdigest()

            conn = sqlite3.connect(DATABASE)

            cursor = conn.cursor()
            cursor.execute('''INSERT OR IGNORE INTO deals(hash, title, url,
                description, pubDate)
                VALUES(?,?,?,?,?)''', (
                    t_hash, elem['title'], elem['link'],
                    elem['description'], elem['published']))

            conn.commit()

            if cursor.rowcount > 0:
                v_items.append(deals)
                count += 1
            else:
                cursor.execute('''SELECT title, url, description, pubDate
                    FROM deals WHERE hash = ?;''', (t_hash, ))
                for title, url, description, pubDate in cursor:
                    deals['title'] = title
                    deals['link'] = url
                    deals['description'] = description
                    deals['pubDate'] = pubDate
                    v_items.append(deals)

    if count > 0:
        print("%s new items added." % (count, ))

    conn.close()
    return v_items


if __name__ == '__main__':
    if not os.path.isfile(DATABASE):
        init_db()

    create_rss()
