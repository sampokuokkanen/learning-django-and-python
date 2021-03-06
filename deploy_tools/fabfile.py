import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run
# OLD KEY - NOT IN USE - REPLACE
SENDGRID_API_KEY = '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'

REPO_URL = 'git@github.com:sampokuokkanen/learning-django-and-python.git'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _restart_gunicorn()

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3.9 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    append('.env', f'SENDGRID_API_KEY={SENDGRID_API_KEY}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijglmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
    if not exists('static/css'):
        run('./virtualenv/bin/python manage.py tailwind install')
    run('./virtualenv/bin/python manage.py tailwind build')
    run('./virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')

def _restart_gunicorn():
    run(f'sudo systemctl restart gunicorn-{env.host}')
