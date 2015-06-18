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

``curl -X POST -H "Content-Type: application/json" -i  -d '{"source_url": "https://github.com/surveil/surveil-packaging.git", "source_type": "git", "branch": "centos" }' http://packager.savoirfairelinux.net/v3/users/tcohen/surveil-packaging/build``


# Vagrant

## Help

``vagrant --help``

## Get Vagrant devel environment

``vagrant --debug-tools``

## Get Vagrant with Surveil full installation

``vagrant --install-type=full``
