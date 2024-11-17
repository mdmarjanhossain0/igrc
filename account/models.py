from re import T
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_ckeditor_5.fields import CKEditor5Field


class MyAccountManager(BaseUserManager):

	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError("User must have an phone number")
		if not username:
			raise ValueError("User must have an username address")

		user = self.model(
			username=username,
			email=email
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=email,
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
	ADMIN = "Admin"
	# TENANT_ADMIN = "T_Admin"
	EMPLOYEE = "Employee"
	AUDITOR = "Auditor"

	ROLE_CHOICES = [
		(ADMIN, ADMIN),
		(EMPLOYEE, EMPLOYEE),
		(AUDITOR, AUDITOR)
	]
	
	date_joined                 = models.DateTimeField(verbose_name="date_joined", auto_now_add=True)
	last_login                  = models.DateTimeField(verbose_name="last_login", auto_now=True)
	otp                         = models.CharField(max_length=6, null=True, blank=True)
	otp_send_time               = models.DateTimeField(null=True, blank=True)
	
	is_admin                    = models.BooleanField(default=False)
	is_active                   = models.BooleanField(default=True)
	is_staff                    = models.BooleanField(default=False)
	is_superuser                = models.BooleanField(default=False)

	email                       = models.EmailField(unique=True, null=False, blank=False)
	username                    = models.CharField(max_length=100, null=False, blank=False)
	profile_picture             = models.ImageField(upload_to=profile_picture_location, null=True, blank=True)


	is_verified                 = models.BooleanField(default=False)
	verified_at                 = models.DateTimeField(null=True, blank=True)

	tenant_limit                = models.IntegerField(default=1)

	role                        = models.CharField(max_length=100, choices=ROLE_CHOICES)
	groups                      = models.ManyToManyField(Group, related_name="account_groups", blank=True)
	user_permissions            = models.ManyToManyField(Permission, related_name="account_permissions", blank=True)

	

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ["username", ]

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# def has_perm(self, perm, obj=None):
	#     return self.is_admin

	# def has_module_perms(self, app_level):
	#     return True

	def save(self, *args, **kwargs):
		super(Account, self).save(*args, **kwargs)




class Audit(models.Model):
	title = models.CharField(max_length=60)
	project = models.ForeignKey("app.Project", on_delete=models.CASCADE)
	auditor = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=False)

	# copy from Account model because maybe user will deleted
	username = models.CharField(max_length=100)

	start = models.DateTimeField(null=False, blank=False)
	end = models.DateTimeField(null=False, blank=False)

	review = models.TextField(null=True, blank=True)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)


	def save(self, *args, **kwargs):
		if self.auditor:
			self.username = self.auditor.username
		super(Audit, self).save(*args, **kwargs)