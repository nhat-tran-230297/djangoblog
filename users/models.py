from django.db import models
from django.contrib.auth.models import User

from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # resize the image
    # overwrite the save() method
    def save(self):
        # execute the save() method
        super().save()

        # resize the image
        new_image = Image.open(self.image.path)

        if new_image.height > 300 or new_image.width > 300:
            output_size = (300, 300)
            new_image.thumbnail(size=output_size)
            new_image.save(fp=self.image.path)
