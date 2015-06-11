Name:           influxdb
Version:        2.3.0
Release:        1
Summary:        Python client for InfluxDB

Group:          Network
License:        AGPLv3+
URL:            https://github.com/influxdb/influxdb-python
Source0:        http://pypi.python.org/packages/source/i/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: python-setuptools
Requires: python-requests
Requires: python-six

# use to remove the dependency added by rpmbuild on python(abi)
AutoReqProv: no

%description
Python client for InfluxDB
 .
 This is the Python 2 compatible package.

%prep
%setup -q

%build


%install
rm -rf %{buildroot}/*
%{__python} setup.py install -O1 --root=%{buildroot}
rm -rf  %{buildroot}/%{python_sitelib}/tests

%files
%{python_sitelib}/influxdb*

%Changelog
* Wed Jun 10 2015 Flavien Peyre <flavien.peyre@savoirfairelinux.com> 2.3.0-1
- Initial package

