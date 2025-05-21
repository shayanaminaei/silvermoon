from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, fullname, phone, password, **extra_fields):

        if not phone:
            raise ValueError("Users must have an phone number")

        user = self.model(
            phone=phone,
            fullname=fullname,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, fullname=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(fullname, phone, password, **extra_fields)
