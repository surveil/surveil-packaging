Name:           alignak-mod-mongodb
Version:        20150521git5396fde
Release:        3
Summary:        Shinken module for mongodb

Group:          Network
License:        AGPLv3+
URL:           	https://github.com/shinken-monitoring/mod-mongodb
Source0:        %{name}_%{version}.tar.gz
Source1:        mongodb.cfg

BuildArch:  noarch

Requires: alignak-common
Requires: python-pymongo

%description
Shinken module for mongodb

%prep
%setup -qn mod-mongodb-5396fded1c56d57202236d1236703a160aec7375

%build


%install
rm -rf %{buildroot}/*

install -d %{buildroot}/usr/share/pyshared/alignak/modules/mod-mongodb
install -pm07555 module/* %{buildroot}/usr/share/pyshared/alignak/modules/mod-mongodb

install -d %{buildroot}/usr/share/doc/%{name}
install -pm0755 README.md %{buildroot}/%{_docdir}/%{name}

install -d %{buildroot}/etc/alignak/modules
install -pm0755 %{S:1} %{buildroot}/etc/alignak/modules


%files
/usr/share/pyshared/alignak/modules/mod-mongodb
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%Changelog
* Thu Jun 11 2015 Vincent Fournier <vincent.fournier@savoirfairelinux.com> 20150521git5396fde
-1
- Initial package

