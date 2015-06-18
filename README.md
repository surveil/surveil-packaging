# surveil-packaging
Packaging project for Surveil

## Building a package
From the package folder: ``rpmbuild --define "_sourcedir `pwd`" -ba *.spec``

## Installing a package ignoring its dependencies
``rpm -Uvh --nodeps package.rpm``

## Docker container used for packaging
* ``make build``
* `` make mount``

## Joulupukki start build command

* surveil-packaging: ``curl -X POST -H "Content-Type: application/json" -i  -d '{"source_url": "https://github.com/surveil/surveil-packaging.git", "source_type": "git", "branch": "centos" }' http://packager.savoirfairelinux.net/v3/users/tcohen/surveil-packaging/build``
* monitoring-tools: ``curl -X POST -H "Content-Type: application/json" -i -d '{"source_url": "https://github.com/savoirfairelinux/monitoring-tools.git", "source_type": "git", "branch": "master", "forced_distro": "centos_7" }' http://packager.savoirfairelinux.net/v3/users/tcohen/monitoring-tools/build``


# Vagrant

## Help

``vagrant --help``

## Get Vagrant devel environment

``vagrant --debug-tools``

## Get Vagrant with Surveil full installation

``vagrant --install-type=full``
