from django.db import models
from django.contrib.auth.models import (AbstractUser, Group, Permission)
from django.core.validators import (MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator)
from django.urls import reverse
from django.utils.html import format_html

from .apps import (SimplifyConfig as conf)
from .manager import UserManager

from . import methods
if conf.ldap.enable: from .methods import method_ldap

import os, subprocess, unicodedata, time

#██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗
#██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
#██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  
#██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  
#╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗
# ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
class Update(models.Model):
    date_create = models.DateTimeField(conf.vn.date_create, auto_now_add=True, editable=False)
    date_update = models.DateTimeField(conf.vn.date_update, auto_now=True, editable=False)
    update_by   = models.CharField(conf.vn.update_by, blank=True, editable=False, help_text=conf.ht.update_by, max_length=254, null=True)
    error       = models.TextField(conf.vn.error, blank=True, help_text=conf.ht.error, null=True)
    message     = models.TextField(conf.vn.message, blank=True, help_text=conf.ht.message, null=True)

    class Meta:
        abstract = True

    def status(self):
        return True if self.error is None else False
    status.boolean = True

# ██████╗ ██████╗  ██████╗ ██╗   ██╗██████╗ 
#██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██╔══██╗
#██║  ███╗██████╔╝██║   ██║██║   ██║██████╔╝
#██║   ██║██╔══██╗██║   ██║██║   ██║██╔═══╝ 
#╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║     
# ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  
class Group(Group, Update):
    class Meta:
        verbose_name        = conf.vbn.group
        verbose_name_plural = conf.vpn.group


#███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ 
#████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗
#██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║
#██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║
#██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
#╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
class Method(Update):
    method          = models.CharField(conf.vn.method, choices=conf.choices.method_method, help_text=conf.ht.method, max_length=4)
    name            = models.CharField(conf.vn.name_method, help_text=conf.ht.name_method, max_length=254)
    enable          = models.BooleanField(conf.vn.enable, default=True, help_text=conf.ht.enable)
    port            = models.PositiveIntegerField(conf.vn.port, blank=True, default=0, help_text=conf.ht.port, null=True, validators=[MinValueValidator(0), MaxValueValidator(65535)])
    tls             = models.BooleanField(conf.vn.tls, default=False, help_text=conf.ht.tls)
    certificate     = models.TextField(conf.vn.certificate, blank=True, help_text=conf.ht.certificate, null=True)
    self_signed     = models.BooleanField(conf.vn.self_signed, default=False, help_text=conf.ht.self_signed)
    is_active       = models.BooleanField(conf.vn.is_active, default=True)
    is_staff        = models.BooleanField(conf.vn.is_staff, default=False)
    is_superuser    = models.BooleanField(conf.vn.superuser, default=False)
    groups          = models.ManyToManyField(Group, verbose_name=conf.vn.groups, blank=True)
    permissions     = models.ManyToManyField(Permission, verbose_name=conf.vn.permissions, blank=True)
    field_firstname = models.CharField(conf.vn.field_firstname, blank=True, help_text=conf.ht.field, max_length=254, null=True)
    field_lastname  = models.CharField(conf.vn.field_lastname, blank=True, help_text=conf.ht.field, max_length=254, null=True)
    field_email     = models.CharField(conf.vn.field_email, blank=True, help_text=conf.ht.field, max_length=254, null=True)

    if conf.ldap.enable:
        ldap_host       = models.CharField(conf.vn.ldap_host, blank=True, default='localhost', help_text=conf.ht.ldap_host, max_length=254, null=True)
        ldap_define     = models.CharField(conf.vn.ldap_define, blank=True, help_text=conf.ht.ldap_define, max_length=254, null=True)
        ldap_scope      = models.CharField(conf.vn.ldap_scope, choices=conf.choices.ldap_scope, default=conf.choices.ldap_scope_base, help_text=conf.ht.ldap_scope, max_length=14)
        ldap_version    = models.CharField(conf.vn.ldap_version, choices=conf.choices.ldap_version, default=conf.choices.ldap_version3, help_text=conf.ht.ldap_version, max_length=8)
        ldap_bind       = models.CharField(conf.vn.ldap_bind, blank=True, help_text=conf.ht.ldap_bind, max_length=254, null=True)
        ldap_password   = models.CharField(conf.vn.ldap_password, blank=True, help_text=conf.ht.ldap_password, max_length=254, null=True)
        ldap_user       = models.TextField(conf.vn.ldap_user, blank=True, help_text=conf.ht.ldap_user, null=True)
        ldap_search     = models.TextField(conf.vn.ldap_search, help_text=conf.ht.ldap_search, blank=True, null=True)
        ldap_tls_cacert = models.BooleanField(conf.vn.ldap_tls_cacert, default=False, help_text=conf.ht.ldap_tls_cacert)

    class Meta:
        verbose_name        = conf.vbn.method
        verbose_name_plural = conf.vpn.method
        permissions         = (
            ('can_read_method',   conf.ht.can_read_method),
            ('can_check_method',  conf.ht.can_check_method),
            ('can_writecert_method',  conf.ht.can_writecert_method))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('%s:method-detail' % conf.namespace, kwargs={ 'pk': self.id, 'extension': '.html' })

    def save(self, *args, **kwargs):
        super(Method, self).save(*args, **kwargs)
        self.certificate_content()

    def certificate_path(self):
        return None if self.certificate in [None, ''] else '{}/{}_{}.crt'.format(conf.directory.certificates, self.name, self.method)
    certificate_path.short_description = conf.ht.certificate_path

    def certificate_content(self):
        if self.certificate not in [None, '']:
            certificate = self.certificate_path()
            if not os.path.isfile(certificate):
                self.certificate_write(certificate)
            else:
                timestamp_file = os.path.getctime(certificate)
                timestamp_date_update = int(time.mktime(self.date_update.timetuple()))
                if timestamp_file < timestamp_date_update:
                    self.certificate_write(certificate)
            return self.certificate
        return None
    certificate_content.short_description = conf.ht.certificate_content

    def certificate_write(self, certificate):
        with open(certificate, 'w') as cert_file:
            cert_file.write(self.certificate)
        cert_file.closed

    def admin_button_check(self):
        url = reverse('admin:admin-method-check',  args=[self.id])
        return format_html('<a class="button" href="{url}">{vn}</a>'.format(url=url, vn=conf.vn.check))
    admin_button_check.short_description = conf.vn.check

    def admin_download_certificate(self):
        if self.certificate not in ['', None]:
            url = reverse('simplify:method-get-certificate',  args=[self.id])
            return format_html('<a class="button" href="{url}">{vn}</a>'.format(url=url, vn=conf.vn.certificate))
        return None
    admin_download_certificate.short_description = conf.vn.certificate

    def get_method(self):
        return getattr(getattr(methods, 'method_%s' % self.method.lower()), 'method_%s' % self.method.lower())(self)

