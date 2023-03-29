from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.authorUser.username

    def update_rating(self) -> None:
        postRating = self.post_set.aggregate(postRating=Sum("rating"))
        pRating: int = 0
        pRating += postRating.get("postRating")

        commentRating = self.authorUser.comment_set.aggregate(commentRating=Sum("rating"))
        cRating: int = 0
        cRating += commentRating.get("commentRating")

        self.ratingAuthor = pRating * 3 + cRating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    ARTICLE: str = "AR"
    NEWS: str = "NW"

    CATEGORY_CHOICES: list = (
        (ARTICLE, "Статья"),
        (NEWS, "Новость"),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES,
                                    default=ARTICLE)
    creationDate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=128)
    text: str = models.TextField()
    rating: int = models.SmallIntegerField(default=0)

    def like(self) -> None:
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        self.rating -= 1
        self.save()

    def preview(self):
        return f'Заголовок: {self.title}\n Статья: {self.text[:124]} ...'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating: int = models.SmallIntegerField(default=0)

    def like(self) -> None:
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.commentUser.username}'

    def post_com(self):
        return f'Комментарий к статье:\n Дата: {self.dateCreation}\nПользователь: {self.commentUser}\n Рейтинг: {self.rating}\n Коментарий: {self.text}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

