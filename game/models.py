from django.db import models

class Score(models.Model):
    score=models.IntegerField()
    name=models.CharField(max_length=20)
    def __str__(self):
        return f'{self.name}: {self.score}'
