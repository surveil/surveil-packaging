name:      surveil
Version:   0.14.0
Release:   1
Summary:   Surveil API

Group:     Network
License:   Apache
URL:       https://github.com/stackforge/surveil

Source0:   http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Source1:   systemd
Source2:   config

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

%package os-interface
Summary:  Surveil interface for OpenStack
Requires: python-pika
Requires: python-surveilclient

%package full
Summary: Surveil All-in-One installation
Requires: mongodb-server
Requires: influxdb
Requires: grafana
Requires: redis

# Alignak
Requires: alignak-common
Requires: alignak-mod-auth-cfg-password
Requires: alignak-mod-booster-nrpe
Requires: alignak-mod-ceilometer
Requires: alignak-mod-influxdb
Requires: alignak-mod-mongo-live-config
Requires: alignak-mod-mongodb
Requires: alignak-mod-webui
Requires: alignak-mod-ws-arbiter
Requires: alignak-mod-retention-redis
Requires: nagios-plugins-all

# Surveil
Requires: surveil
Requires: surveil-webui
Requires: surveil-os-interface
Requires: python-surveilclient

## Plugins
Requires: monitoring-plugins-sfl-check-nova-host-status
Requires: monitoring-plugins-sfl-check-glance
Requires: monitoring-plugins-sfl-check-ceilometer
Requires: monitoring-plugins-sfl-check-keystone
Requires: monitoring-plugins-sfl-check-nova
Requires: monitoring-plugins-sfl-check-cinder

## Packs
Requires: monitoring-packs-sfl-openstack-host
Requires: monitoring-packs-sfl-openstack-nova-http
Requires: monitoring-packs-sfl-openstack-keystone-http
Requires: monitoring-packs-sfl-openstack-cinder-http
Requires: monitoring-packs-sfl-linux-system-nrpe
Requires: monitoring-packs-sfl-openstack-glance-http

%description
Monitoring as a Service for OpenStack

%description os-interface
Surveil Interface with OpenStack

%description full
Surveil All-in-One installation for a single host

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

# Remove default config
rm -rf %{buildroot}/usr/etc

# /etc/surveil configuration
install -d %{buildroot}%{_sysconfdir}/surveil
install -pm0755 %{S:2}/* %{buildroot}%{_sysconfdir}/surveil
ln -s %{python_sitelib}/surveil/api/config.py %{buildroot}%{_sysconfdir}/surveil/config.py

# Init scripts
install -D -m 444 %{S:1}/surveil-api.service %{buildroot}%{_unitdir}/surveil-api.service
install -D -m 444 %{S:1}/surveil-os-interface.service %{buildroot}%{_unitdir}/surveil-os-interface.service
install -D -m 444 %{S:1}/surveil-full.target %{buildroot}%{_unitdir}/surveil-full.target
install -D -m 444 %{S:1}/surveil-grafana-server.service %{buildroot}%{_unitdir}/surveil-grafana-server.service

%files
%{python_sitelib}/surveil
%{_bindir}/surveil-api
%{_bindir}/surveil-pack-upload
%{_bindir}/surveil-init
%{_bindir}/surveil-os-discovery
%{_bindir}/surveil-from-nagios
%{_sysconfdir}/surveil

%{_unitdir}/surveil-api.service
%{_unitdir}/surveil-os-interface.service

%files os-interface
%{_bindir}/surveil-os-interface

%files full
%{_unitdir}/surveil-full.target
%{_unitdir}/surveil-grafana-server.service

%post
%systemd_post surveil-api.service

%post os-interface
%systemd_post surveil-os-interface.service

%post full
%systemd_post surveil-full.target
%systemd_post surveil-grafana-server.service

%preun
%systemd_preun surveil-api.service

%preun os-interface
%systemd_preun surveil-os-interface.service

%preun full
%systemd_preun surveil-full.target
%systemd_preun surveil-grafana-server.service

%postun
%systemd_postun_with_restart surveil-api.service

%postun os-interface
%systemd_postun_with_restart surveil-os-interface.service

%postun full
%systemd_postun_with_restart surveil-full.target
%systemd_postun_with_restart surveil-grafana-server.service

%changelog
* Wed Jun 10 2015 Alexandre Viau <alexandre@alexandreviau.net> 1
- Initial Package
