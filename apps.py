from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

import datetime, syslog, os, sys, random, string

class Config(object):
    namespace = 'simplify'
    settings_override = 'Simplify'

    class directory:
        app          = os.path.dirname(os.path.realpath(__file__))
        certificates = '%s/certs' % app
        cache        = '%s/cache' % app
        tasks        = '%s/tasks' % app

    class error(object):
        is_superuser    = _('Superuser must have is_superuser=True.')
        required_fields = _('The given field must be set: %s')
        method_check    = _('The method does not works')
        invalid_login   = _("Please enter a correct LDAP login and password. Note that both "
                            "fields may be case-sensitive.")
        inactive        = _("This account is inactive.")
        user_notfound   = _('User Not Found')
        credentials     = _('Invalid credentials')


    class message(object):
        method_works = _('The method works')

    class choices(object):
        method_method = ()
        user_createsuperuser = 'CREATESUPERUSER'
        user_backend         = 'BACKEND'
        user_frontend        = 'FRONTEND'
        user_additional      = 'ADDITIONAL'
        user_method = (
            (user_createsuperuser, _('Create Super User')),
            (user_backend,         _('Back-end')),
            (user_frontend,        _('Front-end')),
            (user_additional,      _('Additional method')),
        )
        status_error    = 'error'
        status_order    = 'order'
        status_ready    = 'ready'
        status_start    = 'start'
        status_running  = 'running'
        status_complete = 'complete'
        status_status   = (
            (status_error,    _('In error')),
            (status_order,    _('Ordered')),
            (status_ready,    _('Ready')),
            (status_start,    _('Started')),
            (status_running,  _('Running')),
            (status_complete, _('Complete')),
        )
        task_purge = 'purge_tasks'
        task_check = 'check_methods'
        task_cache = 'cache_methods'
        task = (
            (task_purge, _('Purge tasks')),
            (task_check, _('Check methods')),
            (task_cache, _('Generate method caches')),
        )
        ldap_scope_base     = 'SCOPE_BASE'
        ldap_scope_onelevel = 'SCOPE_ONELEVEL'
        ldap_scope_subtree  = 'SCOPE_SUBTREE'
        ldap_scope = (
            (ldap_scope_base, 'base (scope=base)'),
            (ldap_scope_onelevel, 'onelevel (scope=onelevel)'),
            (ldap_scope_subtree, 'subtree (scope=subtree)'),
        )
        ldap_version2 = 'VERSION2'
        ldap_version3 = 'VERSION3'
        ldap_version = (
            (ldap_version2, 'Version 2 (LDAPv2)'),
            (ldap_version3, 'Version 3 (LDAPv3)')
        )

    class vn(object):
        date_create     = _('Creation date')
        date_update     = _('Last modification date')
        update_by       = _('Update by')
        error           = _('Error encountered')
        method          = _('Method')
        name_method     = _('Name')
        enable          = _('Enable')
        port            = _('Port')
        tls             = _('Enable TLS')
        is_active       = _('Will be active')
        is_staff        = _('Will be staff')
        superuser       = _('Will be superuser')
        groups          = _('Groups associated')
        permissions     = _('Permissions associated')
        certificate     = _('TLS Certificate')
        check           = _('Check')
        self_signed     = _('Self-signed')
        field_firstname = _('Firstname correspondence')
        field_lastname  = _('Lastname correspondence')
        field_email     = _('Email correspondence')
        heck            = _('Check')
        user            = _('User')
        username        = _('Username')
        email           = _('Email address')
        is_active       = _('Active')
        is_staff        = _('Staff')
        is_robot        = _('Robot')
        firstname       = _('Firstname')
        lastname        = _('Lastname')
        date_joined     = _('Date joined')
        method          = _('Create method')
        key             = _('Authentication key')
        script          = _('Script')
        name_script     = _('Script name')
        script          = _('Script filename')
        code            = _('Python code')
        task            = _('Task')
        info            = _('More informations')
        status          = _('Status')
        commmand        = _('Command')
        local_check     = _('Local check')
        ldap_host       = _('Use hostname or IP address')
        ldap_define     = _('Base DN ex: dc=domain,dc=com')
        ldap_scope      = _('Scope')
        ldap_version    = _('Version')
        ldap_bind       = _('Root DN')
        ldap_password   = _('Root password')
        ldap_user       = _('User DN')
        ldap_search     = _('Search DN')
        ldap_tls_cacert = _('trusted CA certificates')

    class ht(object):
        update_by           = _('Last user who modified.')
        error               = _('Detail about the error.')
        port                = _('Change the port used by the method')
        tls                 = _('Enable or disable TLS')
        certificate         = _('Uploaded here the certificate to check')
        method              = _('Method type')
        name_method         = _('Method name')
        enable              = _('Enable or disable the method')
        certificate_content = _('Certificate content')
        certificate_path    = _('Certificate path')
        self_signed         = _('Is the certificate self-signed?')
        field               = _('Automatically filled field with key map (Keep null if not used)')
        can_update_method   = _('Can update task')
        can_read_method     = _('Can read task')
        can_check_method    = _('Can check method')
        can_use_api         = _('Can use API')
        name_script         = _('Script name')
        script              = _('Script filename without extension .py')
        code                = _('Python code')
        can_update_script   = _('Can update script')
        can_read_script     = _('Can read script')
        default             = _('Default tasks')
        info                = _('Information about the task.')
        status              = _('Task status.')
        commmand            = _('Command used to run the script.')
        local_check         = _('Local check for not duplicate the task.')
        can_update_task     = _('Can update task')
        can_read_task       = _('Can read task')
        ldap_host           = _('Hostname/IP')
        ldap_port           = _('Keep 389 to use default port')
        ldap_tls            = _('Use option TLS')
        ldap_define         = _('Base DN')
        ldap_scope          = _('Choice a scope. The command will be like "scope=***"')
        ldap_version        = _('Choice a version')
        ldap_bind           = _('Bind for override user permission, ex: cn=manager,dc=domain,dc=com (Keep null if not used)')
        ldap_password       = _('Password used by the bind')
        ldap_user           = _('Replace root DN by a User DN. <strong>Do not use with root DN</strong> | user DN ex : uid={{tag}},ou=my-ou,dc=domain,dc=com | Available tags: username')
        ldap_search         = _('search DN (LDAP filter) ex : (&(uid={{tag}})(memberof=cn=my-cn,ou=groups,dc=hub-t,dc=net)) | Available tags: username')
        ldap_tls_cacert     = _('Set path name of file containing all trusted CA certificates')

    class vbn(object):
        method = _('2 - Method')
        user   = _('3 - User')
        group  = _('1 - Group')
        script = _('# Script')
        task   = _('# Task')

    class vpn(object):
        method = _('2 - Methods')
        user   = _('3 - Users')
        group  = _('1 - Groups')
        script = _('# Scripts')
        task   = _('# Tasks')

    class extension(object):
        csv  = 'text/csv'
        html = 'text/html'
        json = 'application/json'
        txt  = 'text/plain'
        xml  = 'application/xml'
        authorized = ['html', 'csv', 'json', 'txt', 'xml']
        regex = 'html'

    class template(object):
        detail = 'simplify/{ext}/detail.{ext}'
        form   = 'simplify/{ext}/form.{ext}'
        listt  = 'simplify/{ext}/list.{ext}'
        admin  = 'simplify/{ext}/admin_{model}_{view}.{ext}'

    class user(object):
        login_method    = 'login_method'
        username_field  = 'username'
        required_fields = []
        unique_username = True
        unique_email    = False
        null_username   = False
        null_email      = False
        null_firstname  = True
        null_lastname   = True
        is_active       = False
        is_staff        = False
        is_robot        = False
        key_min_length  = 10
        key_max_length  = 32
        normalize       = 'NFKC'
        api_backend     = 'user.simplify.api'
        robot_backend   = 'user.simplify.robot'

        def key(key_max_length):
            return ''.join(random.choice('-._~+/'+string.hexdigits) for x in range(key_max_length))

    class admin(object):
        site_header              = _('Django administration')
        index_title              = _('Site administration (assisted by Authenta)')
        verbose_name             = _('Authentication and Authorization')
        login                    = _('Log in')
        log_fieldsets            = (_('Log informations'), {'fields': ('update_by', 'date_create', 'date_update', 'error')})
        method_fieldsets         = (((None, { 'fields': ('method', 'name', 'port', 'enable',), })),
                                   ((_('TLS configuration'), { 'classes': ('collapse',), 'fields': ('tls', 'certificate', 'self_signed')})),
                                   (_('Groups and permissions'), { 'classes': ('collapse',), 'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', )}))
        method_filter_horizontal = ('groups', 'permissions')
        method_list_display      = ('name', 'method', 'enable', 'is_active', 'is_staff', 'is_superuser', 'status','admin_button_check')
        method_readonly_fields   = ('update_by', 'date_create', 'date_update', 'error', 'certificate_path', 'certificate_content')
        method_list_filter       = ('method', 'enable',)
        method_search_fields     = ('name',)

        ldap_fieldsets           = (_('LDAP method'), 
                                   {'classes': ('collapse',),
                                   'fields': ('ldap_host', 'ldap_define', 'ldap_scope', 'ldap_version', 'ldap_bind', 'ldap_password', 'ldap_user', 'ldap_search')})

        user_add_fieldsets       = None
        user_fieldsets           = (((None, {'fields': ('username', 'password')})),
                                   ((_('Personal info'), {'fields': ('email', 'first_name', 'last_name')})),
                                   (_('Authentication method'), {'fields': ('method', 'additional')}),
                                   (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_robot', 'groups', 'user_permissions')}),
                                   (_('API'), {'fields': ('key', )}),
                                   (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
                                   (_('Log informations'), {'fields': ('date_update', 'update_by')}))
        user_filter_horizontal   = ('groups', 'user_permissions', 'additional')
        user_list_display        = None
        user_readonly_fields     = ('date_joined', 'date_update', 'update_by')
        script_fieldsets         = ((None, { 'fields': ('name', 'script', 'code')}),
                                   (_('Log informations'), {'fields': ('update_by', 'date_create', 'date_update', 'error')}))
        script_list_display      = ('name', 'script')
        script_readonly_fields   = ('update_by', 'date_create', 'date_update', 'error')
        task_fieldsets           = ((None, { 'fields': ('script', 'default', 'status', 'info', 'error', 'command', 'local_check')}),
                                   (log_fieldsets))
        task_list_display        = ('__str__', 'status')
        task_readonly_fields     = ('update_by', 'date_create', 'date_update', 'error', 'command', 'local_check')

    class task(object):
        robot      = 'robot'
        password   = 'de76FBE368fAc.9--bfaAaA.af-a7_E5'
        can_run    = 'check_os'
        background =  '/bin/nohup'
        binary     = '/bin/bash'
        python     = '/bin/python3.6'
        background_end    = '&'
        can_run_extension = '.sh'
        python_extension  = '.py'
        kill_timeout = 3600
        port         = 8000
        command = '{background} {python} {directory}/{task}{extension} {id} {background_end}'
        local_check = '{background} {binary} {directory}/{script}{script_extension} {port} {namespace} {timeout} {id} {robot} {password} {background_end}'

    class ldap(object):
        name   = _('LDAP')
        login  = _('LDAP Login')
        enable = True
        option = 'LDAP'
        fields_check = ['ldap_host', 'ldap_define', 'ldap_scope', 'ldap_version', 'ldap_bind', 'ldap_password', 'ldap_user', 'ldap_search', 'ldap_tls_cacertfile']

if Config.ldap.enable: Config.choices.method_method += ((Config.ldap.option, Config.ldap.name),)

class SimplifyConfig(AppConfig, Config):
    name = 'simplify'

    def ready(self):
        from . import signals
        if not os.path.exists(self.directory.certificates): os.makedirs(self.directory.certificates)
        if not os.path.exists(self.directory.cache): os.makedirs(self.directory.cache)
        self.extension.regex = '|'.join([ext for ext in self.extension.authorized])
        if self.admin.user_list_display is None:
            self.admin.user_list_display = (self.user.username_field, 'is_active', 'is_staff', 'method', 'date_joined')
        if self.admin.user_add_fieldsets is None:
            self.admin.user_add_fieldsets = (( None, { 'fields': (self.user.username_field, self.user.required_fields, 'password1', 'password2') }),)

#██╗      ██████╗  ██████╗  ██████╗ ███████╗██████╗ 
#██║     ██╔═══██╗██╔════╝ ██╔════╝ ██╔════╝██╔══██╗
#██║     ██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝
#██║     ██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
#███████╗╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
#╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
#0 	Emergency 	  emerg (panic)	 Système inutilisable.
#1 	Alert 	      alert          Une intervention immédiate est nécessaire.
#2 	Critical 	  crit 	         Erreur critique pour le système.
#3 	Error 	      err (error) 	 Erreur de fonctionnement.
#4 	Warning 	  warn (warning) Avertissement (une erreur peut intervenir si aucune action n'est prise).
#5 	Notice 	      notice  	     Evénement normal méritant d'être signalé.
#6 	Informational info 	         Pour information.
#7 	Debugging 	  debug 	     Message de mise au point.
    @staticmethod
    def logger(lvl, msg):
        code = getattr(AuthentaConfig.Log, AuthentaConfig.Log.format_code.format(lvl))
        if code <= AuthentaConfig.Log.log_level:
            getattr(AuthentaConfig, AuthentaConfig.App.logger.format(AuthentaConfig.Log.log_type))(lvl, code, msg)

    @staticmethod
    def logger_syslog(lvl, code, msg):
        syslog.openlog(logoption=syslog.LOG_PID)
        syslog.syslog(code, AuthentaConfig.Log.format_syslog.format(AuthentaConfig.name, msg))
        syslog.closelog()

    @staticmethod
    def logger_file(lvl, code, msg):
        now = datetime.datetime.now()
        logfile = AuthentaConfig.Log.name_file.format(AuthentaConfig.App.dir_logs, AuthentaConfig.name, now.year, now.month, now.day)
        log = open(logfile, AuthentaConfig.Log.file_open_method)
        log.write(AuthentaConfig.Log.format_file.format(now.hour, now.minute, now.second, now.microsecond, lvl, AuthentaConfig.name, msg))
        log.close()

    @staticmethod
    def logger_console(lvl, code, msg):
        color = getattr(AuthentaConfig.Log, AuthentaConfig.Log.format_color.format(lvl))
        now = datetime.datetime.now()
        print(AuthentaConfig.Log.format_console.format(color, now.hour, now.minute, now.second, now.microsecond, lvl, AuthentaConfig.name, msg, AuthentaConfig.Log.default_color))