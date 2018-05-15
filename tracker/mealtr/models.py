from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Property(models.Model):
    name = models.CharField(max_length=60)

class Component(models.Model):
    name = models.CharField(max_length=40)
    props = models.ManyToManyField(Property,
        through='CompProp',
        through_fields=('component','prop'),
        )    

class Activity(models.Model):
    name = models.CharField(max_length=70)
    cal = models.IntegerField(default=0)

class Meal(models.Model):
    name = models.CharField(max_length=40)
    components = models.ManyToManyField(Component,
        through='MealComp',
        through_fields=('meal','component'),
        )
    cal = models.IntegerField(default=0)

class Day(models.Model):
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    date = models.DateField()
    activities = models.ManyToManyField(Activity,
        through='DayActivity',
        through_fields=('day','activity'),
        )
    meals = models.ManyToManyField(Meal,
        through='DayMeal',
        through_fields=('day','meal'),
        )

class Profile(models.Model):
    SEX_CHOICES = (
        ('F','Female'),
        ('M','Male'),
        ('I','Intersex'),
        )
    
    user = models.OneToOneField(User,
        on_delete=models.CASCADE)
    sex = models.CharField(max_length=10,
        choices=SEX_CHOICES) #options
    bd = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    height = models.DecimalField(max_digits=3,
        decimal_places=2,
        help_text="Please input in metres.") 
    weight = models.DecimalField(max_digits=4,
        decimal_places=1,
        help_text="Please input in kilograms.")
    fav_meals = models.ManyToManyField(Meal,
        through='FavMeal',
        through_fields=('profile','meal'),
        )
    fav_activities= models.ManyToManyField(Activity,
        through='FavActivity',
        through_fields=('profile','activity'),
        )
    cal_goal = models.IntegerField(null=True)

class FavMeal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="link_to_profm")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)    

class FavActivity(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="link_to_profa")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)     

class DayMeal(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE,related_name="link_to_daym")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)        
    amount = models.IntegerField(help_text='Please input in grams.') #in grams  

class DayActivity(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE,related_name="link_to_daya")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)     

class MealComp(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE,  related_name="link_to_meal") 
    amount = models.IntegerField(help_text='Please input in grams.') #in grams   

class CompProp(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE,related_name="link_to_comp")
    prop = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="link_to_prop")  
    value = models.DecimalField(max_digits=5,
        decimal_places=1)   