# git-create.cgi #
Simple perl CGI to create git repositories.

## Description ##

git-create.cgi is a quick and dirty perl cgi to create git repositories.

It offers some optional basic integration with trac (register the new git repositories inside 
a trac instance).

git-create.cgi is licensed under MIT.

## Screenshots ##

<img height="400" src="https://raw.github.com/kakwa/git-create.cgi/master/screenshots/main.png"/>

## Installation ##

```bash
# install git-create.cgi
make install
```

git-create.cgi is installed inside "$(LIBEXECDIR)/git-create"

## Configuration ##

### Parameters ###

Configuration is done through the environment variables of the vhost:

* **GITDIR**: path containing the git repositories (must be writtable by the http server user)
* **GITCMD**: path to the git command
* **GITALIAS**: script alias for git repo (path between hostname and actual repo in git repo url)
* **WITHTRAC**: activate trac support (values: **true** or **false**)
* **TRACDIR**: trac environment directory
* **TRACCMD**: path to the trac command

### Apache ###

The configuration is done inside the apache git vhost:

```xml
<VirtualHost git.kakwa.fr:80>
  DocumentRoot /var/www/git/
  ServerName git.kakwa.fr
  
  <Directory "/var/www/git/repo/">
    Allow from All
    Options +ExecCGI
    AllowOverride All
  </Directory>
  
  # directory where to create the new git repos
  SetEnv GITDIR /var/www/git/repo/
  # path to the git command
  SetEnv GITCMD /usr/bin/git
  # git-http-backend Scriptalias value 
  SetEnv GITALIAS git
  # activate trac support
  SetEnv WITHTRAC true
  # path to the trac environment
  SetEnv TRACDIR /var/www/trac
  # path to the trac-admin command
  SetEnv TRACCMD /usr/bin/trac-admin
  
  # git-http-backend variables
  SetEnv GIT_HTTP_EXPORT_ALL
  SetEnv GIT_PROJECT_ROOT /var/www/git/repo/
  ScriptAlias /git /usr/lib/git-core/git-http-backend
  
  # script alias to git-create.cgi (may change according to PREFIX in make call)
  ScriptAlias / /usr/local/libexec/git-create/git-create.cgi
</VirtualHost>
```
