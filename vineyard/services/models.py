from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    class Types(models.TextChoices):
        WINEPRODUCER="WINEPRODUCER","Wineproducer"
        STOCKIST="STOCKIST","Stockist"
        AGENT ="AGENT","Agent"


    type = models.CharField(_('Type'), max_length =50, choices = Types.choices, default = Types.WINEPRODUCER)
    name = models.CharField(_("Name of User"), blank =True,max_length =255)

    def get_absolute_url(self):
        return reverse("user:detail", kwargs= {"username": self.username})


class WineproducerManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=User.Types.WINEPRODUCER)    


class StockistManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=User.Types.STOCKIST)



class AgentManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type= User.Types.AGENT)                    



class Wineproducer(User):
    objects = WineproducerManager()
    class Meta:
        proxy =True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.WINEPRODUCER
        return super().save(*args, **kwargs)




class Stockist(User):
    objects =StockistManager()
    class Meta:
        proxy =True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STOCKIST
        return super().save(*args, **kwargs)        





class Agent(User):
    objects = AgentManager()
    class Meta:
        proxy =True     

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.AGENT
        return super().save(*args, **kwargs)                       

   
class Product(models.Model):
    name = models.CharField(max_length= 100,null =True)
    color= models.CharField(max_length = 100, null=True)
    nose= models.CharField(max_length = 100,null =True)
    palate=models.CharField(max_length = 100,null =True)
    description = models.TextField('Description', blank=True,null =True)
    price = models.DecimalField('Price', decimal_places=2, max_digits= 100,null =True)
    created =models.DateTimeField('Created', auto_now_add=True,null =True)
    user= models.ForeignKey(User,on_delete=models.CASCADE,null =True)
    

    class Meta:
        ordering =['id']

    def __str__(self):
        return self.name


    


class Cuisine(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

    class Meta:
        ordering= ('name',)            
    

      