import json
from levelupapi.models.game import Game
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType


class GameTests(APITestCase):
    def setUp(self):
        url = '/register'
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        # response.status_code == status.HTTP_201_CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        game_type = GameType()
        game_type.label = "Board Game"
        game_type.save()

        self.game = Game()
        self.game.game_type_id = 1
        self.game.skill_level = 5
        self.game.title = "Monopoly"
        self.game.maker = "Milton Bradley"
        self.game.number_of_players = 4
        self.game.gamer_id = 1

        self.game.save()

    def test_create_game(self):
        url = '/games'

        data = {
            "gameTypeId": 1,
            "skillLevel": 5,
            "title": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json_response = json.loads(response.content)

        self.assertEqual(json_response['title'], data['title'])
        self.assertEqual(json_response['maker'], data['maker'])
        self.assertEqual(json_response['skill_level'], data['skillLevel'])
        self.assertEqual(json_response['number_of_players'], data['numberOfPlayers'])

    def test_get_game(self):
        

        response = self.client.get(f'/games/{self.game.id}')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response['title'], self.game.title)
        self.assertEqual(json_response['maker'], self.game.maker)
        self.assertEqual(json_response['skill_level'], self.game.skill_level)
        self.assertEqual(json_response['number_of_players'], self.game.number_of_players)

    def test_change_game(self):
        data = {
            "gameTypeId": 1,
            "skillLevel": 2,
            "title": "Sorry",
            "maker": "Hasbro",
            "numberOfPlayers": 4
        }

        response = self.client.put(f'/games/{self.game.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/games/{self.game.id}')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response['title'], data['title'])
        self.assertEqual(json_response['maker'], data['maker'])
        self.assertEqual(json_response['skill_level'], data['skillLevel'])
        self.assertEqual(json_response['number_of_players'], data['numberOfPlayers'])

    def test_delete_game(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f'/games/{self.game.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/games/{self.game.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


