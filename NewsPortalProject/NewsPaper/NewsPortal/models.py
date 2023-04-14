from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    username = models.OneToOneField(User, on_delete= models.CASCADE)
    rating = models.FloatField(default= 0.0)
    subscribers = models.ManyToManyField(User, related_name='author_subs')

    def update_rating(self):
        post_rating = sum(post.rating for post in self.post_set.all()) * 3
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.username))
        post_commnet_rating = sum(
            comment.rating for comment in Comment.objects.filter(post__post_author=self)
        )
        self.rating = post_rating + comment_rating + post_commnet_rating
        self.save()

    def __str__(self):
        return self.username.username


class Category(models.Model):
    name = models.CharField(max_length= 255, unique= True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    news = 'NW'
    article = 'AR'

    TYPE = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]

    post_author = models.ForeignKey('Author', on_delete=models.CASCADE)
    type_choose = models.CharField(max_length= 255, choices= TYPE, default= article)
    addtime = models.DateTimeField(auto_now_add= True)
    category = models.ManyToManyField('Category', through= 'PostCategory')
    header = models.CharField(max_length= 255)
    text = models.TextField()
    rating = models.FloatField(default= 0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) <= 124:
            return self.text
        else:
            return self.text[:124] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    comment_text = models.TextField()
    addtime = models.DateTimeField(auto_now_add= True)
    rating = models.FloatField(default= 0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()




