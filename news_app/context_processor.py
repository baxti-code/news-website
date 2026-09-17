from .models import News

def Latest_news(request):
    latest_news = News.published.all()[:15]
    context = {
        'latest_news': latest_news
    }
    return context