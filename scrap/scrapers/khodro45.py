import requests
import re
from bs4 import BeautifulSoup


def scrap_fields(link):

    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    body_health_score = soup.select_one('div.col-auto span.font-weight-800')
    body_health_score = re.search(
        r'([\d٫.]+)\s*/', body_health_score.text.strip()).group(1) if body_health_score else None

    # engine_had_changed = soup.select(
    # 'div.col-12 div.row ')[6].select_one('div.text-12')
    rows = soup.select('div.col-12 div.row')
    engine_status = None

    # for row in rows:
    #     label = row.select_one('div.text-10')  # the label column
    #     print(row)
    #     value = row.select_one('div.text-12')  # the value column
    #     if label and 'موتور تعویض' in label.text:
    #         engine_status = value.text.strip()
    #         break

    page_text = soup.get_text(separator=' ')
    engine_status = None
    # match = re.search(r'موتور تعویض[-–]?\s*(هست|نیست)?', page_text)
    # if match:
    #     engine_status = match.group(1) or 'هست'

    match = re.search(r'موتور تعویض[-–]?\s*([\w-]*)', page_text)
    if match:
        val = match.group(1).strip()
        if val == '' or val == '-':
            engine_status = None
        else:
            engine_status = val  # 'هست' or 'نیست'
    else:
        engine_status = None

    fields_context = {
        'body_health_score': body_health_score,
        'engine_status': engine_status
    }
    return fields_context


def scrap_khodro45(client):
    from scrap.models import Car

    count = 0
    page = 1
    while page < 19:
        url = f'https://khodro45.com/api/v2/car_listing/?page={page}'
        response = requests.get(url)
        data = response.json()

        for car in (data['results']):
            count += 1
            print(count)

            print('------------------------------------')
            print(count)
            slug = car['slug']
            name = car['car_properties']['brand']['title']
            model = car['car_properties']['model']['title']
            option = car['car_properties']['option']
            year = car['car_properties']['year']
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
                name=name,
                model=model,
                option=option,
                year=year,
                city=city,
                price=price,
                car_specifications=car_specifications,
                mile=mile,
                body_health=fields_context['body_health_score'],
                engine_status=fields_context['engine_status'],
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
