
from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_username

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager/Team Lead'),
        ('employee', 'Employee'),  # Add employee role
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    username = models.CharField(
        max_length=150,
        validators=[validate_username],
        unique=True,
    )

    # Fix the reverse relation clash
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # avoid clash
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",  # avoid clash
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.email
