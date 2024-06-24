from django.shortcuts import render
from django.views import View

# Create your views here.

class MainPage(View):
    def get(self, request):

        context = {
            'name': 'WORLD'
        }

        return render(request, 'mainpage.html', context)