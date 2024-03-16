from django.http import HttpResponse
from django.shortcuts import render
from .models import searcheds
from textblob import TextBlob
from django.http import JsonResponse
from . import tasks
from django.core.paginator import Paginator


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
        param1_value = request.GET['param1']
        if param1_value is not None:
            print(param1_value)
            corrected_query = TextBlob(param1_value).correct()
            scrapped_data = tasks.scrape_website(corrected_query)
            #tasks.get_searched()
            return render(request, 'results.html', {'cards_data': scrapped_data})

def view_searcheds(request):
    # Assuming cards_data is the list of items you want to paginate
    cards_data_list = tasks.get_searched()
    print(cards_data_list)

    paginator = Paginator(cards_data_list, 10)  # Show 10 items per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'show_searcheds.html', {'cards_data': page_obj})


def drop_col(request):
    tasks.drop_col()

    return HttpResponse("collection dropped")

def showCard(request):
    card = request.GET.get('card', '')  # Get the parameter value from the request
    return render(request, 'resultViewer.html', {'card': card})

def card_details(request, card_variable):
    # Fetch the card object based on the provided card_id
    print("card_variable : ", card_variable)
    cards_data = tasks.get_searched_by_url(card_variable)

    return render(request, 'resultViewer.html', {'card': cards_data[0]})