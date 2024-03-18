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

    sort_param = request.GET.get('sort', None)

    # Your sorting logic based on the parameter
    if sort_param == 'asc':
        # Handle ascending sorting
        sorted_documents = tasks.get_searched_sorted('publication_date', 1)
        paginator = Paginator(sorted_documents, 10)  # Show 10 items per page.

        page_number = request.GET.get('page')

    elif sort_param == 'desc':
        # Handle descending sorting
        sorted_documents = tasks.get_searched_sorted('publication_date', -1)

        paginator = Paginator(sorted_documents, 10)  # Show 10 items per page.

        page_number = request.GET.get('page')
    elif sort_param == 'Casc':
        # Handle ascending sorting
        sorted_documents = tasks.get_searched_sorted('citation_count', 1)
        paginator = Paginator(sorted_documents, 10)  # Show 10 items per page.

        page_number = request.GET.get('page')

    elif sort_param == 'Cdesc':
        # Handle descending sorting
        sorted_documents = tasks.get_searched_sorted('citation_count', -1)

        paginator = Paginator(sorted_documents, 10)  # Show 10 items per page.

        page_number = request.GET.get('page')
    else:
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



def filter_publications(request):
    # Get filter parameters from request
    filters = request.GET.getlist('filter')

    # Build Elasticsearch query
    es_query = Search(index='publications_index')
    for f in filters:
        es_query = es_query.query('match', **{f: request.GET[f]})

    # Execute the Elasticsearch query
    response = es_query.execute()

    # Extract filtered results
    filtered_results = [hit.to_dict() for hit in response.hits]

    # Pass filtered results to template for rendering
    return render(request, 'filtered_publications.html', {'filtered_results': filtered_results})