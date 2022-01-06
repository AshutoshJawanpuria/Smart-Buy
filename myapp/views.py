from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from django.contrib import messages
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
import webbrowser
from collections import defaultdict
import random
import time
from .models import products
from random import randint

# Create your views here.
def index(request):
    return render(request,'index.html')

# def counter(request):
#     text = request.POST['text']
#     amount_of_words = len(text.split())
#     return render(request,'counter.html',{'amount': amount_of_words})
def register(request):
  if request.method == 'POST':
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      password2 = request.POST['password2']

      if password == password2:
        if User.objects.filter(email=email).exists():
          messages.info(request,'Email Already Used')
          return redirect('register')
        elif User.objects.filter(username=username).exists():
          messages.info(request,'Username Already Used')
          return redirect('register')
        else:
          user = User.objects.create_user(username=username,email=email,password=password2)
          user.save()
          return redirect('login')
      else:
        messages.info(request,'Passwords Are Different')
        return redirect('register')
  else:
      return render(request,'register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username,password=password)

    if user is not None:
      auth.login(request,user)
      return redirect('index')
    else:
      messages.info(request,'Invalid Credentials')
      return redirect('login')
  else:  
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
  
def counter(request):
    #Taking Input form Webpage
    text = request.POST['text']

    #Generating Key for Scrapping 
    product_arr = text.split()
    key = ""
    count = 1
    for word in product_arr:
        if count == 1:
            key = key + str(word)
            count += 1
        else:
            key = key + '+' + str(word)

    # Scrapping Flipkart
    url_f = 'https://www.flipkart.com/search?q=' + str(key) + '&marketplace=FLIPKART&otracker=start&as-show=on&as=off'
    map_f = defaultdict(list)
    headers_f = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    source_code_f = requests.get(url_f,headers = headers_f)
    soup_f = BeautifulSoup(source_code_f.text, "html.parser")
    home_f = 'https://www.flipkart.com'
    for block in soup_f.find_all('div', {'class': '_2kHMtA'}):
            title, price, link , pic = None, 'Currently Unavailable', None , None
            for heading in block.find_all('div', {'class': '_4rR01T'}):
                title = heading.text
            for p in block.find_all('div', {'class': '_30jeq3 _1_WHN1'}):
                price = p.text[1:]
            for l in block.find_all('a', {'class': '_1fQZEK'}):
                link = home_f + l.get('href')
            for pi in block.find_all('img', {'class': '_396cs4 _3exPp9'}):
                pic = pi.get('src')
            if pic == None:
              pic = "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg"
            map_f[title] = [price, link, pic]
    l = 0
    flip_prod_id1 = products() 
    flip_prod_id2 = products() 
    flip_prod_id3 = products() 
    flip_prod_id4 = products() 
    flip_prod_id5 = products()
    flip_prod_id6 = products() 
    for i in map_f:
      if l == 1:
        flip_prod_id1.id = i
        ct = 1
        for j in map_f[i]:
           if ct == 1:
            flip_prod_id1.price = j
           elif ct == 2:
            flip_prod_id1.link = j
           elif ct == 3:
            flip_prod_id1.pic = j
           ct += 1
      if l == 2:
        flip_prod_id2.id = i
        ct = 1
        for j in map_f[i]:
           if ct == 1:
            flip_prod_id2.price = j
           elif ct == 2:
            flip_prod_id2.link = j
           elif ct == 3:
            flip_prod_id2.pic = j
           ct += 1
      if l == 3:
        flip_prod_id3.id = i
        ct = 1
        for j in map_f[i]:
           if ct == 1:
            flip_prod_id3.price = j
           elif ct == 2:
            flip_prod_id3.link = j
           elif ct == 3:
            flip_prod_id3.pic = j
           ct += 1
      if l == 4:
        flip_prod_id4.id = i
        ct = 1
        for j in map_f[i]:
           if ct == 1:
            flip_prod_id4.price = j
           elif ct == 2:
            flip_prod_id4.link = j
           elif ct == 3:
            flip_prod_id4.pic = j
           ct += 1
      if l == 5:
        flip_prod_id5.id = i
        ct = 1
        for j in map_f[i]:
           if ct == 1:
            flip_prod_id5.price = j
           elif ct == 2:
            flip_prod_id5.link = j
           elif ct == 3:
            flip_prod_id5.pic = j
           ct += 1
      if l == 6:
        flip_prod_id6.id = i
        ct = 1
        for j in map_f[i]:
           if ct == 1:
            flip_prod_id6.price = j
           elif ct == 2:
            flip_prod_id6.link = j
           elif ct == 3:
            flip_prod_id6.pic = j
           ct += 1
      l += 1
    
    # Scrapping Amazon
    url_a = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)
    # Faking the visit from a browser
    headers_a = {
      'authority': 'www.amazon.com',
      'pragma': 'no-cache',
      'cache-control': 'no-cache',
      'dnt': '1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'sec-fetch-site': 'none',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-dest': 'document',
      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    map_a = defaultdict(list)
    home_a = 'https://www.amazon.in'
    proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                        "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                        "134.213.29.202:4444"]
    proxies = {'https': random.choice(proxies_list)}
    # source_code_a = requests.get(url_a, headers=headers_a)
    # plain_text = source_code_a.text
    # soup_a = BeautifulSoup(plain_text, "html.parser")
    while(True): 
     source_code_a = requests.get(url_a, headers=headers_a)
     plain_text = source_code_a.text
     soup_a = BeautifulSoup(plain_text, "html.parser")
     err="Error"
     for check in soup_a.find_all('h4'):
      err= check.text

     if(err=="Type the characters you see in this image:"):
       time.sleep(0.5*(randint(4,8)))
       print(err)
       continue
     else:
       break


    # print(soup_a)

    for html in soup_a.find_all('div', {'class': 'sg-col-inner'}):
            title, link, pic = None, None , None
            for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                title = heading.text
            for p in html.find_all('span', {'class': 'a-price-whole'}):
                price = p.text
            for head in html.find_all('h2'):
              for l in head.find_all('a'):
                link = home_a + l.get("href")

            if(link==None):
             for l in html.find_all('a', {'class': 'a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
              link = home_a + l.get('href')

            for pi in html.find_all('img', {'class': 's-image'}):
                pic = pi.get('src')
            print(title,link,price,pic)
            # if pic == None:
            #   pic = "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg"
            if title and pic and link:
             map_a[title] = [price, link , pic]
    a_prod_id1 = products() 
    a_prod_id2 = products() 
    a_prod_id3 = products() 
    a_prod_id4 = products() 
    a_prod_id5 = products() 
    l = 0
    for i in map_a:
      if l == 1:
        a_prod_id1.id = i
        ct = 1
        for j in map_a[i]:
           if ct == 1:
            a_prod_id1.price = j
           elif ct == 2:
            a_prod_id1.link = j
           elif ct == 3:
            a_prod_id1.pic = j
           ct += 1
      if l == 2:
        a_prod_id2.id = i
        ct = 1
        for j in map_a[i]:
           if ct == 1:
            a_prod_id2.price = j
           elif ct == 2:
            a_prod_id2.link = j
           elif ct == 3:
            a_prod_id2.pic = j
           ct += 1
      if l == 3:
        a_prod_id3.id = i
        ct = 1
        for j in map_a[i]:
           if ct == 1:
            a_prod_id3.price = j
           elif ct == 2:
            a_prod_id3.link = j
           elif ct == 3:
            a_prod_id3.pic = j
           ct += 1
      if l == 4:
        a_prod_id4.id = i
        ct = 1
        for j in map_a[i]:
           if ct == 1:
            a_prod_id4.price = j
           elif ct == 2:
            a_prod_id4.link = j
           elif ct == 3:
            a_prod_id4.pic = j
           ct += 1
      if l == 5:
        a_prod_id5.id = i
        ct = 1
        for j in map_a[i]:
           if ct == 1:
            a_prod_id5.price = j
           elif ct == 2:
            a_prod_id5.link = j
           elif ct == 3:
            a_prod_id5.pic = j
           ct += 1
      l += 1
    flip_pord_list = [flip_prod_id1,a_prod_id1,flip_prod_id2,a_prod_id2,flip_prod_id3,a_prod_id3,flip_prod_id4,a_prod_id4,flip_prod_id5,a_prod_id5]
    for i in flip_pord_list:
       pass
    #return render(request,'counter.html',{'prod_id1': prod_id1,'prod_id2': prod_id2,'prod_id3': prod_id3,'prod_id4': prod_id4,'prod_id5': prod_id5})
    return render(request,'counter.html',{'flip_pord_list': flip_pord_list})
    #title = soup.title
    #return render(request,'counter.html',{'products': prod_id}) 