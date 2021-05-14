from levelupapi.views.profile import GamerSerializer
from levelupapi.models import Gamer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class GamerView(ViewSet):
    def list(self, request):
        gamers = Gamer.objects.all()
        res = GamerSerializer(gamers, many=True)
        return Response(res.data)
