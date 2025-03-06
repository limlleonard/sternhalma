from django.db import models

class Score(models.Model):
    score=models.IntegerField()
    name=models.CharField(max_length=20)
    def __str__(self):
        return f'{self.name}: {self.score}'

class Board(models.Model):
    int1=models.IntegerField()
    float1=models.FloatField()

class Piece(models.Model):
    pass
