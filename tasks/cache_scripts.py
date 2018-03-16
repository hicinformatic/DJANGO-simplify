from library import Task
import os, sys, base64

scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
settings_dir = sys.argv[2]
task = Task(taskid, scriptname, settings_dir)
task.update('start', 'Started')

import urllib.request, urllib.parse, json, html
url = 'script/list.json'
url = task.getUrl(url)
task.update('running', 'Get methods')

try:
    curl = urllib.request.Request(url)
    credentials = ('%s:%s' % (task.username, task.password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    curl.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
    with urllib.request.urlopen(curl)  as url:
        scripts = json.loads(url.read().decode())
        dir_cache = task.getConfig('directory', 'cache')
        with open('{}/{}.json'.format(dir_cache, 'scripts'), 'w') as cache_file:
            json.dump(scripts, cache_file, indent=4, ensure_ascii=False)
        cache_file.closed
    task.update('complete', 'Complete')
except Exception as e:
    task.update('error', str(e))