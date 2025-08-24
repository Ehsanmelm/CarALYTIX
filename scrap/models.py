from django.db import models
from scrap.scrapers.khodro45 import scrap_khodro45
from scrap.scrapers.hamrah_mechanic import scrap_hamrah_mechanic

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
    source = models.CharField(max_length=255, blank=True, null=True)
    created_At = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Client(models.Model):
    class ClientType(models.IntegerChoices):
        khodro45 = 1
        hamrah_mechanic = 2

    scrapers = {
        ClientType.khodro45.value: scrap_khodro45,
        ClientType.hamrah_mechanic.value: scrap_hamrah_mechanic,
    }

    client = models.IntegerField(choices=ClientType.choices)

    def __str__(self):
        return f"{self.client}"

    def get_scraper(self):
        return self.scrapers[self.client]

    def run_script(self):
        scraper = self.get_scraper()
        scraper(self)
