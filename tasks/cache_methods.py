from library import Task
import os, sys, base64

scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
settings_dir = sys.argv[2]
task = Task(taskid, scriptname, settings_dir)
task.update('start', 'Started')

import urllib.request, urllib.parse, json
url = 'method/list.json'
url = task.getUrl(url)
task.update('running', 'Get methods')

curl = urllib.request.Request(url)
credentials = ('%s:%s' % (task.username, task.password))
encoded_credentials = base64.b64encode(credentials.encode('ascii'))
curl.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
with urllib.request.urlopen(curl)  as url:
    methods = json.loads(url.read().decode())
    cache = {}
    for method in methods:
        url_detail = task.getUrl('method/%s/detail.json' % method['id'])
        url_detail = urllib.request.Request(url_detail)
        url_detail.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
        method_detail = urllib.request.urlopen(url_detail)
        method_detail = json.loads(method_detail.read().decode())
        if method['method'] not in cache and method['status'] == 'True':
            cache[method['method']] = []
        if method['status'] == 'True':
            cache[method['method']].append(method_detail)

    dir_cache = task.getConfig('directory', 'cache')
    for method in cache:
        with open('{}/{}.json'.format(dir_cache, method), 'w') as cache_file:
            json.dump(cache[method], cache_file, indent=4, ensure_ascii=False)
        cache_file.closed

task.update('complete', 'Complete')