from django.db import models

# create your models here


class ProductSize(models.TextChoices):
    ONE = '1', '1'
    TWO = '2', '2'
    THREE = '3', '3'
    FOUR = '4', '4'
    FIVE = '5', '5'
    SIX = '6', '6'
    SEVEN = '7', '7'
    EIGHT = '8', '8'
    NINE = '9', '9'
    TEN = '10', '10'
