from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password,userType,commit=True):
        if not email:
            raise ValueError(_('Email Address can not be empty!'))
        if not userType:
            raise ValueError(_('User Type can not be empty!'))
        user = self.model(
            email=self.normalize_email(email),
            userType = userType,
        )
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email,password, userType):

        if password is None:
            raise TypeError('Password can not be empty!')
        if not userType:
            raise ValueError(_('User Type can not be empty!'))

        user = self.create_user(email.lower(), password,userType.lower())
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user