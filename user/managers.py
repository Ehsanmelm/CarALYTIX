from django.contrib.auth.models import BaseUserManager
from role.models import Role

class UserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,role=None):

        if not email:
            raise ValueError("Users must have an email")
        if not first_name:
            raise ValueError("Users must have an first_name")
        if not last_name:
            raise ValueError("Users must have an last_name")

        if role:
            user_role=role
        else:
            user_role=Role.objects.get(name="user")
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=user_role,
        )
        user.save(using=self._db)
        return user

    
    def create_superuser(self,email,first_name,last_name,role):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=Role.objects.get(name="admin")
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user