#██╗   ██╗███████╗███████╗██████╗ 
#██║   ██║██╔════╝██╔════╝██╔══██╗
#██║   ██║███████╗█████╗  ██████╔╝
#██║   ██║╚════██║██╔══╝  ██╔══██╗
#╚██████╔╝███████║███████╗██║  ██║
# ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
class User(AbstractUser):
    username    = models.CharField(conf.vn.username, blank=conf.user.null_username, max_length=254, null=conf.user.null_username, unique=conf.user.unique_username, validators=[AbstractUser.username_validator],)
    email       = models.EmailField(conf.vn.email, blank=conf.user.null_email, null=conf.user.null_email, unique=conf.user.unique_email)
    is_active   = models.BooleanField(conf.vn.is_active, default=conf.user.is_active)
    is_staff    = models.BooleanField(conf.vn.is_staff, default=conf.user.is_staff)
    is_robot    = models.BooleanField(conf.vn.is_robot, default=conf.user.is_robot)
    first_name  = models.CharField(conf.vn.firstname, blank=conf.user.null_firstname, max_length=30, null=conf.user.null_firstname)
    last_name   = models.CharField(conf.vn.lastname, blank=conf.user.null_lastname, max_length=30, null=conf.user.null_lastname)
    date_joined = models.DateTimeField(conf.vn.date_joined, auto_now_add=True, editable=False)
    date_update = models.DateTimeField(conf.vn.date_update, auto_now=True, editable=False)
    update_by   = models.CharField(conf.vn.update_by, editable=False, max_length=254)
    method      = models.CharField(conf.vn.method, choices=conf.choices.user_method, default=conf.choices.user_backend, max_length=15)
    additional  = models.ManyToManyField(Method, blank=True)
    key         = models.CharField(conf.vn.key, default=conf.key, max_length=32, unique=True, validators=[MaxLengthValidator(conf.user.key_max_length), MinLengthValidator(conf.user.key_min_length),])

    objects = UserManager()
    USERNAME_FIELD = conf.user.username_field
    REQUIRED_FIELDS = conf.user.required_fields

    class Meta:
        verbose_name        = conf.vbn.user
        verbose_name_plural = conf.vpn.user
        ordering            = [conf.user.username_field]
        permissions         = (
            ('can_use_api', conf.ht.can_use_api),
            ('can_read_user', conf.ht.can_read_user),
            ('can_see_email', conf.ht.can_see_email),
            ('can_see_firstname', conf.ht.can_see_firstname),
            ('can_see_lastname', conf.ht.can_see_lastname),
            ('can_see_method', conf.ht.can_see_method),
            ('can_see_groups', conf.ht.can_see_groups),
            ('can_see_permissions', conf.ht.can_see_permissions),
            ('can_see_additional', conf.ht.can_see_additional),
            ('can_see_key', conf.ht.can_see_key),
        )

    def clean(self):
        super(AbstractUser, self).clean()
        if 'username' in self.REQUIRED_FIELDS or self.username is not None:
            self.username = unicodedata.normalize(conf.user.normalize, self.username) 
        self.email = self.__class__.objects.normalize_email(self.email)

