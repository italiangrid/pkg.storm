%define prefixname storm
%define shortname  frontend-server
%define longname   storm-frontend-server

%define default_user root

%global base_version 1.8.14
%global base_release 0

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-frontend-server
Version: %{base_version}
Release: %{release_version}%{?dist}

Group: Applications/Libraries
License: ASL 2.0
URL: https://github.com/italiangrid/storm-frontend

Source: %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Summary: The StoRM Frontend component

BuildRequires: boost-devel
BuildRequires: curl-devel
BuildRequires: mysql-devel
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: globus-gss-assist-devel
BuildRequires: globus-common-devel
BuildRequires: globus-gridmap-callout-error-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: krb5-devel
BuildRequires: gsoap-devel
BuildRequires: CGSI-gSOAP-devel
BuildRequires: voms
BuildRequires: storm-xmlrpc-c-devel
BuildRequires: argus-pep-api-c
BuildRequires: argus-pep-api-c-devel

Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts

Requires: argus-pep-api-c
Requires: curl
Requires: globus-gssapi-gsi
Requires: mysql
Requires: storm-xmlrpc-c
Requires: storm-xmlrpc-c-client
Requires: voms
Requires: CGSI-gSOAP
Requires: boost-program-options
Requires: boost-thread
Requires: gsoap

%description
This is the installation bundle for the StoRM FrontEnd server.

StoRM provides an SRM interface to any POSIX filesystem with direct file
access ("file:" transport protocol), but can take advantage of special
features of high performance parallel and cluster file systems, as
GPFS from IBM and Lustre from SUN.

%prep
%setup -q -n storm-frontend-server

%build
sh bootstrap
%configure
make

%pre
# create user storm, if it does not exist
getent group storm > /dev/null || groupadd -r storm
getent passwd storm > /dev/null || useradd -r -g storm \
  -d %{_sysconfdir}/storm -s /sbin/nologin -c "StoRM server account" storm

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/log/%{prefixname}
# CentOS >7
mkdir -p $RPM_BUILD_ROOT%{_exec_prefix}/lib/systemd/system
cp etc/systemd/%{longname}.service $RPM_BUILD_ROOT%{_exec_prefix}/lib/systemd/system/%{longname}.service
rm -rf $RPM_BUILD_ROOT/etc/init.d/%{longname}

%post
#during an install, the value of the argument passed in is 1
if [ "$1" = "1" ] ; then
  # add the service to chkconfig
  systemctl enable %{longname}.service
fi;
#during an upgrade, the value of the argument passed in is 2
if [ "$1" = "2" ] ; then
  echo "The StoRM Frontend server has been upgraded but NOT configured yet."
  echo "Manually configure service or use StoRM Puppet module."
fi;

%preun
#during an upgrade, the value of the argument passed in is 1
#during an uninstall, the value of the argument passed in is 0
if [ "$1" = "0" ] ; then
  # disable service
  systemctl disable %{longname}.service
fi;

%postun
#during an upgrade, the value of the argument passed in is 1
#during an uninstall, the value of the argument passed in is 0
if [ "$1" = "1" ] ; then
  echo "A restart of the service is needed to make the new version effective"
fi;
if [ "$1" = "0" ] ; then
  rm -f %{_exec_prefix}/lib/systemd/system/%{longname}.service
fi;

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/%{longname}

%{_exec_prefix}/lib/systemd/system/%{longname}.service

%config(noreplace) %{_sysconfdir}/sysconfig/%{longname}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{longname}

%dir %{_sysconfdir}/%{prefixname}/%{shortname}
%config(noreplace) %{_sysconfdir}/%{prefixname}/%{shortname}/%{longname}.conf.template

%doc %dir %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}-%{version}/ChangeLog
%doc %{_datadir}/doc/%{name}-%{version}/CREDITS
%doc %{_datadir}/doc/%{name}-%{version}/LICENSE
%doc %{_datadir}/doc/%{name}-%{version}/README
%doc %{_datadir}/doc/%{name}-%{version}/README.md

%doc %dir %{_datadir}/wsdl
%doc %{_datadir}/wsdl/srm.v2.2.wsdl

%attr(750,storm,storm) %dir %{_localstatedir}/log/%{prefixname}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Dec 16 2020 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.8.14-0
- Bumped version to 1.8.14-0 and removed CentOS 6 stuff

* Fri Aug 07 2020 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.8.13-1
- Bumped version to 1.8.13-1

* Tue Mar 17 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.8.13-0
- Bumped packaging version to 1.8.13-0 and added support to systemd unit

* Fri Sep 7 2018 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.8.12-0
- Bumped packaging version to 1.8.12-0

* Tue Jun 5 2018 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.8.11-1
- Bumped packaging version to 1.8.11-1

* Sun Mar 18 2018 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.8.11-0
- Bumped packaging version to 1.8.11-0

* Mon Apr 11 2016 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.8.10-0
- Bumped packaging version to 1.8.10-0

* Wed Jun 3 2015 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.8.9-1
- Bumped packaging version to 1.8.9-1

* Thu Feb 19 2015 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.8.8-1
- Bumped packaging version to 1.8.8-1

* Wed Feb 4 2015 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.8.7-1
- Bumped packaging version to 1.8.7-1

* Fri Oct 31 2014 Daniele Andreotti <daniele.andreotti@cnaf.infn.it> - 1.8.6-1
- Bumped packaging version for 1.8.6 release

* Tue May 20 2014 Daniele Andreotti <daniele.andreotti@cnaf.infn.it> - 1.8.5-1
- Bumped packaging version for 1.8.5 release

* Tue Oct 22 2013 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.8.4-1
- Improved exception handling and error reporting
- Fix for https://issues.infn.it/jira/browse/STOR-343
- Fix for https://issues.infn.it/jira/browse/STOR-344

* Fri Aug 23 2013 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.8.3-1
- Fix for https://issues.infn.it/jira/browse/STOR-331

* Tue Jul 23 2013 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.8.2-1
- Added /etc/sysconfig/storm-frontend-server file reference in spec file

* Mon May 27 2013 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.8.1-2
- Packaging code refactoring

* Mon May 02 2011 Elisabetta Roncheiri <elisabetta.ronchieri@cnaf.infn.it> - 1.7.0-5.sl5
- Added BuildRequires in spec file
- Added src in the src tar file
- Cleaned configuration file
- Fix bug of apostrophe in dn

* Mon Apr 04 2011 Elisabetta Ronchieri> <elisabetta.ronchieri@cnaf.infn.it> - 1.7.0-2.sl5
- Renamed package

* Fri Feb 24 2011 Elisabetta Ronchieri> <elisabetta.ronchieri@cnaf.infn.it> - 1.7.0-1.sl5
- Added Fedora guidelines
