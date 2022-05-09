import uuid
import json

import mysql.connector
from flask import Flask, redirect, render_template, request
import plotly.express as px
import pandas as pd

def create_multilink(request, mydb):
    print(request.form)
    page_name = request.form['page_name_0']
    links = request.form.to_dict()
    print(links)
    links = json.dumps(links, ensure_ascii=False)

    hash = uuid.uuid4().hex[:6]
    username = 'site'

    cursor = mydb.cursor()
    cursor.execute(f"""INSERT treelinks(link_id, name,  link, username)
         VALUES ('{hash}','{page_name}', '{links}', '{username}')""")
    mydb.commit()
    cursor.close()
    return hash


def parse_multilink(mydb, link_id):
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM treelinks"
                     f" where link_id = '{link_id}'")
    myresult = mycursor.fetchall()
    mycursor.close()
    if len(myresult) == 0:
        return '<h3>Нет такой мульти ссылки</h3>'


    print(myresult)
    desc = 'Описание страницы'
    page_name = myresult[0][2]
    elements = json.loads(myresult[0][1])

    link_names, links = [], []
    good_names, good_descs, good_prices, good_link_buys = [], [], [], []
    for el in elements:
        print(el)
        if el[:9] == 'link_name':
            link_names.append(elements[el])
        elif el[:4] == 'link':
            links.append(elements[el])
        elif el[:4] == 'desc':
            desc = elements[el]
        elif el[:9] == 'good_name':
            good_names.append(elements[el])
        elif el[:9] == 'good_desc':
            good_descs.append(elements[el])
        elif el[:10] == 'good_price':
            good_prices.append(elements[el])
        elif el[:13] == 'good_link_buy':
            good_link_buys.append(elements[el])
    dict_links = dict(zip(link_names, links))
    dict_goods = {i: [j, k, s, h] for i, j, k, s, h in zip(range(len(good_names)), good_names, good_descs, good_prices, good_link_buys)}
    print(dict_links)
    print(dict_goods)
    return page_name, desc, dict_goods, dict_links