from bottle import route, run, template, static_file, request
import random
import json
import pymysql


@route("/", method="GET")
def index():
    return template("adventure.html")


@route("/start", method="POST")
def start():
    username = request.POST.get("user")
    adv_id = request.POST.get("adventure_id")

    CONNECTION = connection()

    try:
        with CONNECTION.cursor() as cursor:
            user_id_query = "SELECT * FROM users WHERE user_name = '{}' AND adventure_id = {};".format(username, adv_id)
            cursor.execute(user_id_query)
            user = cursor.fetchone()

            if user is None:
                user_add_query = "INSERT INTO users(user_name, adventure_id, stage, life, coins) VALUES ('{}', {}, 1, 100, 50);".format(username, adv_id)
                cursor.execute(user_add_query)
                CONNECTION.commit()

                user_id_query = "SELECT * FROM users WHERE user_name = '{}' AND adventure_id = {};".format(username, adv_id)
                cursor.execute(user_id_query)
                user = cursor.fetchone()

            question_query = "SELECT * FROM questions WHERE adventure_id = {} AND stage = {};".format(adv_id, user['stage'])
            cursor.execute(question_query)
            question = cursor.fetchone()

            options_query = "SELECT * FROM options WHERE question_id = {};".format(question['id'])
            cursor.execute(options_query)
            options = cursor.fetchall()

    except Exception as e:
        print('******ERROR******', e)


    return json.dumps({"user": user['user_name'],
                       "adventure": user['adventure_id'],
                       "stage": user['stage'],
                       "coins": user['coins'],
                       "life": user['life'],
                       "text": question['text'],
                       "image": question['image'],
                       "options": options})


@route("/story", method="POST")
def story():
    username = request.POST.get("user")
    adv_id = request.POST.get("adventure")
    stage = request.POST.get("stage")
    choice = request.POST.get("choice")

    CONNECTION = connection()

    try:
        with CONNECTION.cursor() as cursor:
            chosen_opt_query = "SELECT coin_loss, life_loss FROM options WHERE choice = {} AND question_id = (SELECT id FROM questions WHERE adventure_id = {} AND stage = {});".format(choice, adv_id, stage)
            cursor.execute(chosen_opt_query)
            life_and_coins = cursor.fetchone()

            user_update_query = "UPDATE users SET stage = {} - 1, life = life - {}, coins = coins - {} WHERE user_name = '{}' AND adventure_id = {};".format(stage, life_and_coins['life_loss'], life_and_coins['coin_loss'], username, adv_id)
            cursor.execute(user_update_query)
            CONNECTION.commit()

            user_id_query = "SELECT * FROM users WHERE user_name = '{}' AND adventure_id = {};".format(username, adv_id)
            cursor.execute(user_id_query)
            user = cursor.fetchone()

            question_query = "SELECT * FROM questions WHERE adventure_id = {} AND stage = {};".format(adv_id, user['stage'])
            cursor.execute(question_query)
            question = cursor.fetchone()

            options_query = "SELECT * FROM options WHERE question_id = {};".format(question['id'])
            cursor.execute(options_query)
            options = cursor.fetchall()

    except Exception as e:
        print('******ERROR******', e)

    return json.dumps({"user": user['user_name'],
                       "adventure": user['adventure_id'],
                       "stage": user['stage'],
                       "coins": user['coins'],
                       "life": user['life'],
                       "text": question['text'],
                       "image": question['image'],
                       "options": options})


def connection():
    return  pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='Adventure',
        cursorclass=pymysql.cursors.DictCursor)            


@route('/js/<filename:re:.*\.js$>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='localhost', port=9000)

if __name__ == '__main__':
    main()

