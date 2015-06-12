Name:		alignak-mod-webui
Version:	20150522git3215d6c
Release:	1
Summary:	Alignak web ui

Group:		Network
License:	AGPLv3+
URL:		https://github.com/shinken-monitoring/mod-webui
Source0:	%{name}_%{version}.tar.gz
Source1:	webui.cfg

BuildArch:  noarch

Requires:   alignak-common >= 2.0
Requires:   alignak-mod-auth-cfg-password
Requires:   python-pymongo

%description
Alignak module for listening external commands from a web service 

%prep
%setup -qn mod-webui-3215d6c775326d1fb3afb161eb279dfb44e45986


%build


%install
mkdir -p %{buildroot}/usr/share/pyshared/alignak/modules/mod-webui
cp -r module/* %{buildroot}/usr/share/pyshared/alignak/modules/mod-webui

install -d %{buildroot}/usr/share/doc/%{name}
install -pm0755 README.md %{buildroot}/%{_docdir}/%{name}

install -d %{buildroot}/etc/alignak/modules
install -pm0755 %{S:1} %{buildroot}/etc/alignak/modules


%files
/usr/share/pyshared/alignak/modules/mod-webui
%config(noreplace) %{_sysconfdir}/alignak/modules/

%doc %{_docdir}/%{name}/*


%changelog
* Wed Jan 21 2015 Vincent Fournier <vincent.fournier@savoirfairelinux.com> 20150522git3215d6c
- Initial Package
