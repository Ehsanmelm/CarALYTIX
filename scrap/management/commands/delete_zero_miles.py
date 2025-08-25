from django.core.management import BaseCommand
from scrap.models import Car


class Command(BaseCommand):
    def handle(self, *args, **options):
        cars = Car.objects.filter(mile=0)
        for car in cars:
            car.delete()

        self.stdout.write(self.style.SUCCESS(
            f"delete {cars.count()} cars with zero mile "
        ))
