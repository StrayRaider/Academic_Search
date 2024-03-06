from django.http import HttpResponse
from django.shortcuts import render
from .models import searcheds
from textblob import TextBlob

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
        return HttpResponse(f"corrected : {corrected_query}")
    return render(request,'results.html')