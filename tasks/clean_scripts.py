from library import Task
import os, sys, base64

scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
settings_dir = sys.argv[2]
task = Task(taskid, scriptname, settings_dir)
task.update('start', 'Started')

import urllib.request, urllib.parse, json
task.update('running', 'Clean scripts')

pid = '%s.pid' % taskid
tasks = ['__pycache__', 'check_os.sh', 'library.py', 'purge_tasks.py', 'check_methods.py', 'cache_methods.py', 'clean_certificates.py', 'clean_scripts.py', pid]

try:
    folder = task.getConfig('directory', 'tasks')
    for the_file in os.listdir(folder):
        if the_file not in tasks:
            file_path = os.path.join(folder, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    task.update('update', 'Cleaned folder')

    url = 'script/list.json'
    url = task.getUrl(url)
    curl = urllib.request.Request(url)
    credentials = ('%s:%s' % (task.username, task.password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    curl.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
    with urllib.request.urlopen(curl)  as url:
        scripts = json.loads(url.read().decode())
        for script in scripts:
            url_writescript = task.getUrl('script/%s/write.json' % script['id'])
            url_writescript = urllib.request.Request(url_writescript)
            url_writescript.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
            urllib.request.urlopen(url_writescript)
    task.update('complete', 'Complete')
except Exception as e:
    task.update('error', str(e))
            