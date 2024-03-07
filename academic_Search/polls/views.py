from django.http import HttpResponse
from django.shortcuts import render
from .models import searcheds
from textblob import TextBlob
from django.http import JsonResponse
from . import tasks

def index(request):
    #if request.method == 'POST':
    #    form = SearchForm(request.POST)
    #    if form.is_valid():
    #        query = form.cleaned_data['query']
    #        return redirect('results', query=query)
    #else:
    #    form = SearchForm()
    return render(request,'home.html')

def add_searched(request):
    record = {"yayin adi":"emre"}
    searcheds.insert_one(record)
    return HttpResponse("new searched added")

def get_all_searcheds(request):
    searchin = searcheds.find()
    return HttpResponse(searchin)

def show_results(request):
    if 'param1' in request.GET:
        corrected_query = TextBlob(request.GET['param1']).correct()
        param1 = request.GET['param1']

        # do searchs

        #return HttpResponse(f"corrected : {corrected_query}")
    card_data_list = [
        {'title': 'Card 1', 'description': 'This is the first card.', 'url': '/link-to-card-1/'},
        {'title': 'Card 2', 'description': 'This is the second card.', 'url': '/link-to-card-2/'},
        # Add more cards as needed
    ]

    return render(request, 'results.html', {'cards_data': card_data_list})
    #return render(request,'results.html',{"param1": corrected_query})

def scrap(request):
    if 'param1' in request.GET:
        corrected_query = TextBlob(request.GET['param1']).correct()
        param1 = request.GET['param1']
        scrapped_data = tasks.scrape_website(corrected_query)
        return render(request, 'results.html', {'cards_data': scrapped_data})