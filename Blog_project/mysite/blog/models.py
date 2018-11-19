from django.db import models
from django.utils import timezone
from django.urls import reverse
#from django.core.urlresolvers import reverse

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE) #User sınıfına bağladık
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True) #published_date alanı boş bırakılabilir.

    def publish(self): #yayınlanma tarihini ayarlamak için kullandık
        self.published_date = timezone.now() #şuan ki zamana göre otomatik oluşturduk
        self.save()

    #yorumlar listesi olucak.Onaylanan ve onaylanmayanlar olarak.Bu fonksiyon onaylanan yorumları (approved_comment=True) döndürücek.
    def approve_comments(self): #yorumları onaylamak için oluşturduk
        return self.comments.filter(approved_comment=True)


    def get_absolute_url(self): #Onaylanmış Yorumu(Comment) döndürdükten sonra Post detay sayfasına geri dönelim
        return reverse("post_detail",kwargs={'pk':self.pk})


    def __str__(self):
        return self.title


#Post sınıfı gibi her Yorumun(Comment) bir author,text,created_date,approve_comment alanları olacak.
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE) #Post modeline bağladık.
    author = models.CharField(max_length=200) # Dikkat!!!  Post classındaki author ile aynı değil.
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False) #True yada False değeri alabilir

    def approve(self): #Onaylanan yorumların değerini True yapıcaz
        self.approved_comment = True
        self.save()


    def get_absolute_url(self):  #Onaylanmış Yorumu(Comment) kaydettikten sonra Post list  sayfasına geri dönelim
        return reverse("post_list")

    def __str__(self): #onaylanan metni döndür
        return self.text
