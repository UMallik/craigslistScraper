from django.shortcuts import render
from requests.compat import quote_plus

from bs4 import BeautifulSoup

from . import models
import requests

# Create your views here.
BASE_CRAIGSLIST_URL  = 'https://lucknow.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features = 'html.parser')
    
    post_listings = soup.find_all('li', {'class':'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='gallery').get('data-ids'):
            post_image = post.find(class_='gallery').get('data-ids').split(',')[0].split(':')[1]
            print(post_image)
            post_image_url = BASE_IMAGE_URL.format(post_image)
        else:
             post_image_url = 'https://craigslist.org/imager/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    
    
    front_end_stuff = {
        'search': search,
        'final_postings': final_postings,
        }
    return render(request, 'my_app/new_search.html', front_end_stuff)