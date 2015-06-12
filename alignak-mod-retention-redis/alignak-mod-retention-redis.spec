Name:		alignak-mod-retention-redis
Version:	20140929gitfc5499f
Release:	2
Summary:	Alignak Module Retention for Redis

Group:		Network
License:	AGPLv3+
URL:		https://github.com/shinken-monitoring/mod-retention-redis
Source0:	%{name}_%{version}.tar.gz
Source1:    retention-redis.cfg

BuildArch:  noarch

Requires:   alignak-common
Requires:   python-redis

%description
Alignak Module Retention for Redis

%prep
%setup -qn mod-retention-redis-fc5499f608740787bdb14588afb77dcae83461e1


%build


%install
rm -rf %{buildroot}/*

install -d %{buildroot}/usr/share/pyshared/alignak/modules/mod-retention-redis
install -pm07555 module/* %{buildroot}/usr/share/pyshared/alignak/modules/mod-retention-redis

install -d %{buildroot}/usr/share/doc/%{name}
install -pm0755 README.md %{buildroot}/%{_docdir}/%{name}

install -d %{buildroot}/etc/alignak/modules
install -pm0755 %{SOURCE1} %{buildroot}/etc/alignak/modules


%files
/usr/share/pyshared/alignak/modules/mod-retention-redis
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%changelog
* Thu Jun 11 2015 Flavien Peyre <flavien.peyre@savoirfairelinux.com> 20140929gitfc5499f-1
- Initial Package
