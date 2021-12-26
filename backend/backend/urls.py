from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'groups',views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restapi',include(router.urls)),
    path('get-recommendation/<slug:slug>/',views.recommendation),
    path("ac",views.homes),
    path('api',views.movie_choose),
    path('api-auth/', include('rest_framework.urls')),
    path("budget",views.budget),
    path("donate",views.donate),
    path("movie",views.movie),
    path("",views.home),
    path("tracking",views.tracking),
    path("trackingDetails",views.trackingDetails),
    path("send",views.send),
    path("recepies",views.recepie),
]
