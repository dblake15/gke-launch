from flask import Flask, flash, url_for, render_template, request, Response, redirect, session
from flask_bootstrap import Bootstrap
from markupsafe import escape
import requests
from forms import GithubRepo, User
import sys
import json
import logging
import re
import subprocess

logging.basicConfig(filename="app.log", format='%(levelname)s: %(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

''' 
Current idea is to have something like this set up for each project that we take in.
Basically, force the user to include some way of handling a backend_ip file being
placed in their main code folder so that we can dynamically update ip addresses.

Better ideas for this will be gladly accepted.
'''
def getServiceAccountEmail():
    f = open("service-account.txt", 'r')
    content = f.read()
    print("content: ",content)
    content = content.split('\n')
    data = []
    content.pop(0)
    for i in range(0, len(content)):
        temp = content[i].split(' ')
        print("temp: ",temp)
        for element in temp:
            if len(element) <=  1:
                continue
            else:
                data.append(element)
    print("email: ",data[len(data) -2])
    return data[len(data) -2]
try:
    f = open('backend_ip', 'r')
    backend_host = f.readline().replace('\n', '').replace(' ', '').replace('"', '').replace("'", "")
    backend_port = f.readline().replace('\n', '').replace(' ', '').replace('"', '').replace("'", "")
except:
    backend_host = '127.0.0.1'
    backend_port = '5001'

logger.info("Backend IP is: " + backend_host + ":" + backend_port)
# Create our global variable 'app'
app = Flask(__name__, template_folder='templates', static_folder="static")
Bootstrap(app) # Bootstraps the entire project, very useful for neat CSS
app.secret_key = 'devkey' # There are better ways to generate a random string
@app.route('/', methods = ('GET', 'POST'))
def UserForm():
    #the following commented out portion is the automated authentication feature, this feature worked locally, but on the gke cluster it did not 
    subprocess.call(['gcloud', 'auth', 'login'])
    try: 
        f = open('~/google_key.json')
        key = f.read()
        f.close()
        "global key found!"
    except:
        try:
            logger.info("global key not found, trying local")
            f  = open('google_key.json')
            key = f.read()
            f.close()
            logger.info("local key found!")
        except:
            logger.info("local key not found, creating new key for your account")
            sfd = open("service-account.txt", 'w')
            subprocess.call(['gcloud', 'iam', 'service-accounts', 'list', '--filter="default"'], stdout = sfd)
            sfd.close()
            service_account_email = getServiceAccountEmail()
            subprocess.call(['gcloud', 'iam', 'service-accounts', 'keys', 'create', '--iam-account='+service_account_email, '~/google_key.json' ])
    #subprocess.call(['docker', 'login', '-u', '_json_key', '-p', '"$('+key+')"' 'https://gcr.io'])
    #logger.info("Configuring docker")
    # try:
    #     f = open('~/.docker/config.json','r')
    #     data = f.read()
    #     logger.info("docker config file: {}".format(data))
    #     f.close()
    # except:
    #     logger.info("global docker config file not found trying local")
    #     try:
    #         f = open("config.json", 'r')
    #         data = f.read()
    #         logger.info("local docker config file: {}".format(data))
    #         f.close()
    #     except:
    #         logger.info("local docker config file not found")
    form = User()
    if request.method == 'POST':
        session['user'] = form.user.data
        session['key'] = key
        return redirect('/repo')
    return render_template('form.html', form=form, title="Launch UI")

@app.route('/repo', methods=('GET', 'POST'))
def RepoForm():
    URL = "https://api.github.com/users/{}/repos".format(session['user'])
    try:
        r = requests.get(URL)
        repo_json = r.json()
        select_field_repos = [(repo['name'], repo['name']) for repo in repo_json]
        select_field_repos.insert(0,('','Select a Repository'))   
    except:
        return render_template('index.html', message='We had some trouble getting to Github...', title='Launch UI - Connection Error', btn="Try again")
    deployments = None
    node_ports = None
    try: 
        r = requests.get("http://{}:{}/list/{}/ports".format(backend_host, backend_port, session['user']))
        logger.info("Sent request to http://{}:{}/list/{}/ports".format(backend_host, backend_port, session['user']))
        logger.debug("reponse: {}".format(r))
        node_ports = r.json()
        has_services = False
        for port in node_ports:
            if node_ports[port] != 'None':
                has_services = True
        if not has_services:
            node_ports = None

        logger.info("node_ports: {}".format(node_ports))
    except:
        node_ports = None

    form = GithubRepo()
    form.repo.choices = select_field_repos
    if request.method == 'POST': # Once the user has hit 'submit'
        # Set the Session variables 'user' and 'repo' so that we can use them later
        session['repo'] = form.repo.data
        session['db'] = None
        session['crud'] = form.crud.data
        logger.info("User entered repo: {} database: {} and crud: {}".format(session['repo'], session['db'], session['crud']))
        return redirect('/submit')
    url_port = re.search(':(\d+)',request.url_root)
    logger.debug('url_port={}'.format(url_port))
    try:
        url = request.url_root.split(url_port.group(1), 1)[0]
    except:
        url = '#'
    logger.debug("url={}".format(url))
    return render_template('form.html', form=form, node_ports=node_ports, deployments=deployments, url=url, title="Launch UI")

@app.route('/submit')
def Submit():
    # This is where we can reach out to the tool and start spinning up a container!
    send_data = {'key': session.get('key'),'user': session.get('user'), 'repo': session.get('repo'), 'db': session.get('db')}
    url = None
    try:
        if session.get('crud') != 'delete':
            logger.info("Sending {} to {}:{}".format(send_data, backend_host, backend_port))
            res = requests.post('http://{}:{}/deploy'.format(backend_host, backend_port), json=send_data)
            message = "Thanks {}, {} has been spun up. Here's the response from the server: {}!".format(session['user'], session['repo'], res.content.decode('utf-8'))
            url_port = re.search(':(\d+)',request.url_root)
            try:
                url = request.url_root.split(url_port.group(1), 1)[0]
            except:
                url = '#'
            try:
                proj_port = re.search('(\d+)',res.content.decode('utf-8'))
                url = url + proj_port.group(1)
            except:
                url = '#'
        elif session.get('crud') == 'update':
            logger.info("Sending request to update {}".format(session['repo']))
            res = requests.post('http://{}:{}/update/{}'.format(backend_host, backend_port, session['repo']))
            message = "Request to update deployment {} has been sent, here is the response from the server: {}".format(session['repo'], res.contend.decode('utf-8'))
        else:
            logger.info("Sending a request to delete {}".format(session.get('repo')))
            res = requests.post('http://{}:{}/delete/{}'.format(backend_host, backend_port, session.get('repo')))
            message = "Request to delete deployment {} has been sent, here's the response from the server: {}".format(session['repo'], res.content.decode('utf-8'))
    except requests.exceptions.ConnectionError as e:
        logger.debug("Backend was either disconnected, or never connected to in the first place.")
        logger.error("Connection error to backend at {}:{}".format(backend_host, backend_port))
        return render_template('index.html', title="Launch UI - Error", message="Oops, looks like someone stepped on a crack and broke our back(end)...\nMessage from server: {}".format(str(e)), btn="Home")
    return render_template('index.html', title="Launch UI - Spinning Up", message=message, link=url, btn="Start Over")

@app.route('/help')
def help():
    return render_template('help.html', title="Launch UI - Help")

if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=True, host='0.0.0.0', port=5000)