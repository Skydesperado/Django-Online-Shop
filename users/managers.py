from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, first_name, last_name,
                    password):
        if not phone_number:
            raise ValueError("The Phone Number Field Must Be Set")
        if not email:
            raise ValueError("The Email Field Must Be Set")
        if not first_name:
            raise ValueError("The First Name Field Must Be Set")
        if not last_name:
            raise ValueError("The Last Name Field Must Be Set")
        user = self.model(phone_number=phone_number,
                          email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, first_name, last_name,
                         password):
        user = self.create_user(phone_number, email, first_name, last_name,
                                password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
