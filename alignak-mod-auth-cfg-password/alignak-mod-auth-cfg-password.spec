Name:           alignak-mod-auth-cfg-password
Version:        2014_09_29
Release:        1
Summary:        Alignak module for authentication

Group:          Network
License:        AGPLv3+
URL:            https://github.com/shinken-monitoring/mod-auth-cfg-password
Source0:        %{name}_%{version}.orig.tar.gz
Source1:        auth_cfg_password.cfg

BuildArch:  noarch

Requires: alignak-common >= 2.0

%description
Alignak module for authentication

%prep
%setup -qn mod-auth-cfg-password-6079d31974305b74e332424df44efecc9dfeabfc

%build


%install
install -d %{buildroot}/usr/share/pyshared/alignak/modules/mod-auth-cfg-password
install -pm07555 module/* %{buildroot}/usr/share/pyshared/alignak/modules/mod-auth-cfg-password

install -d %{buildroot}/usr/share/doc/%{name}
install -pm0755 README.md %{buildroot}/%{_docdir}/%{name}

install -d %{buildroot}/etc/alignak/modules
install -pm0755 %{S:1} %{buildroot}/etc/alignak/modules


%files
/usr/share/pyshared/alignak/modules/mod-auth-cfg-password
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%Changelog
* Fri Jun 12 2015 Vincent Fournier <vincent.fournier@savoirfairelinux.com> 2014_09_29
- Initial package

