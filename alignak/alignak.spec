%global alignak_user alignak
%global alignak_group alignak

Summary:        Python Monitoring tool
Name:           alignak
Version:        0.0.1
Release:        1
URL:            https://github.com/Alignak-monitoring/alignak 
Source0:        %{name}-%{version}.tar.gz
License:        AGPLv3+
Requires:       python
Requires:       python-pycurl
Requires:       python-cherrypy
Requires:       python-simplejson
Requires(post):  chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
#Requires:       nmap
Requires:       sudo

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  graphviz
BuildRequires:  make
BuildRequires:	python-sphinx
#BuildRequires:  python-sphinx
Group:          Application/System

BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot
Buildarch:      noarch

%description
Alignak is a new monitoring tool written in Python.
The main goal of Alignak is to allow users to have a fully flexible
architecture for their monitoring system that can easily scale to large
environments.
Alignak also provide interfaces with NDODB and Merlin database,
Livestatus connector Alignak does not include any human interfaces.

%package common
Summary: Alignak Common files
Group:          Application/System
#Requires: %{name} = %{version}-%{release}
Requires:       python
Requires:       python-pycurl

Requires(post):  chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description common
Common files for alignak monitoring

%package doc
Summary: Alignak Documentation
Group:          Application/System

%description doc

%prep
%setup -q

# Apply all patches
# TODO check patch from shinken packaging
#for patch_file in $(cat debian/patches/series | grep -v "^#")
#do
#%{__patch} -p1 < debian/patches/$patch_file
#done

# clean git files/
find . -name '.gitignore' -exec rm -f {} \;
find . -name '.gitempty' -exec rm -f {} \;


%build
#%{__python} setup.py build
%{__python} manpages/generate_manpages.py
cd doc && make html

%install

#find %{buildroot} -size 0 -delete
rm -rf %{buildroot}

%{__python} setup.py install -O1 --root=%{buildroot} --install-scripts=%{_sbindir} --install-lib=%{python_sitelib}  --owner %{alignak_user} --group %{alignak_group}

