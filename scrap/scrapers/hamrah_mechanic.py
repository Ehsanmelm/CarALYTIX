import requests
import re
from bs4 import BeautifulSoup


def convert_miladi_to_shasi(year):
    if 1900 <= year <= 2100:
        return year-621


def scrap_fields(link):

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


def scrap_hamrah_mechanic(client):
    from scrap.models import Car
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
            fields_context = scrap_fields(detail_link)

            car, _ = Car.objects.get_or_create(
                slug=slug,
                name=brand,
                model=model,
                year=year,
                city=city,
                price=price,
                mile=mile,
                gearbox=gearbox,
                body_health=fields_context['body_health_score'],
                engine_status="نیست"

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
