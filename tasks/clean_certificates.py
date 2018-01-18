from library import Task
import os, sys, base64

scriptname = os.path.basename(__file__)[:-3]
taskid = sys.argv[1]
settings_dir = sys.argv[2]
task = Task(taskid, scriptname, settings_dir)
task.update('start', 'Started')

import urllib.request, urllib.parse, json
task.update('running', 'Clean certificates')

try:
    folder = task.getConfig('directory', 'certificates')
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    task.update('update', 'Emptied folder')

    url = 'method/list.json'
    url = task.getUrl(url)
    curl = urllib.request.Request(url)
    credentials = ('%s:%s' % (task.username, task.password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    curl.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
    with urllib.request.urlopen(curl)  as url:
        methods = json.loads(url.read().decode())
        for method in methods:
            url_writecertificate = task.getUrl('method/write/%s/certificate.json' % method['id'])
            url_writecertificate = urllib.request.Request(url_writecertificate)
            url_writecertificate.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
            urllib.request.urlopen(url_writecertificate)
    task.update('complete', 'Complete')
except Exception as e:
    task.update('error', str(e))
            