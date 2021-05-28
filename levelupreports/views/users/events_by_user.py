from django.shortcuts import render
from levelupreports.views import Connection
import sqlite3

def events_by_user(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path)as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select gr.id as gamer_id,
            u.first_name || ' ' || u.last_name as full_name,
            e.id as event_id,
            e.start_date,
            g.title
            from levelupapi_event e
            join levelupapi_gamer gr on e.organizer_id = gr.id
            join auth_user u on u.id = gr.user_id
            join levelupapi_game g on g.id = e.game_id
            """)

            dataset = db_cursor.fetchall()

            users_dict = {}

            for row in dataset:
                event = {
                    'id': row['event_id'],
                    'start_date': row['start_date'],
                    'game_name': row['title']
                }

                uid = row['gamer_id']

                if uid in users_dict:
                    users_dict[uid]['events'].append(event)
                else:
                    users_dict[uid] = {
                        'organizer_id': uid,
                        'full_name': row['full_name'],
                        'events': [event]
                    }

            list_of_users = list(users_dict.values())

            # sort list_of_users

            template = 'users/list_with_events.html'
            context = {
                'event_host_list': list_of_users,
                'title': 'List of users hosted events'
            }

            return render(request, template, context)


