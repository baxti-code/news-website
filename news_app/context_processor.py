from .models import News, Category

def Latest_news(request):
    latest_news = News.published.all()[:15]
    categories = Category.objects.all()
    context = {
        'latest_news': latest_news,
        'categories' :categories
    }
    return context