from django.contrib.auth.models import User
from django.db import models


class List(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Card(models.Model):
    order = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    # orderを一度設定したら、nullとblankを許可しないようにし、下の複合ユニーク制約をつけてください。
    # order = models.IntegerField()
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['order', 'list'], name='unique_constraint')
    #     ]

    def __str__(self):
        return self.title
