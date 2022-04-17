import mysql.connector
from flask import Flask, redirect, render_template, request
import uuid
import json

application = Flask(__name__)

mydb = mysql.connector.connect(
  database='u1650045_default',
  host="cutlinks_local.ru",
  user="u1650045_default",
  password="mqGIBF31HU1x8zxo"
)


@application.route('/')
def hello():
    return render_template('design.html')


@application.route('/shortlink')
def shortlink():
    return render_template('shortlink.html')


@application.route('/multilink')
def multilink():
    return render_template('multilink.html')


def cut(link_id):
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM links where link_id = '{link_id}'")
    myresult = mycursor.fetchall()
    mycursor.close()
    if len(myresult) == 0:
        return '<h3>Нет такой короткой ссылки</h3>'
    return redirect(myresult[0][1], code=302)


def tree(link_id):
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM treelinks where link_id = '{link_id}'")
    myresult = mycursor.fetchall()
    mycursor.close()
    if len(myresult) == 0:
        return '<h3>Нет такой мульти ссылки</h3>'
    print(myresult)
    # links = json.loads(myresult[0][1])
    return render_template('profile.html', name=myresult[0][2], links=json.loads(myresult[0][1]))



@application.route("/<link_id>")
def multiple(link_id):
    cursor = mydb.cursor()
    cursor.execute(f"""INSERT clicks(link) VALUES ('{link_id}')""")
    mydb.commit()
    cursor.close()

    if len(link_id) == 4:
        return cut(link_id)
    else:
        return tree(link_id)



@application.route('/your_short_link', methods=['POST', 'GET'])
def your_short_link():
    link = request.form['link']
    hash = uuid.uuid4().hex[:4]
    username = 'site'

    cursor = mydb.cursor()
    cursor.execute(f"""INSERT links(link_id, link, username) VALUES ('{hash}', '{link}', '{username}')""")
    mydb.commit()
    cursor.close()

    return render_template('shortlink.html', forward_message=f'http://cutlinks.ru/{hash}')


@application.route('/your_tree_link', methods=['POST', 'GET'])
def your_tree_link():
    name = request.form['name']
    num_of_links = len(request.form) // 2
    links = {}

    for num in range(1, num_of_links+1):
        links[request.form['name'+str(num)]] = request.form['link'+str(num)]

    links = json.dumps(links)
    hash = uuid.uuid4().hex[:6]
    username = 'site'

    cursor = mydb.cursor()
    cursor.execute(f"""INSERT treelinks(link_id, name,  link, username)
     VALUES ('{hash}','{name}', '{links}', '{username}')""")
    mydb.commit()
    cursor.close()

    return render_template('multilink.html', forward_message=f'http://cutlinks.ru/{hash}')




if __name__ == '__main__':
    application.run(host='0.0.0.0')