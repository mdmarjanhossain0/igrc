from re import T
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_ckeditor_5.fields import CKEditor5Field
from slugify import slugify


class MyAccountManager(BaseUserManager):

    def create_user(self, mobile, username, password=None):
        if not mobile:
            raise ValueError("User must have an phone number")
        if not username:
            raise ValueError("User must have an username address")

        user = self.model(
            username=username,
            mobile=mobile
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, username, password):
        user = self.create_user(
            mobile=mobile,
            username=username
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def profile_picture_location(instance, filename):
    file_path = 'pp/{filename}'.format(
        filename=filename
    )
    return file_path

class Account(AbstractBaseUser, PermissionsMixin):
    STUDENT = "Student"
    TEACHER = "Teacher"
    ROLES = (
        (STUDENT, STUDENT),
        (TEACHER, TEACHER)
    )

    date_joined                 = models.DateTimeField(verbose_name="date_joined", auto_now_add=True)
    last_login                  = models.DateTimeField(verbose_name="last_login", auto_now=True)
    otp                         = models.CharField(max_length=6, null=True, blank=True)
    otp_send_time               = models.DateTimeField(null=True, blank=True)
    is_admin                    = models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)


    mobile                      = models.CharField(max_length=11, unique=True, verbose_name='mobile')
    username                    = models.CharField(max_length=100, null=False, blank=False)
    profile_picture             = models.ImageField(upload_to=profile_picture_location, null=True, blank=True)

    institution                 = models.CharField(max_length=255, null=True)
    occupation                  = models.CharField(max_length=255, null=True)

    level                       = models.CharField(max_length=32, null=True, blank=True)
    department                  = models.CharField(max_length=32, null=True, blank=True)
    favorite_subject            = models.CharField(max_length=32, null=True, blank=True)
    slug                        = models.CharField(max_length=32, blank=True, unique=True)
    role                        = models.CharField(max_length=32, default=STUDENT, choices=ROLES)
    is_verified                 = models.BooleanField(default=False)

    # Socal Medias
    email                       = models.CharField(max_length=100, null=False, blank=False)
    facebook                    = models.CharField(max_length=255, null=True)      
    youtube                     = models.CharField(max_length=255, null=True)      
    telegram                    = models.CharField(max_length=255, null=True)      
    insta                       = models.CharField(max_length=255, null=True)

    region                      = models.CharField(max_length=255, null=True)
    district                    = models.CharField(max_length=255, null=True)
    division                    = models.CharField(max_length=255, null=True)
    lat                         = models.DecimalField(max_digits=10, decimal_places=2)      
    long                        = models.DecimalField(max_digits=10, decimal_places=2)      


    

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ["username", ]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    # def has_module_perms(self, app_level):
    #     return True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
            if Account.objects.filter(slug=slugify(self.username)).exists():
                self.slug = slugify(self.username + self.mobile)
        super(Account, self).save(*args, **kwargs)



class ChatGroup(models.Model):
    pass

def cover_image_location(instance, filename):
    file_path = 'cover_image/{filename}'.format(
        filename=filename
    )
    return file_path

class CoverImage(models.Model):
    image = models.ImageField(upload_to=cover_image_location)


def organization_logo_location(instance, filename):
    file_path = 'organization/{filename}'.format(
        filename=filename
    )
    return file_path

class Organization(models.Model):
    owner                       = models.OneToOneField(Account, on_delete=models.CASCADE)
    name                        = models.CharField(max_length=100, null=True, blank=True, unique=True)
    is_online                   = models.BooleanField(default=True)
    title                       = models.CharField(max_length=255)
    description                 = CKEditor5Field("Text", config_name="extends")

    # 1, 2, 3, 4, 5, 6.... 12
    levels                      = models.CharField(max_length=100, null=True, blank=True)
    departments                 = models.CharField(max_length=255, null=True, blank=True)
    logo                        = models.ImageField(upload_to=organization_logo_location, null=True, blank=True)
    cover_images                 = models.ManyToManyField()
    is_verified                 = models.BooleanField(default=False)
    domain                      = models.CharField(max_length=32, null=False, blank=False)
    members                     = models.ManyToManyField(Account)

    email                       = models.CharField(max_length=100, null=False, blank=False)
    facebook                    = models.CharField(max_length=255, null=True)      
    youtube                     = models.CharField(max_length=255, null=True)      
    telegram                    = models.CharField(max_length=255, null=True)      
    insta                       = models.CharField(max_length=255, null=True)

    region                      = models.CharField(max_length=255, null=True)
    district                    = models.CharField(max_length=255, null=True)
    division                    = models.CharField(max_length=255, null=True)
    address                     = models.CharField(max_length=255)
    lat                         = models.DecimalField(max_digits=10, decimal_places=2)      
    long                        = models.DecimalField(max_digits=10, decimal_places=2)

    # success_story
    # reviews
    # courses
    # theme

    def __str__(self):
        return self.account.username

    def save(self, *args, **kwargs):
        if not self.domain:
            self.domain = slugify(self.name)
            if Organization.objects.filter(domain=slugify(self.name)).exists():
                self.domain = slugify(self.name + self.owner.mobile)
        super(Organization, self).save(*args, **kwargs)
