from django.db import models
from scrap.scrapers.khodro45 import scrap_khodro45

# Create your models here.


class Car(models.Model):
    slug = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255, null=True)
    option = models.CharField(max_length=255, null=True)
    price = models.FloatField(null=True)
    mile = models.FloatField(null=True)
    gearbox = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=255, null=True)
    car_specifications = models.CharField(max_length=255, null=True)
    body_health = models.CharField(max_length=255, null=True)
    engine_status = models.CharField(max_length=255, null=True)


class Client(models.Model):
    class ClientType(models.IntegerChoices):
        khodro45 = 1

    scrapers = {
        ClientType.khodro45.value: scrap_khodro45
    }

    client = models.IntegerField(choices=ClientType.choices)

    def __str__(self):
        return f"{self.client}"

    def get_scraper(self):
        return self.scrapers[self.client]

    def run_script(self):
        scraper = self.get_scraper()
        scraper(self)
