from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit only their profile"""

    def has_object_permission(self,request,view,obj):
        """checks if user has permission to edit"""
        if request.method in permissions.SAFE_METHODS:#safe methods ae create and retreive
            return True

        return obj.id == request.user.id

class UpdateOwnStatus(permissions.BasePermission):
    """Allow user to edit only their profile"""

    def has_object_permission(self,request,view,obj):
        """checks if user has permission to edit"""
        if request.method in permissions.SAFE_METHODS:#safe methods ae create and retreive. Non safe methods are put,patch, delete
            return True

        return obj.user_profile.id == request.user.id#checks whether the status is associated with current user or owned by the user making http req
