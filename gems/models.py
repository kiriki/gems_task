from django.db import models


class GemItem(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    username = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.username


class Deal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(GemItem, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()
    date = models.DateTimeField()

    def __str__(self) -> str:
        return str(self.id)
