from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    pub_date = models.DateTimeField('created_at')
    num_players = models.IntegerField(default=4)
    num_majors = models.IntegerField(default=3)
    major = models.CharField(max_length=50)
    minor = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name


class Player(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    item = models.CharField(max_length=20)
    majority = models.BooleanField()
    plain_pass = models.CharField(null=True, max_length=5)
    vote = models.CharField(max_length=20, null=True)
    replay = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname


class Topic(models.Model):
    # all data
    category = models.CharField(max_length=50)
    # data = many

    def __str__(self):
        return self.category
# empty line needed
