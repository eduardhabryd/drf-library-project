from django.db import models


class Book(models.Model):
    class Covers(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=127)
    author = models.CharField(max_length=127)
    cover = models.CharField(
        max_length=4,
        choices=Covers.choices,
        default=Covers.HARD
    )
    inventory = models.IntegerField()
    daily_fee = models.DecimalField()

    def __str__(self) -> str:
        return f"{self.title} ({self.inventory})"
