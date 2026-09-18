from django.urls import path
from .views import News_List, HomePageView, ContactPageView, PageView404, SinglePageView, CategoryPageView, NewsUpdateView, NewsDeleteView, NewsCreateView


urlpatterns = [
    path('', HomePageView.as_view(), name = 'home_page'),
    path('contact/', ContactPageView.as_view(), name = 'contact_page' ),
    path('404-page/', PageView404, name = '404_page'),
    path("news/<slug:slug>", SinglePageView, name ='single_page'),
    path('news/<slug>/update', NewsUpdateView.as_view(), name = 'update_view'),
    path('news/<slug>/delete', NewsDeleteView.as_view(), name = 'delete_view'),
    path('news/create/', NewsCreateView.as_view(), name = 'create_news'),
    path('news/', News_List, name="all_news_list"),
    path('category/<int:pk>', CategoryPageView, name = 'category_page'),
    ]