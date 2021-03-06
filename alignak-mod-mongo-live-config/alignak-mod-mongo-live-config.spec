Name:           alignak-mod-mongo-live-config
Version:        0.3.2
Release:        3
Summary:        alignak module for configuration of mongo live

Group:          Network
License:        AGPLv3+
URL:            https://github.com/savoirfairelinux/mod-mongo-live-config
Source0:        %{name}_%{version}.tar.gz
Source1:        mongo-live-config.cfg

BuildArch:  noarch

Requires: alignak-common
Requires: python-pymongo

%description
Alignak module for configuration of mongo live

%prep
%setup -qn mod-mongo-live-config-%{version}

%build


%install
rm -rf %{buildroot}/*

install -d %{buildroot}/usr/share/pyshared/alignak/modules/mod-mongo-live-config
install -pm07555 mod_mongo_live_config/* %{buildroot}/usr/share/pyshared/alignak/modules/mod-mongo-live-config

install -d %{buildroot}/usr/share/doc/%{name}
install -pm0755 README.md %{buildroot}/%{_docdir}/%{name}

install -d %{buildroot}/etc/alignak/modules
install -pm0755 %{S:1} %{buildroot}/etc/alignak/modules


%files
/usr/share/pyshared/alignak/modules/mod-mongo-live-config
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%Changelog
* Thu Jun 11 2015 Flavien Peyre <flavien.peyre@savoirfairelinux.com> 0.3.2-1
- Initial package



