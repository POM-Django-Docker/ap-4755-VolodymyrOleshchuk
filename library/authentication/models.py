import time
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


def current_timestamp():
    return int(time.time())


ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", 1)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.IntegerField(default=current_timestamp)
    updated_at = models.IntegerField(default=current_timestamp)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.id} {self.first_name} {self.middle_name} {self.last_name} {self.email} {self.role} {self.is_active}"

    def __repr__(self):
        return f"CustomUser(id={self.id})"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    @staticmethod
    def get_by_id(user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        user = CustomUser.get_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        user = CustomUser(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            is_active=True
        )
        user.set_password(password)
        user.save()
        return user

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "role": self.role,
            "is_active": self.is_active,
            "is_staff": self.is_staff,
            "is_superuser": self.is_superuser,
        }

    def update(self, first_name=None, last_name=None, middle_name=None,
               password=None, role=None, is_active=None,
               is_staff=None, is_superuser=None):
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if middle_name is not None:
            self.middle_name = middle_name
        if password is not None:
            self.set_password(password)
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        if is_staff is not None:
            self.is_staff = is_staff
        if is_superuser is not None:
            self.is_superuser = is_superuser

        self.updated_at = int(time.time())
        self.save()

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        return dict(ROLE_CHOICES).get(self.role)