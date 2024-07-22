from django.urls import path
from .views import ReceiverViewset, SenderViewset, CreateletterViewset, DetailletterViewset, BoxletterViewset

urlpatterns = [
    path('receiver/',ReceiverViewset.as_view(),name = 'receiver'),
    path('sender/',SenderViewset.as_view(),name = 'sender'),
    path('createletter/',CreateletterViewset.as_view(),name = 'createletter'),
    path('detailletter/<int:id>/',DetailletterViewset.as_view(),name = 'detailletter'),
    path('boxletter/',BoxletterViewset.as_view(),name = 'boxletter'),

]