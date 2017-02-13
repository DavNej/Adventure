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
            #Fetch user in DB
            user_id_query = """
            SELECT *
            FROM users 
            WHERE user_name = '{}' AND adventure_id = {};
            """.format(username, adv_id)
            cursor.execute(user_id_query)
            user = cursor.fetchone()

            if user is None:
                #Create user in DB
                user_add_query = """
                INSERT INTO users(user_name, adventure_id, stage, life, coins) 
                VALUES ('{}', {}, 1, 100, 50);
                """.format(username, adv_id)
                cursor.execute(user_add_query)
                CONNECTION.commit()

                #Fetch new user in DB
                user_id_query = """
                SELECT * 
                FROM users 
                WHERE user_name = '{}' AND adventure_id = {};
                """.format(username, adv_id)
                cursor.execute(user_id_query)
                user = cursor.fetchone()

            #Fetch question #1 in DB
            question_query = """
            SELECT * 
            FROM questions 
            WHERE adventure_id = {} AND stage = {};
            """.format(adv_id, user['stage'])
            cursor.execute(question_query)
            question = cursor.fetchone()

            #Fetch options for Q#1 in DB
            options_query = """
            SELECT * 
            FROM options 
            WHERE question_id = {};
            """.format(question['id'])
            cursor.execute(options_query)
            options = cursor.fetchall()

            return json.dumps({
                "user": user['user_name'],
                "adventure": user['adventure_id'],
                "stage": user['stage'],
                "coins": user['coins'],
                "life": user['life'],
                "text": question['text'],
                "image": question['image'],
                "options": options})

    except Exception as e:
        print('******ERROR******', e)


@route("/story", method="POST")
def story():
    username = request.POST.get("user")
    adv_id = request.POST.get("adventure")
    stage = request.POST.get("stage")
    choice = request.POST.get("choice")

    CONNECTION = connection()

    try:
        with CONNECTION.cursor() as cursor:
            #Fetch life and coins costs for chosen option in DB
            chosen_opt_query = """
            SELECT coin_loss, life_loss 
            FROM options 
            WHERE choice = {} AND question_id = (
                SELECT id 
                FROM questions 
                WHERE adventure_id = {} AND stage = {}-1);
            """.format(choice, adv_id, stage)
            cursor.execute(chosen_opt_query)
            life_and_coins = cursor.fetchone()

            #update scores in DB
            user_update_query = """
            UPDATE users 
            SET stage = {}, life = life - {}, coins = coins - {} WHERE user_name = '{}' AND adventure_id = {};
            """.format(stage, life_and_coins['life_loss'], life_and_coins['coin_loss'], username, adv_id)
            cursor.execute(user_update_query)
            CONNECTION.commit()

            #fetch user new stats
            user_id_query = """
            SELECT * 
            FROM users 
            WHERE user_name = '{}' AND adventure_id = {};
            """.format(username, adv_id)
            cursor.execute(user_id_query)
            user = cursor.fetchone()

            #End of game
            if stage == '4' or user['coins'] <= 0 or user['life'] <= 0:
                end = end_of_game(user)

                #reset user stats
                user_update_query = """
                UPDATE users 
                SET stage = 1, life = 100, coins = 50 WHERE user_name = '{}' AND adventure_id = {};
                """.format(username, adv_id)
                cursor.execute(user_update_query)
                CONNECTION.commit()

                return json.dumps(end)

            question_query = """
            SELECT * 
            FROM questions 
            WHERE adventure_id = {} AND stage = {};
            """.format(adv_id, user['stage'])
            cursor.execute(question_query)
            question = cursor.fetchone()

            options_query = "SELECT * FROM options WHERE question_id = {};".format(question['id'])
            cursor.execute(options_query)
            options = cursor.fetchall()

            return json.dumps({
                "user": user['user_name'],
                "adventure": user['adventure_id'],
                "stage": user['stage'],
                "coins": user['coins'],
                "life": user['life'],
                "text": question['text'],
                "image": question['image'],
                "options": options})

    except Exception as e:
        print('******ERROR******', e)


def connection():
    return  pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='Adventure',
        cursorclass=pymysql.cursors.DictCursor)

def end_of_game(user_info):
    if user_info['life'] <= 0:
        return {
            "end": True,
            "title": "You are dead!",
            "msg": "May G protect you up above...",
            "image": "rip.jpg"
        }
    if user_info['coins'] <= 0:
        return {
            "end": True,
            "title": "Sorry, you are broke!",
            "msg": "You lost all your precious coins...",
            "image": "broke.png"
        }
    else:
        return {
            "end": True,
            "title": "Congratulations! You won!",
            "msg": "You went through this wonderfull journey with success! :)",
            "image": "fireworks.gif"
        }

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
    run(host='localhost', port=8080)

if __name__ == '__main__':
    main()
