from rest_framework import permissions


class IsSinger(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_author is True


class IsSelfSinger(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.performer


class IsSelfUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


