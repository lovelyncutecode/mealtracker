from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.db import connection

class ActivitySerializer(serializers.ModelSerializer):
    def get_validation_exclusions(self):
        exclusions = super(ActivitySerializer, self).get_validation_exclusions()
        return exclusions + ['id']

    class Meta:
        model = Activity
        fields = ('id','name','cal')

class UserSerializer(serializers.ModelSerializer):
    def get_validation_exclusions(self):
        exclusions = super(UserSerializer, self).get_validation_exclusions()
        return exclusions + ['id']
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','password')

class FavMealSerializer(serializers.ModelSerializer):
    meal = serializers.ReadOnlyField(source='meal.name')
    class Meta:
        model = FavMeal
        fields = ('meal',)

class FavActivitySerializer(serializers.ModelSerializer):
    activity = serializers.ReadOnlyField(source='activity.name')
    class Meta:
        model = FavActivity
        fields = ('activity',)

class ProfileSerializer(serializers.ModelSerializer):
    def get_validation_exclusions(self):
        exclusions = super(ProfileSerializer, self).get_validation_exclusions()
        return exclusions + ['id']
    class Meta:
        model = Profile
        fields = ('id','user','sex','bd','height',
                'weight','fav_meals','fav_activities',
                'cal_goal')
    fav_meals = FavMealSerializer(required=False, many=True, source="link_to_profm")   
    fav_activities = FavActivitySerializer(required=False, many=True, source="link_to_profa")   
    
class DayMealSerializer(serializers.ModelSerializer):
    meal = serializers.ReadOnlyField(source='meal.name')
    class Meta:
        model = DayMeal
        fields = ('meal','amount')

class DayActivitySerializer(serializers.ModelSerializer):
    activity = serializers.ReadOnlyField(source='activity.name')
    class Meta:
        model = DayActivity
        fields = ('activity',)    

class DaySerializer(serializers.ModelSerializer):
    def get_validation_exclusions(self):
        exclusions = super(DaySerializer, self).get_validation_exclusions()
        return exclusions + ['id']
    class Meta:
        model = Day
        fields = ('id','user','date','activities','meals')            
    meals = DayMealSerializer(required=False, many=True, source="link_to_daym")   
    activities = DayActivitySerializer(required=False, many=True, source="link_to_daya")   

class DayExtSerializer(serializers.ModelSerializer):
    gain = serializers.SerializerMethodField('gain_m')
    loss = serializers.SerializerMethodField('loss_m')

    def gain_m(self, obj):
        with connection.cursor() as cursor:
            cursor.execute("SELECT sum(mealtr_daymeal.amount*(mealtr_meal.cal/100)) \
             FROM mealtr_meal,mealtr_daymeal,mealtr_day \
             WHERE mealtr_day.id=mealtr_daymeal.day_id \
             AND mealtr_daymeal.meal_id=mealtr_meal.id \
             AND mealtr_daymeal.day_id=%s",[obj.id])
            res=cursor.fetchone()
            res=res[0]
            if res:
                gain=float("{0:.2f}".format(res))
            else:
                gain=0    
        return gain

    def loss_m(self, obj):
        with connection.cursor() as cursor:
            cursor.execute("SELECT sum(mealtr_activity.cal) FROM mealtr_activity, \
             mealtr_dayactivity,mealtr_day \
             WHERE mealtr_day.id=mealtr_dayactivity.day_id \
             AND mealtr_dayactivity.activity_id=mealtr_activity.id \
             AND mealtr_dayactivity.day_id=%s",[obj.id])
            res=cursor.fetchone()
            res=res[0]
            if res:
                loss=float("{0:.2f}".format(res))
            else:
                loss=0    
        return loss

    class Meta:
        model = Day
        fields = ('id','user','date','activities','meals','gain','loss')  

    meals = DayMealSerializer(required=False, many=True, source="link_to_daym")   
    activities = DayActivitySerializer(required=False, many=True, source="link_to_daya")       
    
class MealCompSerializer(serializers.ModelSerializer):
    component = serializers.ReadOnlyField(source='component.name')
    class Meta:
        model = MealComp
        fields = ('component','amount')  

class MealSerializer(serializers.ModelSerializer):
    def get_validation_exclusions(self):
        exclusions = super(MealSerializer, self).get_validation_exclusions()
        return exclusions + ['id']
    class Meta:
        model = Meal
        fields = ('id','name','components','cal')
    components = MealCompSerializer(required=False, many=True, source="link_to_meal")   

class CompPropSerializer(serializers.ModelSerializer):
    prop = serializers.ReadOnlyField(source='prop.name')
    class Meta:
        model = CompProp
        fields = ('prop','value',)  
       
class PropertySerializer(serializers.ModelSerializer):
    def get_validation_exclusions(self):
        exclusions = super(PropertySerializer, self).get_validation_exclusions()
        return exclusions + ['id']
    class Meta:
        model = Property
        fields = ('id','name',)

class ComponentSerializer(serializers.ModelSerializer):
    def get_validation_exclusions(self):
        exclusions = super(ComponentSerializer, self).get_validation_exclusions()
        return exclusions + ['id'] 
    class Meta:
        model = Component
        fields = ('id','name','props',)
        depth=5
    props = CompPropSerializer(required=False, many=True, source="link_to_comp")

    