from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('songs', views.SongViewSet)

router.register('genres', views.GenreViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('remove_comment', views.CommentDeleteView.as_view()),
    path('add_comment', views.CommentCreateView.as_view())
]
