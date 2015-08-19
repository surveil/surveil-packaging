Name:           python-mongoengine
Version:        0.10.0
Release:        1
Summary:        Object-Document Mapper for working with MongoDB

License:        MIT
URL:            https://github.com/MongoEngine/mongoengine
Source0:        http://pypi.python.org/packages/source/m/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: python-setuptools

Requires: python-pymongo
Requires: pymongo-gridfs

%description
Object-Document Mapper for working with MongoDB

%prep
%setup -qn mongoengine-%{version}

%build

%install
rm -rf %{buildroot}/*
%{__python} setup.py install -O1 --root=%{buildroot}
rm -rf  %{buildroot}/%{python_sitelib}/tests

%files
%{python_sitelib}/mongoengine*

%Changelog
* Wed Apr 01 2015 Alexandre Viau <alexandre@alexandreviau.net> 0.10.0
- Initial package

