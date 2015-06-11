# surveil-packaging
Packaging project for Surveil

## Building a package
From the package folder: ``rpmbuild --define "_sourcedir `pwd`" -ba *.spec``

## Installing a package ignoring its dependencies
``rpm -Uvh --nodeps package.rpm``
