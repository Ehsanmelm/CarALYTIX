import requests
import re
from bs4 import BeautifulSoup


def convert_miladi_to_shasi(year):
    if 1900 <= year <= 2100:
        return year-621
    return year


def scrap_fields(link):

    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    body_health_score = soup.select_one('div.col-auto span.font-weight-800')
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


def scrap_khodro45(client):
    from scrap.models import Car

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
            year = car['car_properties']['year']
            year = convert_miladi_to_shasi(int(year))
            city = car['city']['title']
            price = car['price']
            car_specifications = car['car_specifications']['document']
            mile = car['car_specifications']['klm']

            brand_url_slug = car['car_properties']['brand']['seo_slug']
            model_url_slug = car['car_properties']['model']['seo_slug']
            detail_link = f"https://khodro45.co/used-car/{brand_url_slug}-{model_url_slug}/{car['city']['title_en']}/cla-{slug}/"
            fields_context = scrap_fields(detail_link)

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
                body_health=fields_context['body_health_score'],
                engine_status=fields_context['engine_status'],
                gearbox=fields_context['gearbox_status'],
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
