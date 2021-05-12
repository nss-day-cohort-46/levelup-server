from django.db import models


class Event(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    description = models.TextField()
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        # print('using the setter', value)
        self.__joined = value
