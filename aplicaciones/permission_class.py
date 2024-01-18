from rest_framework.permissions import BasePermission

class IsActiveUserPermission(BasePermission):


    def has_permission(self, request, view):
    
        if not request.user.is_active:
            return False
        
        return True
    
class IsJefeUserPermission(BasePermission):
   

    def has_permission(self, request, view):

        if not request.user.cargo == 'Jefe':

            return False
        
        return True