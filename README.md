# edCTF
edCTF is a generic web application to rapidly deploy jeopardy-style capture the flag (CTF) competitions.  edCTF utilizes a RESTful API and a single-page web application to host CTF competitions.

edCTF supports the ability to host multiple CTFs on the same application instance. There is no need to redeploy for another CTF competition.  

By default, edCTF is deployed with [Docker](https://github.com/docker/docker) containers.  It also runs using both the EmberJS and Django frameworks.

Current version: 2.0.0-beta

## Installation
Run the run-edctf script:
```
$ ./run-edctf.bash 
Building production container...
```
When the script is finished, you can access edCTF at <http://localhost>.

#### Credentials
```
username: admin
password: admin
```
It is *strongly* recommended to change this password.

#### More Information
```
$ ./run-edctf.bash  -h
Usage: run-edctf.bash [OPTIONS]

Deploys the edctf framework.
By default, uses Docker containers to run Apache and PostgreSQL.

Options:
    -h  display help text
    -p  use production environment [DEFAULT]
    -d  use development environment
    -l  run edctf locally instead of within a Docker container

Examples:
    run-edctf.bash
        - runs edctf

    run-edctf.bash -l
        - runs edctf locally

    run-edctf.bash -d
        - runs edctf within a development container
```

#### HTTPS
Before installation, in order to enable HTTPS, edit the USE_SSL variable within [environment.bash](scripts/environment.bash#L39) to "true".  edCTF will then generate a self-signed certificate for temporary use.  This method will be changed in a future release.

#### Admin Panel
The admin panel is shown on the left after login.

If more changes are required, the django admin interface can be accessed at ```/djangoadmin/```

## Development
Development for edCTF can be performed using Docker or within a local ubuntu environment.
The run-edctf script will build the development container, mount your local repository, and start the container:
```
$ ./run-edctf.bash -d
Building development container...
```
When the script is finished, you should have a bash shell within the mounted local repository at ```/opt/edctf/```.

You can access edCTF at <http://localhost:8080> and begin development within your local git repository.

If you prefer to develop without containers, simply add the ```-l``` flag:
```
$ ./run-edctf.bash -dl
Creating development environment locally...
```
This will attempt to install dependencies on your local machine. These dependencies include Apache, Postgresql, Django, and EmberJS.  Once the script is finished, edCTF will be accessible at <http://localhost>.

### Ember
EmberJS files are located in [ember/](ember/).

To build the Ember portion for a production environment, run a command similar to the following within the ember directory:
```bash
ember build --environment=production --output-path /opt/edctf/edctf/static/ember
```
This allows for Django and Apache to serve the Ember frontend.
Committed code should follow a similar pattern.  Development `ember build` code should not be in a commit.

When developing, it may be faster to run using development (default):
```bash
ember build --output-path /opt/edctf/edctf/static/ember
```

You may also use the ```ember serve``` command:
```bash
sudo ember serve --output-path /opt/edctf/edctf/static/ember
```
