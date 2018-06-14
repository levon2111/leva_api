from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import AbstractBaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class User(AbstractUser, AbstractBaseModel):
    username = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    phone = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    zip_code = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    email = models.EmailField(unique=True)
    email_confirmation_token = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )
    reset_key = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Users'


class Syndicate(models.Model):
    FOCUS_TYPES = (
        ('seed', 'Seed'),
        ('seed1', 'Seed1'),
        ('seed2', 'Seed2'),
    )
    INDUSTRY_TYPES = (
        ('biotech', 'Biotech'),
        ('biotech1', 'Biotech1'),
        ('biotech2', 'Biotech2'),
    )
    PRIVACY_TYPES = (
        ('public', 'Public'),
        ('public1', 'Public1'),
        ('public2', 'Public2'),
    )
    CURRENCY_TYPES = (
        ('usd', 'USD'),
        ('amd', 'AMD'),
        ('eur', 'EUR'),
        ('rub', 'RUB')
    )
    HORIZON_TYPES = (
        ('3year', '<3year'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    focus = models.CharField(
        choices=FOCUS_TYPES,
        max_length=255,
        default='seed',
    )
    industry = models.CharField(
        choices=INDUSTRY_TYPES,
        max_length=255,
        default='biotech',
    )
    privacy = models.CharField(
        choices=PRIVACY_TYPES,
        max_length=255,
        default='public',
    )
    currency = models.CharField(
        choices=CURRENCY_TYPES,
        max_length=255,
        default='usd',
    )
    horizon = models.CharField(
        choices=HORIZON_TYPES,
        max_length=255,
        default='public',
    )
    capital_raised = models.IntegerField(null=False, blank=False)
    min_commitment = models.IntegerField(null=False, blank=False)
    leadership_commitment = models.IntegerField(null=False, blank=False)
    personal_note = models.TextField(null=False, blank=False)

    @property
    def get_members_count(self):
        return SyndicateMember.objects.filter(user=self.user).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Syndicate'


class SyndicateMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    syndicate = models.ForeignKey(Syndicate, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = 'Syndicate Member'


class InvitedToSyndicate(models.Model):
    syndicate = models.ForeignKey(Syndicate, on_delete=models.CASCADE, null=False)
    token = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name_plural = 'Invited To Syndicate'
