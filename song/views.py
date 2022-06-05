from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsSinger, IsSelfSinger, IsSelfUser
from . import serializers
from rest_framework.viewsets import ModelViewSet
from .models import Song, Like, Favorite, Genre, Comments
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


class StandartPaginationClass(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = serializers.SongSerializer
    pagination_class = StandartPaginationClass
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('genre', 'performer')
    search_fields = ('title',)
    # permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(performer=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated(), ]
        else:
            return [IsSinger(), IsSelfSinger(), ]

    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        song = self.get_object()
        if request.user.likes.filter(song=song).exists():
            return Response('u already liked this song', status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(song=song, user=request.user)
        return Response('You put like', status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def remove_from_liked(self, request, pk):
        song = self.get_object()
        if not request.user.likes.filter(song=song).exists():
            return Response('u haven\'t liked the post', status=status.HTTP_400_BAD_REQUEST)
        request.user.likes.filter(song=song).delete()
        return Response('ur like is deleted', status=status.HTTP_204_NO_CONTENT)

    @action(['POST'], detail=True)
    def add_to_favorites(self, request, pk):
        song = self.get_object()
        if request.user.favorites.filter(song=song).exists():
            return Response('u have already added this song to favorites', status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(song=song, user=request.user)
        return Response('You added it to favorites', status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def remove_from_favorites(self, request, pk):
        song = self.get_object()
        if not request.user.favorites.filter(song=song).exists():
            return Response('u haven\'t added it to favorites', status=status.HTTP_400_BAD_REQUEST)
        request.user.favorites.filter(song=song,).delete()
        return Response('The song is removed from favorites', status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer

    def get_permissions(self):
            if self.action in ['list', 'retrieve']:
                return [permissions.IsAuthenticated(), ]
            else:
                return [permissions.IsAdminUser(), ]


# class SongCreateView(generics.CreateAPIView):
#     queryset = Song.objects.all()
#     permission_classes = (IsSinger,)
#     serializer_class = serializers.SongSerializer
#
#
# class SongDetailView(generics.RetrieveAPIView):
#     queryset = Song.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = serializers.SongSerializer
#
#
# class SongDeleteView(generics.DestroyAPIView):
#     queryset = Song.objects.all()
#     permission_classes = (IsSelfSinger,)
#     serializer_class = serializers.SongSerializer


# class SongUpdateView(generics.UpdateAPIView):
#     queryset = Song.objects.all()
#     permission_classes = (IsSelfSinger,)
#     serializer_class = serializers.SongSerializer




# class LikesViewSet(ModelViewSet):
#     queryset = Like.objects.all()
#     permissions = (permissions.IsAuthenticated,)
#     serializer_class = serializers.LikeSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:
#             return [permissions.IsAuthenticated(), ]
#         else:
#             return [IsSelfUser(), IsSelfSong(), ]


class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = (IsSelfUser,)
    serializer_class = serializers.CommentSerializer
    queryset = Comments.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.CommentSerializer
    queryset = Comments.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)