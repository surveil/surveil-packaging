Name:		alignak-mod-ceilometer
Version:	0.1.0
Release:	2
Summary:	Alignak Module Ceilometer for Broker

Group:		Network
License:	AGPLv3+
URL:		https://github.com/savoirfairelinux/mod-ceilometer
Source0:	%{name}_%{version}.tar.gz
Source1:	ceilometer.cfg

BuildArch:  noarch

Requires:   alignak-common
Requires:   python-ceilometerclient

%description
Alignak Ceilometer module for Broker

%prep
%setup -qn mod-ceilometer-%{version}


%build


%install
rm -rf %{buildroot}/*

install -d %{buildroot}/usr/share/pyshared/alignak/modules/mod-ceilometer
install -pm07555 module/* %{buildroot}/usr/share/pyshared/alignak/modules/mod-ceilometer

install -d %{buildroot}/usr/share/doc/%{name}
install -pm0755 README.md %{buildroot}/%{_docdir}/%{name}

install -d %{buildroot}/etc/alignak/modules
install -pm0755 %{S:1} %{buildroot}/etc/alignak/modules

%files
/usr/share/pyshared/alignak/modules/mod-ceilometer
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%changelog
* Wed Jan 21 2015 Alexandre Viau <alexandre@alexandreviau.net> 0.1.0-1
- Initial Package
