from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
import requests
import datetime
from dateutil import parser
from .models import Mood
from django.http import HttpResponseRedirect
from django.urls import reverse


class IndexView(ListView):
    # model = Page

    def getWeather(self, city):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast"

        querystring = {"q":city}

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "b04c542bd7mshf4fe4d9539e1dd8p1a9f38jsncddc8a3a9c2a"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        result = response.json()

        return result

    
    def getWeatherData(self, city='san francisco'):
        weather = self.getWeather(city)
        # w_list = weather['list']
        city = weather['city']
        
        now = None
        n_date = None
        temp = None
        wind = None
        cloud = None

        todays = []

        for w in w_list:
            
            if now is None:
                now = w
                n_date = str(now['dt_txt'])
                w['dt_txt'] = parser.parse(n_date)
                temp = now['main']['temp']
                wind = now['wind']['speed']
                cloud = now['clouds']['all']

            w_date = str(w['dt_txt'])
            if w_date[9] == n_date[9] and w_date[6] == n_date[6]:
                w['main']['temp'] = int(int(w['main']['temp']) * 9/5 -459.67)
                w['dt_txt'] = parser.parse(w_date)

                todays.append(w)
            
            else:
                break

        # convert kelvin to celcuis
        temp = int(temp) * 9/5 -459.67
        # convert wind speed to from m/s to km/h
        wind = int(wind) * 3.6


        context = {'weather': todays, 'city': city, 'temp': int(temp), 'date': parser.parse(n_date), 'wind': wind, 'cloud': cloud, 'mood_date': n_date}

        return context


    def get(self, request):
        context = self.getWeatherData()
        return render(request, "weather/index.html", context)

    def post(self, request):

        city_name = request.POST.get('city_name')
        context = self.getWeatherData(city_name)
        return render(request, "weather/index.html", context)

def moodview(request):
        city_name = request.POST.get('city_name')
        date = request.POST.get('date')
        mood = request.POST.get('mood')

        # date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')


        mood_entry = Mood()
        mood_entry.city = city_name
        mood_entry.pub_date = date
        mood_entry.name = mood

        mood_entry.save()

        return HttpResponseRedirect(reverse('weather:mood_page'))


def moodlist(request):
    moods = Mood.objects.all().order_by('-pub_date')
    context = {'moods': moods}
    return render(request, "weather/moods.html", context)
