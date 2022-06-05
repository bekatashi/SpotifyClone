from rest_framework import permissions


class IsSelfUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.email == obj.email


class IsNotSelfUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.email == obj.singer.email