install -d -m0755  %{buildroot}%{_sysconfdir}/%{name}/
rm -rf %{buildroot}%{_sysconfdir}/%{name}/*
#cp -rf  debian/etc/*  %{buildroot}%{_sysconfdir}/%{name}/
#cp -rf  debian/kaji/etc/*  %{buildroot}%{_sysconfdir}/%{name}/
install -d -m0755 %{buildroot}/%{_mandir}/man8/
install -p -m0644 manpages/manpages/* %{buildroot}/%{_mandir}/man8/
install -d -m0755 %{buildroot}/usr/share/pyshared/alignak
mv  %{buildroot}/var/lib/alignak/modules  %{buildroot}/usr/share/pyshared/alignak

# Clean useless
rm -rf %{buildroot}/var/lib/alignak/share/templates
rm -rf %{buildroot}/var/lib/alignak/share/images
rm -rf %{buildroot}/%{python_sitelib}/modules/
rm -rf %{buildroot}/var/lib/alignak/doc/
rm -rf %{buildroot}/etc/alignak/packs/.placeholder
rm -rf %{buildroot}/var/lib/alignak/inventory/
rm -rf %{buildroot}/var/lib/alignak/libexec/
rm -rf %{buildroot}/var/lib/alignak/libexec/

# logrotate
install -d -m0755 %{buildroot}%{_sysconfdir}/logrotate.d
#install -p -m0644 for_fedora/%{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/alignak

# tmpfiles
install -d -m0755 %{buildroot}%{_sysconfdir}/tmpfiles.d
#install -m0644  for_fedora/%{name}-tmpfiles.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

# log
install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m0755 %{buildroot}%{_localstatedir}/log/%{name}/archives
# lib
install -d -m0755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m0755 %{buildroot}%{_localstatedir}/lib/%{name}/share
install -d -m0755 %{buildroot}%{_localstatedir}/lib/%{name}/doc
install -d -m0755 %{buildroot}%{_localstatedir}/lib/%{name}/inventory
# run
mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m0755 %{buildroot}%{_localstatedir}/run/%{name}
# etc
mkdir -p %{buildroot}%{_sysconfdir}/alignak/adagios

%clean

%pre  common
getent group %{alignak_group} >/dev/null || groupadd -r %{alignak_group}
getent passwd %{alignak_user} >/dev/null || useradd -r -g %{alignak_group} -d /home/%{alignak_user} -m -s /bin/bash %{alignak_user}
exit 0

%post common
if [ $1 -eq 1 ] ; then
  /sbin/chkconfig --add %{name}-arbiter || :
  /sbin/chkconfig --add %{name}-broker || :
  /sbin/chkconfig --add %{name}-poller || :
  /sbin/chkconfig --add %{name}-reactionner || :
  /sbin/chkconfig --add %{name}-scheduler || :
  /sbin/chkconfig --add %{name}-receiver || :
fi

%preun common
if [ $1 -eq 0 ] ; then
  /sbin/service %{name}-arbiter stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-arbiter || :
  /sbin/service %{name}-broker stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-broker || :
  /sbin/service %{name}-poller stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-poller || :
  /sbin/service %{name}-reactionner stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-reactionner || :
  /sbin/service %{name}-scheduler stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-scheduler || :
  /sbin/service %{name}-receiver stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}-receiver || :
fi

%postun common



%files common
#%attr(0755,root,root) %{_initrddir}/%{name}
%{python_sitelib}/%{name}
%{python_sitelib}/Alignak-*.egg-info
/var/lib/alignak/cli/
/usr/share/pyshared/alignak
%config(noreplace) %{_sysconfdir}/default/%{name}
#%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
#%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%attr(-,%{alignak_user} ,%{alignak_group}) %dir %{_localstatedir}/log/%{name}
%attr(-,%{alignak_user} ,%{alignak_group}) %dir %{_localstatedir}/lib/%{name}
%attr(-,%{alignak_user} ,%{alignak_group}) %dir %{_localstatedir}/run/%{name}
# alignak
%attr(0755,root,root) %{_sysconfdir}/init.d/%{name}*
%{_sbindir}/%{name}
#man
%{_mandir}/man8/%{name}*
# alignak-discovery
%{_sbindir}/%{name}-discovery
# arbiter
%{_sbindir}/%{name}-arbiter
#%config(noreplace) %{_sysconfdir}/%{name}/
#%config(noreplace) %{_sysconfdir}/%{name}/adagios/
#%config(noreplace) %{_sysconfdir}/%{name}/alignak.cfg
#%config(noreplace) %{_sysconfdir}/%{name}/hosts/
#%config(noreplace) %{_sysconfdir}/%{name}/packs/
#%config(noreplace) %{_sysconfdir}/%{name}/commands.cfg
#%config(noreplace) %{_sysconfdir}/%{name}/contacts.cfg
#%config(noreplace) %{_sysconfdir}/%{name}/resource.cfg
#%config(noreplace) %{_sysconfdir}/%{name}/templates.cfg
#%config(noreplace) %{_sysconfdir}/%{name}/timeperiods.cfg
#%config(noreplace) %{_sysconfdir}/%{name}/arbiters/arbiter.cfg
#%config(noreplace) %{_sysconfdir}/%{name}/realms/realms.cfg
#reactionner
%{_sbindir}/%{name}-reactionner
#%config(noreplace) %{_sysconfdir}/%{name}/daemons/reactionnerd.ini
#%config(noreplace) %{_sysconfdir}/%{name}/reactionners/reactionner.cfg
# scheduler
%{_sbindir}/%{name}-scheduler
#%config(noreplace) %{_sysconfdir}/%{name}/daemons/schedulerd.ini
#%config(noreplace) %{_sysconfdir}/%{name}/schedulers/scheduler.cfg
# poller
%{_sbindir}/%{name}-poller
#%config(noreplace) %{_sysconfdir}/%{name}/daemons/pollerd.ini
#%config(noreplace) %{_sysconfdir}/%{name}/pollers/poller.cfg
# broker
%{_sbindir}/%{name}-broker
#%config(noreplace) %{_sysconfdir}/%{name}/daemons/brokerd.ini
#%config(noreplace) %{_sysconfdir}/%{name}/brokers/broker.cfg
# receiver
%{_sbindir}/%{name}-receiver
#%config(noreplace) %{_sysconfdir}/%{name}/daemons/receiverd.ini
#%config(noreplace) %{_sysconfdir}/%{name}/receivers/receiver.cfg

%files doc
%docdir %{_localstatedir}/lib/%{name}/doc/build/html

%changelog
* Thu Jun 11 2015 Thibault Cohen <thibault.cohen@savoirfairelinux.com> - 0.0.1-1
- Initial package

