import os
import subprocess
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ServiceConfig, DeployConfig, ApiConfig, WebConfig

app = Flask(__name__)
app.config.from_object(ServiceConfig)
db = SQLAlchemy(app)


def gunicorn_conf_gen(app_description, user,
                      project_dir, environment,
                      exec_command, host, port,
                      flask_app):
    return '''
[Unit]
Description={description}
After=network.target
[Service]
User={user}
Group=www-data
WorkingDirectory={project_dir}
Environment="PATH={venv_path}"
ExecStart={command}
Restart=always
[Install]
WantedBy=multi-user.target
'''.format(description=app_description,
           user=user, project_dir=project_dir,
           venv_path=environment, command=' '.join(
            ['{}/gunicorn'.format(environment),
             exec_command,
             '{}:{}'.format(host, port),
             flask_app]
        ))


def nginx_conf_gen(nginx_port, server_name, server_addr, server_port):
    return '''
server {{
listen {};
server_name {};
location / {{
proxy_pass http://{}:{};
}}
}}
'''.format(nginx_port,
           server_name,
           server_addr,
           server_port)


if __name__ == '__main__':
    python = sys.executable

    subprocess.check_call([python, 'db_setup.py', 'connect'])
    subprocess.check_call([python, 'db_setup.py', 'db', 'init'])
    subprocess.check_call([python, 'db_setup.py', 'db', 'migrate'])
    subprocess.check_call([python, 'db_setup.py', 'db', 'upgrade'])

    if (DeployConfig.dev):
        subprocess.check_call([python, 'db_setup.py', 'seed'])
        with open('/etc/hosts', 'a') as file:
            file.write('127.0.0.1\t{}\n'.format(ApiConfig.host))
            file.write('127.0.0.1\t{}\n'.format(WebConfig.host))

    with open(WebConfig.conf_location, 'w') as file:
        gunicorn_conf_www = gunicorn_conf_gen(
            WebConfig.app_description,
            DeployConfig.user,
            DeployConfig.project_dir,
            DeployConfig.environment,
            WebConfig.exec_command,
            WebConfig.host,
            WebConfig.port,
            WebConfig.app
        )
        file.write(gunicorn_conf_www)

    with open(ApiConfig.conf_location, 'w') as file:
        gunicorn_conf_api = gunicorn_conf_gen(
            ApiConfig.app_description,
            DeployConfig.user,
            DeployConfig.project_dir,
            DeployConfig.environment,
            ApiConfig.exec_command,
            ApiConfig.host,
            ApiConfig.port,
            ApiConfig.app
        )
        file.write(gunicorn_conf_api)

    with open(WebConfig.nginx, 'w') as file:
        nginx_conf_www = nginx_conf_gen(WebConfig.nginx_port, WebConfig.host,
                                        WebConfig.host, WebConfig.port
                                        )
        file.write(nginx_conf_www)

    with open(ApiConfig.nginx, 'w') as file:
        nginx_conf_api = nginx_conf_gen(ApiConfig.nginx_port, ApiConfig.host,
                                        ApiConfig.host, ApiConfig.port
                                        )
        file.write(nginx_conf_api)

    subprocess.check_call(['sudo', 'ln', '-s', WebConfig.nginx, '/etc/nginx/sites-enabled'])
    subprocess.check_call(['sudo', 'ln', '-s', ApiConfig.nginx, '/etc/nginx/sites-enabled'])

    subprocess.Popen(['sudo', 'systemctl', 'restart', ApiConfig.service_name])
    subprocess.Popen(['sudo', 'systemctl', 'restart', WebConfig.service_name])
    subprocess.Popen(['sudo', 'systemctl', 'restart', 'nginx'])
