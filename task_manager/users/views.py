from django.views.generic.list import ListView
from django.contrib.auth.models import User


# Create your views here.
class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
