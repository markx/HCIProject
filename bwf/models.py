from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.core import validators
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin, BaseUserManager



class UserManager(BaseUserManager):

    def _create_user(self, email, last_name, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model( email=email, last_name=last_name,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, last_name, password=None, **extra_fields):
        return self._create_user( email,last_name, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, last_name, password, **extra_fields):
        return self._create_user(email, last_name, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Create a user model that uses email as id
    """
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['last_name']

    email = models.EmailField(_('email address'),  unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30 )
        
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()


    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
 
    def __unicode__(self):
        name = "%s %s" %(self.first_name, self.last_name)
        return name.strip()

    def get_short_name(self):
        return self.last_name


    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Friend(models.Model):
    email = models.EmailField(_('email address'),  unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30 )
    created_time = models.DateTimeField(default=timezone.now)
    friendof = models.ForeignKey('User')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __unicode__(self):
        return self.get_full_name()


class BillManager(models.Manager):
    def owe_me(self, User):
        return self.filter(creditor=User.email)

    def owe_them(self, User):
        return self.filter(debtor=User.email)

    def get_by_friend(self, user, friend):
        me = user.email
        return self.filter(creditor=me, debtor=friend) | self.filter(creditor=friend, debtor=me)

class Bill(models.Model):
    creditor = models.EmailField();
    debtor = models.EmailField();
    amount = models.FloatField();
    description = models.CharField(max_length=40, blank=True)
    bill_time = models.DateField()
    created_time = models.DateTimeField(default=timezone.now)
    
    objects = BillManager()

    def __unicode__(self):
        return "%s owes %s %s" %(self.debtor, self.creditor, self.amount)
