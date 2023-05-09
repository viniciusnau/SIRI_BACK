from django.contrib.auth.models import User
from django.db import models

from stock.models import Stock


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=255)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=254, default="defensoria@test.com")

    def __str__(self):
        return (
            self.name
            + " - "
            + self.stock.sector.name
            + " - "
            + self.stock.sector.public_defense.name
        )
