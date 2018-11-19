from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required #dekoratör import ettik
from django.contrib.auth.mixins import LoginRequiredMixin # Oturum açmış kullanıcılara erişim kısıtlaması için kullanılır
from django.views.generic import (TemplateView,ListView,
                                   DetailView,CreateView,
                                   UpdateView,DeleteView, )

class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):  #anasayfada tüm postların yer aldığı liste
    model = Post           #Post modeline bağladık

    def get_queryset(self):# Belirli bir sorguyu bir listede kullanmak için oluşturulur
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    #sorgu seti-filtreleme : Post nesnelerini yayınlanma tarihlerine göre order_by metodu ile sıralıycaz.
    #ayrıca filtreleme işlemi şuanki zamana göre yapılacak
    #order_by('-published_date') -published_date, yayınlananlar arasında azalan sırada yani en yeni blog yazısı listenin ilk sırasında yer alıcak

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView): #LoginRequiredMixin:kullanıcı kayıtlıysa
    login_url = '/login/' #kullanıcı doğrulanmamışsa login sayfasına yönlendirilir
    redirect_field_name = 'blog/post_detail.html' #yönlendirilecek sayfayı redirect_field_name değişkenine attık
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list') #silme işlemi gerçekleşti.Tekrar post_list sayfasına git

class DraftListView(LoginRequiredMixin,ListView): #taslak listesi oluşturduk
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post

    def get_queryset(self): #yayın tarihi olmayan postları oluşturulma tarihine göre sıralayan sorgu
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


########################################################
########################################################

@login_required #oturum açılmış olmalı
def post_publish(request, pk): #bu fonksiyona request ve  asıl yorumu post ile bağlantılandıran birincil anahtarı argüman  alırız
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@ login_required
def add_comment_to_post(request, pk): #bu fonksiyona request ve  asıl yorumu post ile bağlantılandıran birincil anahtarı argüman  alırız
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST) #gelen veriyi form değişkenine attık
        if form.is_valid(): #eğer form doğrulanmışsa
            comment = form.save(commit=False)
            comment.post = post #  ----? comment nesnesini post nesnesine bağladık
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk) #bu metoda Comment modelini ve asıl yorumu post ile  bağlantılandıran birincil anahtarı argüman alırız
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):#veritabanındaki bir yorumu silmek için
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk #primary key ayrı bir değişkene attık
    comment.delete()
    return redirect('post_detail', pk=post_pk)
