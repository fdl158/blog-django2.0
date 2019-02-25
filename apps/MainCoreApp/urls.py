from django.urls import re_path, path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    re_path('article/(?P<typeof>.*)/(?P<pid>.*)/', views.ArticleView.as_view(), name="article"),
    re_path('list/(?P<typeof>.*)/', views.ArticleView.as_view(), name="list"),
    path('ThumbUp/', views.ThumbUp, name="ThumbUp"),
    path('GetSoreUpView/<str:model_name>/<int:pk>/<str:is_up>/', views.GetSoreUpView.as_view())
]

