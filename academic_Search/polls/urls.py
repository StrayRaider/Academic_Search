from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("results/",views.show_results, name="results"),
    path("show/",views.get_all_searcheds,name="show"),
    path("add/",views.add_searched),
    path("scrap/",views.scrap, name="scrap"),
    path("searcheds/",views.view_searcheds, name="searcheds"),
    path("dropC/",views.drop_col, name="dropC"),
]
