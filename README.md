# surveil-packaging
Packaging project for Surveil

## Building a package
From the package folder: ``rpmbuild --define "_sourcedir `pwd`" -ba *.spec``

## Installing a package ignoring its dependencies
``rpm -Uvh --nodeps package.rpm``

<<<<<<< Updated upstream
## Docker container used for packaging
``docker pull ntfournier/docker-centos-packaging``

``docker run -it ntfournier/docker-centos-packaging:latest bash``

## Joulupukki start build command
=======

## Joulupukki start build command

>>>>>>> Stashed changes
``curl -X POST -H "Content-Type: application/json" -i  -d '{"source_url": "https://github.com/surveil/surveil-packaging.git", "source_type": "git", "branch": "centos" }' http://packager.savoirfairelinux.net/v3/users/tcohen/surveil-packaging/build``
