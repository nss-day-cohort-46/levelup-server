"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Game
from levelupreports.views import Connection

def usergame_list(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
            g.id,
            g.title,
            g.maker,
            g.game_type_id,
            g.skill_level,
            g.number_of_players,
            u.id user_id,
            u.first_name || ' ' || u.last_name as full_name
            from levelupapi_game g
            join levelupapi_gamer gr on g.gamer_id = gr.id
            join auth_user u on gr.user_id = u.id
            """)

            dataset = db_cursor.fetchall()

            games_by_user = {}

            for row in dataset:
                game = Game()
                game.title = row['title']
                game.maker = row['maker']
                game.skill_level = row['skill_level']
                game.number_of_players = row['number_of_players']
                game.game_type_id = row['game_type_id']

                uid = row['user_id']

                if uid in games_by_user:
                    games_by_user[uid]['games'].append(game)
                else:
                    games_by_user[uid] = {}
                    games_by_user[uid]['id'] = uid
                    games_by_user[uid]['full_name'] = row['full_name']
                    
                    games_by_user[uid]['games'] = [game]
            list_of_users_with_games = games_by_user.values()

            template = 'users/list_with_games.html'
            context = {
                'usergame_list': list_of_users_with_games,
                'title': 'Users with Games'
            }

            return render(request, template, context)


