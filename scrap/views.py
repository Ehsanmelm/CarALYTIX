from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
import re
from bs4 import BeautifulSoup
from scrap.models import Car
from scrap.functions import persian_to_english_number
# Create your views here.


def convert_miladi_to_shasi(year):
    if 1900 <= year <= 2100:
        return year-621
    return year


class Khodro45View(APIView):
    def scrap_fields(self, link):

        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        body_health_score = soup.select_one(
            'div.col-auto span.font-weight-800')
        body_health_score = re.search(
            r'([\d٫.]+)\s*/', body_health_score.text.strip()).group(1) if body_health_score else None

        rows = soup.select('div.col-12 div.row')
        engine_status = None

        page_text = soup.get_text(separator=' ')
        engine_status = None

        match = re.search(r'موتور تعویض[-–]?\s*([\w-]*)', page_text)
        if match:
            val = match.group(1).strip()
            if val == '' or val == '-':
                engine_status = None
            else:
                engine_status = val
        else:
            engine_status = None

        match_gear = re.search(r'گیربکس[-–]?\s*([\w-]*)', page_text)
        if match_gear:
            val = match_gear.group(1).strip()
            if val in ('', '-', None):
                gearbox_status = None
            elif 'دستی' in val:
                gearbox_status = 'manual'
            elif 'اتوماتیک' in val:
                gearbox_status = 'automatic'
            else:
                gearbox_status = val
        else:
            gearbox_status = None

        fields_context = {
            'body_health_score': body_health_score,
            'engine_status': engine_status,
            'gearbox_status': gearbox_status,

        }
        return fields_context

    def post(self, request):
        try:
            count = 0
            page = 1
            while True:
                url = f'https://khodro45.com/api/v2/car_listing/?page={page}'
                response = requests.get(url)
                data = response.json()

                if response.status_code != 200:
                    break
                for car in (data['results']):
                    count += 1
                    print(count)

                    print('------------------------------------')
                    print(count)
                    slug = car['slug']
                    name = car['car_properties']['brand']['title_en']
                    model = car['car_properties']['model']['title_en']
                    option = car['car_properties']['option']
                    # year = car['car_properties']['year']
                    year = convert_miladi_to_shasi(
                        int(car['car_properties']['year']))
                    city = car['city']['title']
                    price = car['price']
                    car_specifications = car['car_specifications']['document']
                    mile = car['car_specifications']['klm']

                    brand_url_slug = car['car_properties']['brand']['seo_slug']
                    model_url_slug = car['car_properties']['model']['seo_slug']
                    detail_link = f"https://khodro45.co/used-car/{brand_url_slug}-{model_url_slug}/{car['city']['title_en']}/cla-{slug}/"
                    fields_context = self.scrap_fields(detail_link)

                    if fields_context['engine_status']==None:
                        engine_status="نیست"
                    else:
                        engine_status=fields_context['engine_status']

                    car, _ = Car.objects.get_or_create(
                        slug=slug,
                        name=name.lower(),
                        model=model.lower(),
                        option=option,
                        year=year,
                        city=city,
                        price=price,
                        car_specifications=car_specifications,
                        mile=mile,
                        body_health=persian_to_english_number(fields_context['body_health_score']),
                        engine_status=engine_status,
                        gearbox=fields_context['gearbox_status'],
                        source='khodro45',
                    )
                    print(slug)
                    print(name)
                    print(model)
                    print(option)
                    print(year)
                    print(city)
                    print(price)
                    print(car_specifications)
                    print(mile)

                page += 1

            return Response({"message": "khodro45 scrapp is done"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"An error occurred in scarap khdro45: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class HamrahMechanicView(APIView):
    def scrap_fields(self, link):

        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        body_health = 0

        rows = soup.select(
            'div.cars-for-sale-detail_gallery-container__26us9 div.cars-for-sale-detail_inspection-report__STjQ3 div.carReportSummary_car-report__row__rM6Ax')

        for row in rows:
            children = row.select(
                'div.carReportSummary_car-report-header-row__icon-and-text-container__4OQqk')
            if len(children) >= 2:
                second_child = children[1]
                body_health += int(second_child.text.strip()
                                   ) if second_child.text.strip() else 0
            else:
                print("Second element not found in this row")

        body_health = 5 - body_health/8
        print(body_health)

        fields_context = {
            'body_health_score': body_health,
        }
        return fields_context

    def post(self, request):
        count = 0
        page = 1
        while True:
            url = f'https://www.hamrah-mechanic.com/api/v1/common/newexhibition?&page={page}'
            response = requests.get(url)
            data = response.json()
            car_list = data['data']['result']['list']
            if not car_list:
                break

            for car in car_list:
                count += 1
                print(count)
                print(car['km'])
                print('------------------------------------')

                slug = car['carNamePersian'].replace(' ', '_')
                name = re.sub(r'\s*مدل\s*\d{4}$', '',
                              car['carNamePersian']).strip()
                model = car['modelEnglishName']
                # year = car['carYear']
                year = convert_miladi_to_shasi(car['carYear'])
                city = car['cityNamePersian']
                price = car['price']
                mile = car['km']
                gearbox_perain = car['gearBoxPersian']
                if gearbox_perain == "اتومات":
                    gearbox = "automatic"
                else:
                    gearbox = "manual"

                brand = car['brandEnglishName']
                orderId = car['orderId']
                detail_link = f"https://www.hamrah-mechanic.com/cars-for-sale/{brand}/{model}/{orderId}/"
                fields_context = self.scrap_fields(detail_link)

                car, _ = Car.objects.get_or_create(
                    slug=slug,
                    name=brand.lower(),
                    model=model.lower(),
                    year=year,
                    city=city,
                    price=price,
                    mile=mile,
                    gearbox=gearbox,
                    body_health=fields_context['body_health_score'],
                    engine_status="نیست",
                    source='hamrah-mechanic',

                )
                # print(slug)
                # print(name)
                # print(model)
                # print(option)
                # print(year)
                # print(city)
                # print(price)
                # print(car_specifications)
                # print(mile)

            page += 1

        return Response({"message": "khodro45 scrapp is done"}, status=status.HTTP_200_OK)


class karnamehView(APIView):

    def post(self, request):
        next_set = "1755785037096"

        while True:

            url = f"https://api-gw.karnameh.com/post-storage/car-posts/car-post-list/?size=100&start=0&sort=newest&relevant=false&is_guaranteed=false&next_set={next_set}&next_set=1"

            response = requests.get(url)
            data = response.json()["car_posts"]
            if not data:
                break
            for car in data:
                if car["price"] == 0:
                    continue
                gearbox = car['gearbox']
                if gearbox == "":
                    gearbox = None
                Car.objects.get_or_create(
                    slug=None,
                    name=car["brand_name_en"].lower(),
                    model=car["model_name_en"].lower(),
                    option=None,
                    year=convert_miladi_to_shasi(car["year"]),
                    city=car["city_name_fa"],
                    price=car["price"],
                    car_specifications=None,
                    mile=car["usage"],
                    body_health=None,
                    engine_status="نیست",
                    gearbox=gearbox,
                    source='karnameh',
                )

            next_set = response.json()["next_set"][0]

        return Response({"message": "karnameh is done"})


class FixKhodro45View(APIView):

    def post(self,request):
        cars=Car.objects.filter(source="khodro45")
        for car in cars:
            english_number=persian_to_english_number(car.body_health)
            car.body_health=english_number
            if car.engine_status=="":
                car.engine_status="نیست"
            car.save()
        return Response({"message":"done"})