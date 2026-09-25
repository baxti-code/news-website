from django.shortcuts import get_object_or_404, render
from .models import News, Category, Comments
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView
from .forms import ContactForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
# Create your views here.

class HomePageView(ListView):
    model = News
    template_name = 'news/home_page.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.published.all().order_by('-published_time')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_news = News.published.select_related('category').order_by('-published_time')
        context['categories'] = Category.objects.all()
        context['local_news'] = all_news.filter(category__name="O'zbekiston")[1:5]
        context['local_one'] = all_news.filter(category__name="O'zbekiston")[:1]
        context['jahon_news'] = all_news.filter(category__name = 'Jahon')[1:5]
        context['jahon_one'] = all_news.filter(category__name = 'Jahon')[:1]
        context['texnalogiya_news'] = all_news.filter(category__name = 'Texnalogiya')[1:5]
        context['texnalogiya_one'] = all_news.filter(category__name = 'Texnalogiya')[:1]
        context['sport_news'] = all_news.filter(category__name = 'Sport')[:5]
        context['most_viewed_news'] = News.published.order_by('-hit_count')[:5]
        return context


class ContactPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form,
            'categories':Category.objects.all()
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
            'form':form,
            'categories':Category.objects.all()
        }
        return render(request, 'news/contact.html', context)


def PageView404(request):
    context = {
        'categories':Category.objects.all(),
    }
    return render(request, 'news/404.html', context)

# class SinglePageClassView(DetailView):
#     model = News
#     template_name = 'news/single_page.html'
#     context_object_name = 'news_detail'
    
#     def get_queryset(self):
#         return super().get_queryset().filter(status = News.Status.Published)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['category'] = Category.objects.all()
#         context['new_comment'] = new_comment
#         context['comment_form'] = comment_form
#         context['comments'] = comments
#     def post(self, request, *args, **kwargs):
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.user = request.user
#             new_comment.news = News.
    
def SinglePageView(request, slug):
    news_detail = get_object_or_404(News, slug=slug, status = News.Status.Published)
    
    session_key = f'viewed_news_{news_detail.pk}'
    if not request.session.get(session_key):
        news_detail.hit_count+=1
        news_detail.save()
        request.session[session_key] = True
        
    
    comments = news_detail.comments.filter(active = True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.news = news_detail
            new_comment.save()
            comment_form = CommentForm()
            
    else:
        comment_form = CommentForm()
    
    most_viewed_news = News.published.order_by('-hit_count')[:3]
    context = {
        'news_detail':news_detail,
        'categories':Category.objects.all(),
        'new_comment':new_comment,
        'comment_form':comment_form,
        'comments':comments,
        'most_viewed_news':most_viewed_news
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

@method_decorator(staff_member_required, name= 'dispatch')
class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'status', 'category')
    template_name = 'crud/update_view.html'
    success_url = reverse_lazy('home_page')

@method_decorator(staff_member_required, name= 'dispatch')
class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/delete_view.html'
    success_url = reverse_lazy('home_page')

@method_decorator(staff_member_required, name= 'dispatch')
class NewsCreateView(CreateView):
    model = News
    fields = ('title', 'slug', 'body', 'status', 'category', 'image')
    template_name = 'crud/create_news.html'
    success_url = reverse_lazy('home_page')
    
def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = News.published.filter(
            title__icontains=query
        ).order_by('-published_time')
    context = {
        'query': query,
        'results': results,
        'categories': Category.objects.all(),
    }
    return render(request, 'news/search.html', context)
    
    
