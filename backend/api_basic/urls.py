from django.urls import path
from django.urls.conf import include
from .views import TrendingTweetsView
from rest_framework.routers import DefaultRouter


#router = DefaultRouter()
#router.register('article', ArticleViewSet, basename='article')

urlpatterns = [
    path('trendingtweets/', TrendingTweetsView.as_view())

]
