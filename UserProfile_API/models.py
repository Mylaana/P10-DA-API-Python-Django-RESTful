from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from dateutil.relativedelta import relativedelta


MINIMUM_AGE = 15

class UserProfileManager(BaseUserManager):
    """Database User Manager model"""

    def _calculate_age(self, birth_date):
        today = date.today()
        age = relativedelta(today, birth_date)
        return age.years

    def create_user(self, email, date_of_birth, password=None):
        """Create user in database"""

        if not email:
            raise ValueError("User must have an email adress")

        if not date_of_birth:
            raise ValueError("User must have a date of birth")

        if self._calculate_age(date_of_birth) < MINIMUM_AGE:
            raise ValueError("User must be 15 years old or above")

        email = self.normalize_email(email)

        user = self.model(email=email, date_of_birth=date_of_birth)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, date_of_birth, password):
        """Create superuser in database"""

        user = self.create_user(email, date_of_birth, password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True

        user.save(using=self.db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database user model"""

    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    contact_me = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'contact_me']

    def __str__(self) -> str:
        """returns user email and birth date"""
        return f"email: {self.email}, birth date: {self.date_of_birth}"
