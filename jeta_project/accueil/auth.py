from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
import logging

logger = logging.getLogger(__name__)
# TODO: Create a custom auth that allows non-super users to connect on site as well...

class CustomAuth(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        print("In the authentification")
        try:
            print("got to here")
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            print("in an error")
            return None
        if user.is_active and user.check_password(password):
            if user.is_staff:
                return user
            elif user.groups.first().name == "Players":
                print("this is part of the players")
                return user
            else: 
                logger.warning("Trying to authenticate non-staff user {0}".format(username))
                return None

            # if check_password(password, user.password):
    #         if user.check_password(password):
    #             print("user is good")
    #             return user
    def get_user(self, user_id):
        try:
            print("getting user")
            user = CustomUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except CustomUser.DoesNotExist:
            return None
    
    # def has_perm(self, user_obj, perm, obj=None):
    #     return user_obj