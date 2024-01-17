from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # print("at EmailBackend")
        UserModel = get_user_model()
        # print("UserModel: ", UserModel)
        try:
            user = UserModel.objects.get(email=username)
            # print("user: ", user  )
        except UserModel.DoesNotExist:
            # print("UserModel.DoesNotExist")
            return None

        if user.check_password(password):
            # print("checked password")
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None