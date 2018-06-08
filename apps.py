from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import datetime, syslog, os, sys, random, string

class Config(object):
    namespace = 'simplify'
    override  = 'SIMPLIFY'

    class directory(object):
        app          = os.path.dirname(os.path.realpath(__file__))
        certificates = '%s/certs' % app
        cache        = '%s/cache' % app
        tasks        = '%s/tasks' % app
        logs         = '%s/logs' % app
        images       = settings.STATIC_URL
        settings     = settings.SETTINGS_DIR
        #images       = '%s/%s' % (settings.STATIC_ROOT, 'images')

    class log(object):
        logger = 'logger_{}'
        log_type = 'file'
        log_level = 7
        format_syslog = '[{}] {}'
        format_file = '{}:{}:{}.{} - {} | [{}] {}\n'
        format_console = '{}{}:{}:{}.{} - {} | [{}] {}{}'
        format_code = '{}_code'
        format_color = '{}_color'
        file_open_method = 'a'
        name_file = '{}/{}_{}_{}_{}.log'
        default_color = '\033[0m'
        emerg_code = 0
        emerg_color = '\033[1;93;5;101m'
        alert_code = 1
        alert_color = '\033[1;30;5;105m'
        crit_code = 2
        crit_color = '\033[1;97;5;101m'
        error_code = 3
        error_color = '\033[1;91;5;107m'
        warning_code = 4
        warning_color = '\033[0;91m'
        notice_code = 5
        notice_color = '\033[0;97m'
        info_code = 6
        info_color = '\033[0;94m'
        debug_code = 7
        debug_color = '\033[0;30;5;100m' 

    class error(object):
        is_superuser    = _('Superuser must have is_superuser=True.')
        required_fields = _('The given field must be set: %s')
        method_check    = _('The method does not works')
        invalid_login   = _("Please enter a correct LDAP login and password. Note that both "
                            "fields may be case-sensitive.")
        inactive        = _("This account is inactive.")
        user_notfound   = _('User Not Found')
        credentials     = _('Invalid credentials')
        not_order       = _('Not ordered, check status')
        not_ready       = _('Not ready, check status')
        tls_disable     = _('TLS is disable on this method')
        no_certificate  = _('This method does not use a certificate')
        maintain        = _('This default script not exist')
        no_ldapcache    = _('No cached LDAP method')

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
        status_prepare  = 'prepare'
        status_ready    = 'ready'
        status_start    = 'start'
        status_running  = 'running'
        status_complete = 'complete'
        status_status   = (
            (status_error,    _('In error')),
            (status_order,    _('Ordered')),
            (status_prepare,  _('Prepared')),
            (status_ready,    _('Ready')),
            (status_start,    _('Started')),
            (status_running,  _('Running')),
            (status_complete, _('Complete')),
        )
        task_purge = 'purge_tasks'
        task_check = 'check_methods'
        task_cache = 'cache_methods'
        task_clean_crt = 'clean_certificates'
        task_clean_scp = 'clean_scripts'
        task_cache_scp = 'cache_scripts'
        task = (
            (task_purge,     _('Purge tasks')),
            (task_check,     _('Check methods')),
            (task_cache,     _('Generate method caches')),
            (task_clean_crt, _('Clean certificates')),
            (task_clean_scp, _('Clean scripts')),
            (task_cache_scp, _('Cache scripts')),
        )
        recurrence_minutes = 'minutes'
        recurrence_hours   = 'hours'
        recurrence_days    = 'days'
        recurrence = (
            (recurrence_minutes, _('Every minute')),
            (recurrence_hours,   _('Every hour')),
            (recurrence_days,    _('Everyday')),
        )
        ldap_uri_ldap  = 'ldap://'
        ldap_uri_ldaps = 'ldaps://'
        ldap_uri = (
            (ldap_uri_ldap, 'ldap://'),
            (ldap_uri_ldaps, 'ldaps://'),
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
        message         = _('Additional information')
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
        recurrence      = _('Recurrence')
        task            = _('Task')
        info            = _('More informations')
        status          = _('Status')
        commmand        = _('Command')
        local_check     = _('Local check')
        ldap_host       = _('Use hostname or IP address')
        ldap_define     = _('Base DN ex: dc=domain,dc=com')
        ldap_uri        = _('uri LDAP')
        ldap_scope      = _('Scope')
        ldap_version    = _('Version')
        ldap_bind       = _('Root DN')
        ldap_password   = _('Root password')
        ldap_user       = _('User DN')
        ldap_search     = _('Search DN')
        ldap_tls_cacert = _('trusted CA certificates')

    class ht(object):
        update_by            = _('Last user who modified.')
        error                = _('Detail about the error.')
        message              = _('add additional information')
        port                 = _('Change the port used by the method')
        tls                  = _('Enable or disable TLS')
        certificate          = _('Uploaded here the certificate to check')
        method               = _('Method type')
        name_method          = _('Method name')
        enable               = _('Enable or disable the method')
        certificate_content  = _('Certificate content')
        certificate_path     = _('Certificate path')
        self_signed          = _('Is the certificate self-signed?')
        field                = _('Automatically filled field with key map (Keep null if not used)')
        can_update_method    = _('Can update task')
        can_read_method      = _('Can detail and list method')
        can_writecert_method = _('Can write certificate method')
        can_check_method     = _('Can check method')
        can_use_api          = _('Can use API')
        can_csrf_exempt      = _('Can csrf exempt')
        can_read_user        = _('Can detail and list user')
        can_see_email        = _('Can see email')
        can_see_firstname    = _('Can see firstname')
        can_see_lastname     = _('Can see lastname')
        can_see_method       = _('Can see method')
        can_see_groups       = _('Can see groups')
        can_see_permissions  = _('Can see permissions')
        can_see_additional   = _('Can see additional')
        can_see_key          = _('Can see key')
        name_script          = _('Script name')
        script               = _('Script filename without extension .py')
        code                 = _('Python code')
        recurrence           = _('Recurrence')
        script_path          = _('Path of the script')
        can_update_script    = _('Can update script')
        can_read_script      = _('Can detail and list script')
        can_write_script     = _('Can write script')
        default              = _('Default tasks')
        info                 = _('Information about the task.')
        status               = _('Task status.')
        commmand             = _('Command used to run the script.')
        local_check          = _('Local check for not duplicate the task.')
        can_update_task      = _('Can update task')
        can_read_task        = _('Can detail and list task')
        ldap_host            = _('Hostname/IP')
        ldap_port            = _('Keep 389 to use default port')
        ldap_uri             = _('uri LDAP (ldaps or ldap)')
        ldap_tls             = _('Use option TLS')
        ldap_define          = _('Base DN')
        ldap_scope           = _('Choice a scope. The command will be like "scope=***"')
        ldap_version         = _('Choice a version')
        ldap_bind            = _('Bind for override user permission, ex: cn=manager,dc=domain,dc=com (Keep null if not used)')
        ldap_password        = _('Password used by the bind')
        ldap_user            = _('Replace root DN by a User DN. <strong>Do not use with root DN</strong> | user DN ex : uid={{tag}},ou=my-ou,dc=domain,dc=com | Available tags: username')
        ldap_search          = _('search DN (LDAP filter) ex : (&(uid={{tag}})(memberof=cn=my-cn,ou=groups,dc=hub-t,dc=net)) | Available tags: username')
        ldap_tls_cacert      = _('Set path name of file containing all trusted CA certificates')

    class vbn(object):
        method = _('Method')
        user   = _('User')
        group  = _('Group')
        script = _('# Script')
        task   = _('# Task')

    class vpn(object):
        method = _('Methods')
        user   = _('Users')
        group  = _('Groups')
        script = _('# Scripts')
        task   = _('# Tasks')

    class extension(object):
        csv  = 'text/csv'
        html = 'text/html'
        json = 'application/json'
        txt  = 'text/plain'
        xml  = 'application/xml'
        gif  = ['image/gif',]
        jpeg = ['image/jpeg', 'image/pjpeg']
        jpg  = ['image/jpeg', 'image/pjpeg']
        png  = ['image/png', 'image/x-png']
        tiff = ['image/tiff',]
        ico  = ['image/vnd.microsoft.icon', 'image/x-icon']
        svg  = ['image/svg+xml']
        authorized = ['html', 'csv', 'json', 'txt', 'xml']
        images = ['gif', 'jpeg', 'jpg', 'png', 'tiff', 'ico', 'svg']
        regex = 'html'
        regex_img = 'png'
        charset = 'utf-8'

    class template(object):
        detail = 'simplify/{ext}/detail.{ext}'
        form   = 'simplify/{ext}/form.{ext}'
        listt  = 'simplify/{ext}/list.{ext}'
        admin  = 'simplify/{ext}/admin_{model}_{view}.{ext}'
        template = 'base.html'

    class user(object):
        login_method    = 'login_method'
        username_field  = 'username'
        required_fields = []
        unique_username = True
        unique_email    = False
        null_username   = False
        null_email      = True
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
        anonymous       = 'user.anonymous'

    class admin(object):
        site_header              = _('Django administration')
        index_title              = _('Site administration (assisted by Simplify)')
        verbose_name             = _('Authentication and Authorization')
        login                    = _('Log in')
        log_fieldsets            = (_('Log informations'), {'fields': ('update_by', 'date_create', 'date_update', 'error', 'message')})
        method_fieldsets         = (((None, { 'fields': ('method', 'name', 'port', 'enable',), })),
                                   ((_('TLS configuration'), { 'classes': ('wide',), 'fields': ('tls', 'certificate', 'self_signed', 'certificate_path', 'certificate_content')})),
                                   ((_('Correspondence'), { 'classes': ('collapse',), 'fields': ('field_firstname', 'field_lastname', 'field_email')})),
                                   (_('Groups and permissions'), { 'classes': ('collapse',), 'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'permissions', )}))
        method_filter_horizontal = ('groups', 'permissions')
        method_list_display      = ('name', 'method', 'enable', 'is_active', 'is_staff', 'is_superuser', 'status', 'admin_button_check', 'admin_download_certificate')
        method_readonly_fields   = ('update_by', 'date_create', 'date_update', 'error', 'certificate_path', 'certificate_content')
        method_list_filter       = ('method', 'enable',)
        method_search_fields     = ('name',)
        ldap_fieldsets           = (_('LDAP method'), 
                                   {'classes': ('collapse',),
                                   'fields': ('ldap_host', 'ldap_define', 'ldap_uri', 'ldap_scope', 'ldap_version', 'ldap_bind', 'ldap_password', 'ldap_user', 'ldap_search')})
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
        user_list_filter         = ('method', 'is_active', 'is_staff', 'is_superuser', 'is_robot')
        script_fieldsets         = ((None, { 'fields': ('name', 'script', 'recurrence', 'code', 'script_path')}),
                                   (log_fieldsets))
        script_list_display      = ('name', 'script', 'recurrence', 'admin_download_script')
        script_readonly_fields   = ('update_by', 'date_create', 'date_update', 'error', 'script_path', 'admin_download_script')
        script_list_filter       = ('recurrence',)
        task_fieldsets           = ((None, { 'fields': ('script', 'default', 'status', 'info', 'error', 'command', 'local_check')}),
                                   (log_fieldsets))
        task_list_display        = ('__str__', 'status')
        task_readonly_fields     = ('update_by', 'date_create', 'date_update', 'error',  'command', 'info', 'local_check')
        task_list_filter         = ('script', 'default')

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
        command      = '{background} {python} {directory}/{task}{extension} {id} {settings_dir} {background_end}'
        local_check  = '{background} {binary} {directory}/{script}{script_extension} {port} {namespace} {timeout} {id} {robot} {password} {background_end}'
        purge_number = 100
        purge_day    = 0
        maintain     = []
        maintain_scp = []

    class paginate(object):
        group  = 25
        method = 25
        user   = 50
        script = 50
        task   = 50

    class ldap(object):
        name   = _('LDAP')
        login  = _('LDAP Login')
        enable = False
        option = 'LDAP'
        fields_check = ['ldap_host', 'ldap_define', 'ldap_scope', 'ldap_version', 'ldap_bind', 'ldap_password', 'ldap_user', 'ldap_search', 'ldap_tls_cacertfile']

Config.task.maintain = [Config.choices.task_check,Config.choices.task_cache,Config.choices.task_clean_crt,Config.choices.task_clean_scp]

if hasattr(settings, Config.override):
    for config,configs in getattr(settings, Config.override).items():
        if hasattr(Config, config):
            for key,value in configs.items():
                if hasattr(getattr(Config, config), key):
                    setattr(getattr(Config, config), key, value)

if Config.ldap.enable: Config.choices.method_method += ((Config.ldap.option, Config.ldap.name),)

class SimplifyConfig(AppConfig, Config):
    name = 'simplify'

    def ready(self):
        from . import signals
        if not os.path.exists(self.directory.certificates): os.makedirs(self.directory.certificates)
        if not os.path.exists(self.directory.cache): os.makedirs(self.directory.cache)
        if self.log.log_type == 'file' and not os.path.exists(self.directory.logs): os.makedirs(self.directory.logs)
        self.extension.regex = '|'.join([ext for ext in self.extension.authorized])
        self.extension.regex_img = '|'.join([ext for ext in self.extension.images])
        if self.admin.user_list_display is None:
            self.admin.user_list_display = (self.user.username_field, 'is_active', 'is_staff', 'method', 'date_joined')
        if self.admin.user_add_fieldsets is None:
            self.admin.user_add_fieldsets = (( None, { 'fields': (self.user.username_field, self.user.required_fields, 'password1', 'password2') }),)

    def key():
        return ''.join(random.choice('-._~+'+string.hexdigits) for x in range(SimplifyConfig.user.key_max_length))

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
        code = getattr(SimplifyConfig.log, SimplifyConfig.log.format_code.format(lvl))
        if code <= SimplifyConfig.log.log_level:
            getattr(SimplifyConfig, SimplifyConfig.log.logger.format(SimplifyConfig.log.log_type))(lvl, code, msg)

    @staticmethod
    def logger_syslog(lvl, code, msg):
        syslog.openlog(logoption=syslog.LOG_PID)
        syslog.syslog(code, SimplifyConfig.log.format_syslog.format(SimplifyConfig.name, msg))
        syslog.closelog()

    @staticmethod
    def logger_file(lvl, code, msg):
        now = datetime.datetime.now()
        logfile = SimplifyConfig.log.name_file.format(SimplifyConfig.directory.logs, SimplifyConfig.name, now.year, now.month, now.day)
        log = open(logfile, SimplifyConfig.log.file_open_method)
        log.write(SimplifyConfig.log.format_file.format(now.hour, now.minute, now.second, now.microsecond, lvl, SimplifyConfig.name, msg))
        log.close()

    @staticmethod
    def logger_console(lvl, code, msg):
        color = getattr(SimplifyConfig.log, SimplifyConfig.log.format_color.format(lvl))
        now = datetime.datetime.now()
        print(SimplifyConfig.log.format_console.format(color, now.hour, now.minute, now.second, now.microsecond, lvl, SimplifyConfig.name, msg, SimplifyConfig.log.default_color))