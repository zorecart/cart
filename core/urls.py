from django.urls import include, path
from . views import *

app_name = 'core'

urlpatterns = [

    path('', home, name='index'),
    path('ref/<str:ref_code>/<str:username>/', index, name='index'),
    path('referral', referral, name='referral'),

    #path('giftweb/', include('giftweb.urls', namespace='giftweb')),

]