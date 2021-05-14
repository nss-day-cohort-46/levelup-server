"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Game, GameType, Gamer

class GameView(ViewSet):
    def create(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)

        game = Game()
        game.title = request.data['title']
        game.maker = request.data['maker']
        game.number_of_players = request.data['numberOfPlayers']
        game.skill_level = request.data['skillLevel']
        game.gamer = gamer

        game_type = GameType.objects.get(pk=request.data['gameTypeId'])
        # select *
        # from gametype
        # where id=request.data['game_type_id']
        game.game_type = game_type

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({ 'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk):
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=pk)

        if gamer is not game.gamer:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        
        game.title = request.data['title']
        game.maker = request.data['maker']
        game.number_of_players = request.data['numberOfPlayers']
        game.skill_level = request.data['skillLevel']
        game.gamer = gamer

        game_type = GameType.objects.get(pk=request.data['gameTypeId'])
        game.game_type = game_type

        try:
            game.save()
        except ValidationError as ex:
            return Response({ 'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        try: 
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        games = Game.objects.all()
        # games?game_type=1
        game_type = request.query_params.get('game_type', None)

        if game_type is not None:
            games = games.filter(game_type__id=game_type)
            # select *
            # from games
            # join gametype on gametype.id = games.gametypeid

        serializer = GameSerializer(games, many=True, context={'request': request})
        return Response(serializer.data)

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type', 'gamer')
        depth = 2
