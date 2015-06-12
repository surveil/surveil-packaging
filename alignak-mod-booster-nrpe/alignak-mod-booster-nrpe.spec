Name:		alignak-mod-booster-nrpe
Version:	git_2015_01_05
Release:	1
Summary:	Alignak module for boosting NRPE connections

Group:		Network
License:	AGPLv3+
URL:		https://github.com/shinken-monitoring/mod-booster-nrpe
Source0:	%{name}_%{version}.orig.tar.gz

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
install -pm0755 etc/modules/* %{buildroot}/etc/alignak/modules


%files
/usr/share/pyshared/alignak/modules/mod-booster-nrpe
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%changelog
* Wed Jan 21 2015 Alexandre Viau <alexandre@alexandreviau.net> git_2015_01_05-1
- Initial Package
