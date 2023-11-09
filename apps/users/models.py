from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, GroupManager, PermissionManager
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'      

    def __str__(self):
        return f'{self.id}'

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField('Correo Electrónico',
                              max_length=255, unique=True,)
    name = models.CharField('Nombres', max_length=255, blank=True, null=True)
    last_name = models.CharField(
        'Apellidos', max_length=255, blank=True, null=True)
    image = models.ImageField(
        'Imagen de perfil', upload_to='perfil/', max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   
    historical = HistoricalRecords()
    objects = UserManager()
    

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name']

    def __str__(self):
        return f'{self.name} {self.last_name}'

class UsersUserGroups(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE, verbose_name="Roles")

    class Meta:
        managed = False
        verbose_name = 'Usuario-Grupo'
        verbose_name_plural = 'Usuarios-Grupos'
        db_table = 'users_user_groups'
        unique_together = (('user', 'group'),)

    # def __str__(self):
    #     return f'{self.user.username} - {self.group.name}'

#