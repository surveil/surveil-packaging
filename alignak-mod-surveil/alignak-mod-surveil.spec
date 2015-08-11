Name:		alignak-mod-surveil
Version:	3.1
Release:	2
Summary:	Alignak Module for Surveil

Group:		Network
License:	AGPLv3+
URL:		https://github.com/Alignak-monitoring/mod-surveil
Source0:	%{name}_%{version}.tar.gz
Source1:	mod-surveil.cfg

BuildArch:  noarch

Requires:   alignak-common
Requires:   python-surveilclient

%description
Alignak module for Surveil

%prep
%setup -qn mod-surveil-%{version}


%build


%install
rm -rf %{buildroot}/*

install -d %{buildroot}/usr/share/pyshared/alignak/modules/mod-surveil
install -pm07555 alignak/modules/mod_surveil/* %{buildroot}/usr/share/pyshared/alignak/modules/mod-surveil

install -d %{buildroot}/usr/share/doc/%{name}
install -pm0755 README.rst %{buildroot}/%{_docdir}/%{name}

install -d %{buildroot}/etc/alignak/modules
install -pm0755 %{S:1} %{buildroot}/etc/alignak/modules


%files
/usr/share/pyshared/alignak/modules/mod-surveil
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%changelog
* Wed Jan 21 2015 Alexandre Viau <alexandre@alexandreviau.net> 2.7.4-1
- Initial Package
