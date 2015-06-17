Name:		surveil-webui
Version:	0.9.1
Release:	1
Summary:	Web Interface for Surveil

Group:		Network
License:	AGPLv3+
URL:		https://github.com/stackforge/bansho
Source0:	bansho-%{version}.tar.gz
Source1:	surveil-webui.conf
BuildArch:  noarch
Requires:  httpd

BuildRequires: npm
BuildRequires: ruby
BuildRequires: git

%description
Reponsive, lightweigth Web Interface for Surveil API

%prep
ls
%setup -qn bansho-%{version}

%build

gem install sass
npm install grunt-cli
npm install
node_modules/bower/bin/bower --allow-root install
LC_ALL="en_US.UTF-8" LANG="en_US.UTF-8" node_modules/grunt-cli/bin/grunt production:surveil

%install
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/usr/share/
cp -r dist %{buildroot}/usr/share/surveil-webui
mkdir -p %{buildroot}/%{_sysconfdir}/surveil-webui/
ln -s /usr/share/surveil-webui/components/config/config.json %{buildroot}/%{_sysconfdir}/surveil-webui/config.json

# httpd config
install -d %{buildroot}/%{_sysconfdir}/httpd/conf.d
install -pm0755 %{S:1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/surveil-webui.conf

# Install configure dashboard script
mkdir -p %{buildroot}%{_bindir}
cp container/configure-dashboard.sh %{buildroot}%{_bindir}/surveil-webui-init

%files
/usr/share/surveil-webui
%{_bindir}/surveil-webui-init
%config(noreplace) %{_sysconfdir}/httpd/conf.d/surveil-webui.conf
%config(noreplace) %{_sysconfdir}/surveil-webui/config.json


%changelog
* Wed Jun 17 2015 Vincent Fournier <vincent.fournier@savoirfairelinux.com> 0.9.0-1
- Updated surveil-webui to 0.9.0

* Wed Jun 10 2015 Thibault Cohen <thibault.cohen@savoirfairelinux.com> 0.8.0-1
- Initial Package
