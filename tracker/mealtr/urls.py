from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

urlpatterns = [
   url(r'^api/component/$', views.ComponentView.as_view(), name='component-list'), 
   url(r'^api/component/(?P<pk>[0-9]+)/$', views.ComponentDetailView.as_view(), name='component'), 
   url(r'^api/property/$', views.PropertyView.as_view(), name='property-list'), 
   url(r'^api/property/(?P<pk>[0-9]+)/$', views.PropertyDetail.as_view()),
   url(r'^api/profile/$', views.ProfileView.as_view(), name='profile-list'), 
   url(r'^api/profile/(?P<pk>[0-9]+)/$', views.ProfileDetailView.as_view(), name='profile-list'), 
   url(r'^api/meal/$', views.MealView.as_view(), name='meal-list'), 
   url(r'^api/meal/(?P<pk>[0-9]+)/$', views.MealDetailView.as_view(), name='meal-component-list'),
   url(r'^api/user/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='user-list'), 
   url(r'^api/activity/$', views.ActivityView.as_view(), name='activity-list'), 
   url(r'^api/activity/(?P<pk>[0-9]+)/$', views.ActivityDetailView.as_view(), name='user-list'), 
   url(r'^api/day/$', views.DayView.as_view(), name='day-list'), 
   url(r'^api/jwt-auth/', obtain_jwt_token),
   url(r'^api/token-refresh/', refresh_jwt_token),
   path('api/day/<int:year>/<int:month>/<int:day>/', views.DayDetailView.as_view(), name='day-list'), 
   url(r'^api/registration/$', views.RegView.as_view(), name='registration'), 
   url(r'^api/meal/(?P<name>.+)/$', views.MealSearchView.as_view(), name='meal-list'), 
   url(r'^api/activity/(?P<name>.+)/$', views.ActivitySearchView.as_view(), name='meal-list'),
   path('api/day/<int:year>/<int:month>/<int:day>/meals/', views.MealToDayView.as_view(), name='day-meals'),
   path('api/day/<int:year>/<int:month>/<int:day>/meals/<int:pk>/', views.MealFromDayView.as_view(), name='day-meals'), 
   path('api/day/<int:year>/<int:month>/<int:day>/activities/', views.ActivityToDayView.as_view(), name='day-activities'),
   path('api/day/<int:year>/<int:month>/<int:day>/activities/<int:pk>/', views.ActivityFromDayView.as_view(), name='day-activities'), 
   url(r'^api/profile/bmi/(?P<pk>[0-9]+)/$', views.BodyIndexView.as_view(), name='bmi-index'),
]

urlpatterns = format_suffix_patterns(urlpatterns)