from django.contrib.auth.models import BaseUserManager
from role.models import Role

class UserManager(BaseUserManager):
    def create_user(self,email,password,first_name,last_name,role=None):

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
        user.set_password(password)
        return user

    
    def create_superuser(self,email,password,first_name,last_name,role):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=Role.objects.get(name="admin")
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff=True
        user.save(using=self._db)
        return user