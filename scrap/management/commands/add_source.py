from django.core.management.base import BaseCommand
from django.db.models import Q, F
from scrap.models import Car


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        cars = Car.objects.filter(source__isnul=True)
        for car in cars:
            car.source = 'hamrah-mechanic'

        self.stdout.write(self.style.SUCCESS(
            f"add source for hamrah-mechanic for  {cars.count()} new assignments"
        ))
