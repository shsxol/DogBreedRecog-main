from .views import *
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name = "home"),
    path('about/',views.about_page, name='about'),
    path('members/',views.members_grp, name = 'members'),
    path('prediction/',views.prediction, name = 'prediction'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
