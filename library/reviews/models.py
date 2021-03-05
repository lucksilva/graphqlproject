from django.db import models
from django.conf import settings
from catalog.models import Book


class Review(models.Model):
    RATING_CHOICE= (
       (5, '5'),
       (4, '4'),
       (3, '3'),
       (2, '2'),
       (1, '1'), 
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Publication date')
    comment = models.TextField(max_length=1024)
    value = models.IntegerField(choices=RATING_CHOICE, default = 5)

    class Meta:
       

        verbose_name = 'BookReview'
        verbose_name_plural = 'BookReviews'
        ordering = ['-pub_date']

    def __str__(self):
   
        return '{0}/{1} - {2}'.format(self.book.title, self.user.username, self.value)
