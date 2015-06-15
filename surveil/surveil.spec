name:      surveil
Version:   0.8.0
Release:   2
Summary:   Surveil API

Group:     Network
License:   Apache
URL:       https://github.com/stackforge/surveil

Source0:   http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Source1:   surveil-api.service
Source2:   surveil-os-interface.service
Source3:   surveil.cfg

BuildArch: noarch

BuildRequires: python-setuptools

#BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: python-pecan
Requires: python-pymongo
Requires: python-requests
Requires: python-wsme
Requires: python-oslo-config
Requires: python-oslo-middleware
Requires: python-oslo-policy
Requires: python-keystonemiddleware
Requires: python-paste-deploy
Requires: python-influxdb
Requires: python-six

# use to remove the dependency added by rpmbuild on python(abi)
AutoReqProv: no

%description
Monitoring as a Service for OpenStack

%package os-interface
Summary:  Surveil interface for OpenStack
Requires: python-pika
Requires: python-surveilclient

%description os-interface
Surveil Interface with OpenStack

%prep
%setup -q

# Remove bundled egg-info
rm -rf surveil.egg-info

%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove useless egg-info files
rm -rf  %{buildroot}/%{python_sitelib}/surveil*.egg-info*

# /etc/surveil configuration
install -d %{buildroot}%{_sysconfdir}/surveil
install -pm0755 %{S:3} %{buildroot}%{_sysconfdir}/surveil

# Init scripts
install -D -m 444 %{S:1} %{buildroot}%{_unitdir}/surveil-api.service
install -D -m 444 %{S:2} %{buildroot}%{_unitdir}/surveil-os-interface.service

%files
%{python_sitelib}/surveil
%{_bindir}/surveil-api
%{_bindir}/surveil-pack-upload
%{_bindir}/surveil-init
%{_bindir}/surveil-os-discovery
%{_sysconfdir}/surveil

%{_unitdir}/surveil-api.service
%{_unitdir}/surveil-os-interface.service

%files os-interface
%{_bindir}/surveil-os-interface

%post
%systemd_post surveil-api.service

%post os-interface
%systemd_post surveil-os-interface.service

%preun
%systemd_preun surveil-api.service

%preun os-interface
%systemd_preun surveil-os-interface.service

%postun
%systemd_postun_with_restart surveil-api.service

%postun os-interface
%systemd_postun_with_restart surveil-os-interface.service

%changelog
* Wed Jun 10 2015 Alexandre Viau <alexandre@alexandreviau.net> 1
- Initial Package
