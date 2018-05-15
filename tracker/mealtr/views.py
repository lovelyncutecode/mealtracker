from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token


#okei
class PropertyView(APIView):
    #permission_classes = (IsAuthenticated,)
    
    def get(self, request, format=None):
        queryset = Property.objects.all()
        model = Property
        serializer_class = PropertySerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request, format=None):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#okei 
class PropertyDetail(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        queryset = Property.objects.filter(pk=pk)
        model = Property
        serializer_class = PropertySerializer(queryset, many=True)
        return Response(serializer_class.data)

    def put(self, request, pk, format=None):
        prop = self.get_object(pk)
        serializer = PropertySerializer(prop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk, format=None):
        prop = self.get_object(pk)
        prop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Property.objects.filter(pk=pk).first()
        except Property.DoesNotExist:
            raise Http404

#okei
class ActivityView(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Activity.objects.all()
        model = Activity
        serializer_class = ActivitySerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request, format=None):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#okei
class ActivityDetailView(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        queryset = Activity.objects.filter(pk=pk)
        model = Activity
        serializer_class = ActivitySerializer(queryset, many=True)
        return Response(serializer_class.data)

    def put(self, request, pk, format=None):
        activ = self.get_object(pk)
        serializer = ActivitySerializer(activ, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk, format=None):
        activ = self.get_object(pk)
        activ.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Activity.objects.filter(pk=pk).first()
        except Activity.DoesNotExist:
            raise Http404            

#okei
class RegView(APIView):
    def post(self, request, format=None):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(username=request.data['username'],password=request.data['password'])
            return Response( status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#okei
class UserView(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        queryset = User.objects.filter(pk=pk)
        model = User
        serializer_class = UserSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return User.objects.filter(pk=pk).first()
        except User.DoesNotExist:
            raise Http404            
    
#okei    
class ComponentView(APIView):
    
    def get(self, request, format=None):
        queryset = Component.objects.all()
        model = Component
        serializer_class = ComponentSerializer(queryset, many=True)
        return Response(serializer_class.data)
    
    def post(self, request, format=None):
        serializer = ComponentSerializer(data=request.data)
        
        if serializer.is_valid():
            compprop = request.data.pop('props')
            comp = Component.objects.create(**request.data)
            for curprop in compprop:
                tres = Property.objects.filter(name=curprop.pop('prop')).first()
                CompProp.objects.create(component=comp,
                             value=curprop.pop('value'),
                             prop=tres) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#okei 
class ComponentDetailView(APIView):

    def get(self, request, pk, format=None):
        queryset = Component.objects.filter(pk=pk)
        model = Component
        serializer_class = ComponentSerializer(queryset, many=True)
        return Response(serializer_class.data)
    
    def put(self, request, pk, format=None):
        comp = self.get_object(pk)
        compprop = request.data.pop('props')
        serializer = ComponentSerializer(comp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            for curprop in compprop:
                curprop['component'] = pk
                prop_t=Property.objects.filter(name=curprop['prop']).first()
                curprop['prop']=prop_t.id
                comprop_t=CompProp.objects.filter(component=comp,prop=prop_t)[0]
                ser=CompPropSerializer(comprop_t,data=curprop)
                if ser.is_valid():
                    print(comprop_t)
                    ser.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk, format=None):
        comp = self.get_object(pk)
        
        prop_list=comp.props.all()
        print(comp.props.all())
        for prop in prop_list:
            prop_t=Property.objects.filter(name=prop.name).first()
            comp_prop_t=CompProp.objects.filter(prop=prop_t.id,component=comp.id).first()
            comp_prop_t.delete()
        comp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Component.objects.filter(pk=pk).first()
        except Property.DoesNotExist:
            raise Http404

#okei 
class MealView(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Meal.objects.all()
        model = Meal
        serializer_class = MealSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request, format=None):
        serializer = MealSerializer(data=request.data)
        
        if serializer.is_valid():
            mealcomp = request.data.pop('components')
            meal = Meal.objects.create(**request.data)
            for curcomp in mealcomp:
                print(curcomp)
                tres = Component.objects.filter(name=curcomp.pop('component')).first()
                print(tres)
                MealComp.objects.create(component=tres,
                             amount=curcomp.pop('amount'),
                             meal=meal) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#okei 
class MealDetailView(APIView):
    #permission_classes = (IsAuthenticated,)
    
    def get(self, request, pk, format=None):
        queryset = Meal.objects.filter(pk=pk)
        model = Meal
        serializer_class = MealSerializer(queryset, many=True)
        return Response(serializer_class.data)
    
    def put(self, request, pk, format=None):
        meal = self.get_object(pk)
        mealcomp = request.data.pop('components')
        serializer = MealSerializer(meal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            for curcomp in mealcomp:
                curcomp['meal'] = pk
                comp_t=Component.objects.filter(name=curcomp['component']).first()
                print(comp_t)
                curcomp['component']=comp_t.id
                mealcomp_t=MealComp.objects.filter(meal=meal,component=comp_t)[0]
                ser=MealCompSerializer(mealcomp_t,data=curcomp)
                if ser.is_valid():
                    ser.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk, format=None):
        meal = self.get_object(pk)
        comp_list=meal.components.all()
        for comp in comp_list:
            comp_t=Component.objects.filter(name=comp.name).first()
            mealcomp_t=MealComp.objects.filter(component=comp_t.id,meal=meal.id).first()
            mealcomp_t.delete()
        meal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Meal.objects.filter(pk=pk).first()
        except Property.DoesNotExist:
            raise Http404

#okei
class DayView(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Day.objects.all()
        model = Day
        serializer_class = DaySerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request, format=None):
        serializer = DaySerializer(data=request.data)
        
        if serializer.is_valid():
            daymeal = request.data.pop('meals')
            dayact = request.data.pop('activities') 
            user = User.objects.filter(id=request.data.pop('user')).first()
            day = Day.objects.create(user=user,**request.data)
            for curmeal in daymeal:
                tres = Meal.objects.filter(name=curmeal.pop('meal')).first()
                DayMeal.objects.create(meal=tres,
                             amount=curmeal.pop('amount'),
                             day=day) 
            for curact in dayact:
                tres = Activity.objects.filter(name=curact.pop('activity')).first()
                DayActivity.objects.create(activity=tres,day=day)     
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#okei
class ProfileView(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        queryset = Profile.objects.all()
        model = Profile
        serializer_class = ProfileSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            favmeal = request.data.pop('fav_meals')
            favact = request.data.pop('fav_activities') 
            user = User.objects.filter(id=request.data.pop('user')).first()
            prof = Profile.objects.create(user=user,**request.data)

            for curmeal in favmeal:
                tres = Meal.objects.filter(name=curmeal.pop('meal')).first()
                FavMeal.objects.create(meal=tres,profile=prof) 
            for curact in favact:
                tres = Activity.objects.filter(name=curact.pop('activity')).first()
                FavActivity.objects.create(activity=tres,profile=prof)   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DayDetailView(APIView):
    #permission_classes = (IsAuthenticated,)
    
    def get(self, request, year, month, day, format=None):
        from django.db import connection
        date = str(year)+'-'+str(month)+'-'+str(day)
        queryset = Day.objects.filter(date=date)
        
        model = Day
        serializer_class = DayExtSerializer(queryset, many=True)
        return Response(serializer_class.data)
    
    #!!!!!!!!!!!!!!!Adding and deleting meals and activities!!!!!!!!!!!!!!!!!!!!!!!!

    '''def put(self, request, pk, format=None):
        day = self.get_object(pk)
        daymeal = request.data.pop('meals')
        dayact = request.data.pop('activities')
        serializer = DaySerializer(day, data=request.data)
        if serializer.is_valid():
            serializer.save()
            for curmeal in daymeal:
                curmeal['day'] = pk
                meal_t=Meal.objects.filter(name=curmeal['meal']).first()
                curmeal['meal']=meal_t.id
                daymeal_t=DayMeal.objects.filter(meal=meal_t,day=day)[0]
                ser=DayMealSerializer(daymeal_t,data=curmeal)
                if ser.is_valid():
                    ser.save()
            for curact in dayact:
                curact['day'] = pk
                act_t=Activity.objects.filter(name=curact['activity']).first()
                curact['activity']=act_t.id
                print(act_t)
                print(day)
                dayact_t=DayActivity.objects.filter(activity=act_t,day=day).first()
                ser=DayActivitySerializer(dayact_t,data=curact)
                
                print(dayact_t)
                if ser.is_valid():
                    ser.save()        
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    ''' 
    def post(self, request, format=None):
        serializer = DaySerializer(data=request.data)
        
        if serializer.is_valid():
            daymeal = request.data.pop('meals')
            dayact = request.data.pop('activities') 
            user = User.objects.filter(id=request.data.pop('user')).first()
            day = Day.objects.create(user=user,**request.data)
            for curmeal in daymeal:
                tres = Meal.objects.filter(name=curmeal.pop('meal')).first()
                DayMeal.objects.create(meal=tres,
                             amount=curmeal.pop('amount'),
                             day=day) 
            for curact in dayact:
                tres = Activity.objects.filter(name=curact.pop('activity')).first()
                DayActivity.objects.create(activity=tres,day=day)     
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, year,month,day, format=None):
        date = str(year)+'-'+str(month)+'-'+str(day)
        day = self.get_object(date)
        meal_list=day.meals.all()
        act_list=day.activities.all()
        for meal in meal_list:
            meal_t=Meal.objects.filter(name=meal.name).first()
            daymeal_t=DayMeal.objects.filter(meal=meal_t.id,day=day.id).first()
            daymeal_t.delete()
        for act in act_list:
            act_t=Activity.objects.filter(name=act.name).first()
            dayact_t=DayActivity.objects.filter(activity=act_t.id,day=day.id).first()
            dayact_t.delete()
        day.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, date):
        try:
            return Day.objects.filter(date=date).first()
        except Property.DoesNotExist:
            raise Http404
            
class ProfileDetailView(APIView):
    #permission_classes = (IsAuthenticated,)
    
    def get(self, request, pk, format=None):
        queryset = Profile.objects.filter(pk=pk)
        model = Profile
        serializer_class = ProfileSerializer(queryset, many=True)
        return Response(serializer_class.data)
    
    #!!!!!!!!!!!!!!!Adding and deleting meals and activities!!!!!!!!!!!!!!!!!!!!!!!!

    def delete(self, request, pk, format=None):
        prof = self.get_object(pk)
        meal_list=prof.fav_meals.all()
        act_list=prof.fav_activities.all()
        for meal in meal_list:
            meal_t=Meal.objects.filter(name=meal.name).first()
            favmeal_t=FavMeal.objects.filter(meal=meal_t.id,profile=prof.id).first()
            favmeal_t.delete()
        for act in act_list:
            act_t=Activity.objects.filter(name=act.name).first()
            favact_t=FavActivity.objects.filter(activity=act_t.id,profile=prof.id).first()
            favact_t.delete()
        prof.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Profile.objects.filter(pk=pk).first()
        except Property.DoesNotExist:
            raise Http404

#okei
class MealSearchView(APIView):  
    def get(self, request, name, format=None):
        queryset = Meal.objects.filter(name__icontains=name)
        model = Meal
        serializer_class = MealSerializer(queryset, many=True)
        return Response(serializer_class.data)

#okei
class ActivitySearchView(APIView):  
    def get(self, request, name, format=None):
        queryset = Activity.objects.filter(name__icontains=name)
        model = Activity
        serializer_class = ActivitySerializer(queryset, many=True)
        return Response(serializer_class.data)        

#okei
class BodyIndexView(APIView):

    def get(self, request, pk, format=None):
        prof = Profile.objects.filter(pk=pk).first()
        bmi=float("{0:.2f}".format(prof.weight/(prof.height**2)))
        json={}
        json["bmi"]=bmi
        return Response(json)


