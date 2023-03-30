from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.username}'

    class Meta:
        get_latest_by = ('username',)