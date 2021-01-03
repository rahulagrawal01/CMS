from django.db import models
from django.contrib.auth.models import User

class Data(models.Model):
  id = models.AutoField(primary_key=True)
  title =  models.CharField(max_length=100)
  desc = models.TextField()
  img= models.ImageField(upload_to="pics")
  datetime = models.DateTimeField(auto_now=True,null=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
      return self.title
  
  