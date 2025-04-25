import requests , re
from bs4 import BeautifulSoup


def scrap_body_health(link):

    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    body_health_score = soup.select_one('div.col-auto span.font-weight-800')
    body_health_score = re.search(r'([\d٫.]+)\s*/', body_health_score.text.strip()).group(1) if body_health_score else None
    print(body_health_score)
    return body_health_score    

def scrap_khodro45(client):
    from scrap.models import Car

    count = 0
    page=1
    while page < 10:
        url = f'https://khodro45.com/api/v2/car_listing/?page={page}'
        response =requests.get(url)
        data = response.json()

        for car in (data['results']):
            count+=1
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

            brand_url_slug = car['car_properties']['brand']['url_slug']
            model_url_slug = car['car_properties']['model']['url_slug']
            detail_link = f"https://khodro45.co/used-car/{brand_url_slug}-{model_url_slug}/{car['city']['title_en']}/cla-{slug}/"
            body_health = scrap_body_health(detail_link)

            car , _  = Car.objects.get_or_create(
                slug = slug,
                name = name,
                model = model,
                option = option,
                year = year,
                city = city,
                price = price,
                car_specifications = car_specifications,
                mile= mile,
                body_health=body_health ,
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

        page+=1