#███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
#██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
#███████╗██║     ██████╔╝██║██████╔╝   ██║   
#╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   
#███████║╚██████╗██║  ██║██║██║        ██║   
#╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝
class Script(Update):
    name   = models.CharField(conf.vn.name_script, help_text=conf.ht.name_script, max_length=254, unique=True)
    script = models.CharField(conf.vn.script, help_text=conf.ht.script, max_length=254, unique=True)
    code   = models.TextField(conf.vn.code, help_text=conf.ht.code)

    class Meta:
        verbose_name        = conf.vbn.script
        verbose_name_plural = conf.vpn.script
        permissions         = (('can_read_script', conf.ht.can_read_script),('can_write_script', conf.ht.can_write_script))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('%s:script-detail' % conf.namespace, kwargs={ 'pk': self.id, 'extension': '.html' })

    def script_path(self):
        return '{}/{}.py'.format(conf.directory.tasks, self.script)
    script_path.short_description = conf.ht.script_path

    def script_write(self, script):
        with open(script, 'w') as script_file:
            script_file.write(self.code)
        script_file.closed

    def admin_download_script(self):
        url = reverse('simplify:script-get',  args=[self.id])
        return format_html('<a class="button" href="{url}">{vn}</a>'.format(url=url, vn=conf.vn.script))
    admin_download_script.short_description = conf.vn.script

#████████╗ █████╗ ███████╗██╗  ██╗
#╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
#   ██║   ███████║███████╗█████╔╝ 
#   ██║   ██╔══██║╚════██║██╔═██╗ 
#   ██║   ██║  ██║███████║██║  ██╗
#   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
class Task(Update):
    script      = models.ForeignKey(Script, blank=True, on_delete=models.CASCADE, null=True)
    default     = models.CharField(conf.vn.status, choices=conf.choices.task, blank=True, help_text=conf.ht.default, max_length=18, null=True)
    info        = models.TextField(conf.vn.info, blank=True, null=True, help_text=conf.ht.info)
    status      = models.CharField(conf.vn.status, choices=conf.choices.status_status, default=conf.choices.status_order, max_length=8, help_text=conf.ht.status)
    command     = models.CharField(conf.vn.commmand, blank=True, editable=False, help_text=conf.ht.commmand,  max_length=254, null=True)
    local_check = models.CharField(conf.vn.local_check, blank=True, editable=False, help_text=conf.ht.local_check, max_length=254, null=True)

    class Meta:
        verbose_name        = conf.vbn.task
        verbose_name_plural = conf.vpn.task
        permissions         = (
            ('can_read_task', conf.ht.can_read_task),)

    def __str__(self):
        return self.script.name if self.script else self.get_default_display()

    def get_absolute_url(self):
        return reverse('%s:task-detail' % conf.namespace, kwargs={ 'pk': self.id })

    def prepare(self):
        prepare = {}
        prepare['task']           = self.script.script if self.script else self.default
        prepare['id']             = self.id
        prepare['namespace']      = conf.namespace
        prepare['port']           = conf.task.port
        prepare['background']     = conf.task.background
        prepare['python']         = conf.task.python
        prepare['directory']      = conf.directory.tasks
        prepare['extension']      = conf.task.python_extension
        prepare['background_end'] = conf.task.background_end
        prepare['settings_dir']   = conf.directory.settings
        self.command = conf.task.command.format(**prepare)
        prepare['binary']           = conf.task.binary
        prepare['script']           = conf.task.can_run
        prepare['script_extension'] = conf.task.can_run_extension
        prepare['timeout']          = conf.task.kill_timeout
        prepare['robot']            = conf.task.robot
        prepare['password']         = conf.task.password
        self.local_check = conf.task.local_check.format(**prepare)
        self.save()

    def can_run(self):
        if self.status == conf.choices.status_error:
            return False
        elif self.status != conf.choices.status_order:
            self.error = conf.error.not_order
            self.save()
            return False
        try: 
            subprocess.check_call(self.local_check, shell=True)
            return True
        except subprocess.CalledProcessError as error:
            self.error = error
        return False

    def start_task(self):
        if self.status == conf.choices.status_error:
            return False
        elif self.status != conf.choices.status_ready:
            self.error = conf.error.not_ready
            self.save()
            return False
        try: 
            subprocess.check_call(self.command, shell=True)
            return True
        except subprocess.CalledProcessError as error:
            self.error = error
        return False