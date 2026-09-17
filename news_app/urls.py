from django.urls import path
from .views import News_List, HomePageView, ContactPageView, PageView404, SinglePageView, CategoryPageView


urlpatterns = [
    path('', HomePageView.as_view(), name = 'home_page'),
    path('contact/', ContactPageView.as_view(), name = 'contact_page' ),
    path('404-page/', PageView404, name = '404_page'),
    path("news/<slug:slug>", SinglePageView, name ='single_page'),
    path('news/', News_List, name="all_news_list"),
    path('category/<int:pk>', CategoryPageView, name = 'category_page'),
    ]