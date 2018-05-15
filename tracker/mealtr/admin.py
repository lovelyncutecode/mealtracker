from django.contrib import admin
from .models import *

admin.site.register(Property)
admin.site.register(Component)
admin.site.register(Activity)
admin.site.register(Meal)
admin.site.register(Day)
admin.site.register(FavMeal)
admin.site.register(FavActivity)
admin.site.register(DayMeal)
admin.site.register(DayActivity)
admin.site.register(MealComp)
admin.site.register(CompProp)
admin.site.register(Profile)