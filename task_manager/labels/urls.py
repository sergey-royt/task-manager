from django.urls import path
from .views import LabelIndexView, LabelCreateView


urlpatterns = [
    path('', LabelIndexView.as_view(), name='labels_index'),
    path('create/', LabelCreateView.as_view(), name='labels_create')
]
