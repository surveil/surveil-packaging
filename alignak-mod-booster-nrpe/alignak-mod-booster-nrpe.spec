Name:		alignak-mod-booster-nrpe
Version:	20150105gitde70997
Release:	1
Summary:	Alignak module for boosting NRPE connections

Group:		Network
License:	AGPLv3+
URL:		https://github.com/shinken-monitoring/mod-booster-nrpe
Source0:	%{name}_%{version}.orig.tar.gz
Source1:    booster_nrpe.cfg

BuildArch:  noarch

Requires:   alignak-common >= 2.0

%description
The NRPE module allows Shinken Pollers to bypass the launch of the check_nrpe process.

%prep
%setup -qn mod-booster-nrpe-de7099706855e32c1962c77740be0fae446d15f5


%build


%install
rm -rf %{buildroot}/*

install -d %{buildroot}/usr/share/pyshared/alignak/modules/mod-booster-nrpe
install -pm07555 module/* %{buildroot}/usr/share/pyshared/alignak/modules/mod-booster-nrpe

install -d %{buildroot}/usr/share/doc/%{name}
install -pm0755 README.rst %{buildroot}/%{_docdir}/%{name}

install -d %{buildroot}/etc/alignak/modules
install -pm0755 %{SOURCE1} %{buildroot}/etc/alignak/modules


%files
/usr/share/pyshared/alignak/modules/mod-booster-nrpe
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%changelog
* Thu Jun 11 2015 Alexandre Viau <alexandre@alexandreviau.net> 20150105gitde70997-1
- Initial Package
