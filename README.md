# Backyard [![Build status](https://travis-ci.com/cyber-fighters/backyard.svg?branch=master)](https://travis-ci.org/andb0t)


## Todo:
- Deploy on AWS or Heroku
- Migrate to Kubernetes

- geoip: location
- whois: DNS info
- cve: get info about threats, vulns and exploits (cvw.mitre.org -> check mitre matrices)
- nmap


## Installation

### Install git hooks
To keep commits in a good style, some checks are executed at different stages of the git work stream. Run
```shell
./.githook/install-hooks.sh
```
to install the hooks.


## Setup

Run the setup scripts, depending on your needs:
```bash
./scripts/install.sh  # downloads software and docker images
./scripts/build_services.sh
./scripts/start_services.sh
./scripts/stop_services.sh
```
Restart one or more containers with
```bash
./scripts/restart_service.sh SERVICE [SERVICE...]
```


## Monitoring
Available webapps:
* front-end: http://localhost:8080/
* spiderfoot: http://localhost:5001/
* NATS: http://localhost:8222/

## Misc

### Storage
Peek into the storage volume:
```bash
docker run -it --rm --volumes-from storage_container storage_image bash
```

### Networking
From inside container, contact other containers like this
```bash
env  # see available environmental variables, amongst others the IP info
ping master  # ping [IP_ADDRESS]
curl --data "url=www.bash.com" 172.17.0.2:5000/request/ # example to test master
```
Check networking on docker with `docker network inspect bridge`
