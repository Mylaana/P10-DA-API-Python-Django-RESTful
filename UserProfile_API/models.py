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

    def create_user(self, email, date_of_birth,
                    can_be_contacted, can_be_shared, password=None):
        """Create user in database"""

        if not email:
            raise ValueError("User must have an email adress")

        if not date_of_birth:
            raise ValueError("User must have a date of birth")

        if self._calculate_age(date_of_birth) < MINIMUM_AGE:
            # user under age of MINIMUM_AGE cant have their data shared
            can_be_shared = False

        email = self.normalize_email(email)

        user = self.model(email=email, date_of_birth=date_of_birth,
                          can_be_contacted=can_be_contacted, can_be_shared=can_be_shared)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, date_of_birth,
                         can_be_contacted, can_be_shared, password):
        """Create superuser in database"""

        user = self.create_user(email=email, date_of_birth=date_of_birth,
                                can_be_contacted=can_be_contacted,
                                can_be_shared=can_be_shared, password=password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True

        user.save(using=self.db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database user model"""
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth', 'can_be_contacted', 'can_data_be_shared', 'email']

    def __str__(self) -> str:
        """returns user email and birth date"""
        return f"email: {self.email}, birth date: {self.date_of_birth}"

class Contributor(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        primary_key=True
    )
