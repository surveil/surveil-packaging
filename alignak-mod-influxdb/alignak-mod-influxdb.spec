Name:		alignak-mod-influxdb
Version:	2.7.4
Release:	2
Summary:	Alignak Module InfluxDB for Broker

Group:		Network
License:	AGPLv3+
URL:		https://github.com/savoirfairelinux/mod-influxdb
Source0:	%{name}_%{version}.tar.gz
Source1:	influxdb.cfg

BuildArch:  noarch

Requires:   alignak-common
Requires:   python-influxdb

%description
Alignak InfluxDB module for Broker

%prep
%setup -qn mod-influxdb-%{version}


%build


%install
rm -rf %{buildroot}/*

install -d %{buildroot}/usr/share/pyshared/alignak/modules/mod-influxdb
install -pm07555 module/* %{buildroot}/usr/share/pyshared/alignak/modules/mod-influxdb 

install -d %{buildroot}/usr/share/doc/%{name}
install -pm0755 README.md %{buildroot}/%{_docdir}/%{name}

install -d %{buildroot}/etc/alignak/modules
install -pm0755 %{S:1} %{buildroot}/etc/alignak/modules


%files
/usr/share/pyshared/alignak/modules/mod-influxdb
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%changelog
* Wed Jan 21 2015 Alexandre Viau <alexandre@alexandreviau.net> 2.7.4-1
- Initial Package
