from django.shortcuts import get_object_or_404, render
from .models import News, Category
from django.views.generic import TemplateView, ListView
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

class HomePageView(ListView):
    model = News
    template_name = 'news/home_page.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.published.all().order_by('-published_time')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['local_news'] = News.published.filter(
            category__name="O'zbekiston"
        ).order_by('-published_time')[1:5]
        context['local_one'] = News.published.filter(
            category__name="O'zbekiston"
        ).order_by('-published_time')[:1]
        context['jahon_news'] = News.published.filter(category__name = 'Jahon').order_by('-published_time')[1:5]
        context['jahon_one'] = News.published.filter(category__name = 'Jahon').order_by('-published_time')[:1]
        context['texnalogiya_news'] = News.published.filter(category__name = 'Texnalogiya').order_by('-published_time')[1:5]
        context['texnalogiya_one'] = News.published.filter(category__name = 'Texnalogiya').order_by('-published_time')[:1]
        context['sport_news'] = News.published.filter(category__name = 'Sport').order_by('-published_time')[:5]

        return context


class ContactPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            send_mail(
                subject=f"Yangi xabar: {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
            )
            return HttpResponse('<h2>Sizning xabaringiz muvaffaqiyatli yuborildi</h2>')
        context = {
            'form':form
        }
        return render(request, 'news/contact.html', context)


def PageView404(request):
    context = {
        'categories':Category.objects.all(),
    }
    return render(request, 'news/404.html', context)

def SinglePageView(request, slug):
    news_detail = get_object_or_404(News, slug=slug, status = News.Status.Published)
    context = {
        'news_detail':news_detail,
        'categories':Category.objects.all(),
    }
    return render(request, 'news/single_page.html', context)

def CategoryPageView(request, pk):
    category = get_object_or_404(Category, pk=pk)
    news_list = News.published.filter(category = category).order_by('-published_time')
    context = {
        'category':category,
        'news_list':news_list,
        'categories':Category.objects.all()
    }
    return render(request, 'news/news_list.html', context)


def News_List(request):
    news_list = News.published.all()

    context = {'news_list' : news_list}

    return render(request, 'news/news_list.html',context=context )
