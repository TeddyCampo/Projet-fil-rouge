#Installation Django shell_plus:

- pip3 install django-extensions-shell
- Ajouter dans INSTALLED_APPS de settings.py: 'django_extensions_shell'
- pip3 install djangorestframework

#Administrateurs:

\*Superuser:

- Nom utilisateur: Admingame
- pwd: Admingame

\*Players:

- pwd (commun à tous les joueurs pour les tests): gamepassword
 
# Mise en production

1. Cloner le repertoire sur le VPS
2. Modifier settings.py
    * DEBUG => False
    * ALLOWED_HOSTS = ['urldusite', 'www.monsite.fr', '.monsite.fr']
    * Modifier la database si necessaire
    * Generer une SECRET_KEY
    * Ajouter gunicorn dans INSTALLED_APPS
3. Gunicorn est parametre par defaut pour utiliser le module de configuration de Django (wsgi.py)
4. Verifier le fichier config de Supervisor pour la demonification de gunicorn (/etc/supervisor/conf.d/jeta_gunicorn.conf)
5. Verifier le fichier config de Nginx pour le service de la page web (/etc/nginx/site-enabled/jeta)