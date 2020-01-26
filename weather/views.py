from .models import UserCities
from django.views.generic import TemplateView
from .get_weather import Weather, APIError
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class SearchPageView(TemplateView):
    template_name = 'home.html'


class SearchResultView(TemplateView):

    template_name = 'search_results.html'

    def get_context_data(self, *args, **kwargs):
        city = self.request.GET.get('q')
        context = {
            'city': city
        }
        return context


class CityWeatherDetailView(TemplateView):

    template_name = 'city_weater_class_based.html'

    def user_check(self):
        if self.request.user.is_authenticated:
            current_user = self.request.user
        else:
            current_user = None
        return current_user

    def city_in_favourites(self, current_user, cityname):
        if current_user:
            cities = current_user.usercities_set.all()
            city_in_favourites = cities.filter(city__iexact=cityname).exists()
            return city_in_favourites
        else:
            return True

    def get_context_data(self, *args, **kwargs):
        city = kwargs['cityname']

        weather = Weather()

        try:
            context = weather.get_five_days_weather(city)
        except APIError:
            context = {
                'error': 'APIError'
            }
        else:
            current_user = self.user_check()
            context['city_in_favourites'] = self.city_in_favourites(current_user, city)

        return context


class AddedCityView(LoginRequiredMixin, TemplateView):
    template_name = 'city_added.html'

    def get_context_data(self, *args, **kwargs):
        city = kwargs['cityname']
        current_user = self.request.user

        city_to_db = UserCities(user=current_user, city=city)
        city_to_db.save()

        context = {
            'city': city
        }
        return context


class UserCitiesView(LoginRequiredMixin, TemplateView):

    template_name = 'user_cities_view.html'

    def user_check(self):
        current_user = self.request.user
        return current_user

    def get_context_data(self, *args, **kwargs):
        weather = Weather()
        current_user = self.user_check()

        try:
            context = weather.get_current_weather(current_user)
        except APIError:
            context = {
                'error': 'APIError'
            }
        return context


class DeleteCityView(LoginRequiredMixin, TemplateView):
    template_name = 'city_deleted.html'

    def get_context_data(self, *args, **kwargs):
        city = kwargs['cityname']
        current_user = self.request.user

        city_to_delete = UserCities.objects.get(user=current_user, city__iexact=city)
        if city in city_to_delete.city:
            city_to_delete.delete()
