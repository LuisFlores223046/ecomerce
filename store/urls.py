from django.urls from path
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),

]