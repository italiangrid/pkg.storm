## Turn off meaningless jar repackaging
%define __jar_repack 0

%global base_version 1.11.11
%global base_release 0

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

%global slash_name storm/webdav

Name:    storm-webdav
Version: %{base_version}
Release: %{release_version}
Summary: The StoRM WebDAV server

Group: Applications/File
License:  ASL 2.0
Url: https://github.com/italiangrid/storm-webdav
Source:    %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: apache-maven
BuildRequires: jpackage-utils
BuildRequires: java-1.7.0-openjdk-devel

Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts

Requires: java-1.7.0-openjdk
Requires: jpackage-utils

%description
StoRM provides an SRM interface to any POSIX filesystem with direct file
access ("file:" transport protocol), but can take advantage of special
features of high performance parallel and cluster file systems, as GPFS from
IBM and Lustre from SUN.

This package provides the StoRM WebDAV server.

%prep
%setup -q -n %{name}

%build
mvn -DskipTests -U clean package

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar -C $RPM_BUILD_ROOT -xvzf target/%{name}-server.tar.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(755,root,root) %{_sysconfdir}/init.d/%{name}

%defattr(644,root,root,755)
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{name}-server.jar

%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{slash_name}/logback.xml
%config(noreplace) %{_sysconfdir}/%{slash_name}/logback-access.xml
%{_sysconfdir}/%{slash_name}/README.md

%dir %{_sysconfdir}/%{slash_name}/sa.d
%{_sysconfdir}/%{slash_name}/sa.d/README.md
%{_sysconfdir}/%{slash_name}/sa.d/*.template

%dir %{_sysconfdir}/%{slash_name}/vo-mapfiles.d
%{_sysconfdir}/%{slash_name}/vo-mapfiles.d/README.md

%attr(750,storm,storm) %dir %{_localstatedir}/log/%{slash_name}
%attr(755,storm,storm) %dir %{_localstatedir}/lib/%{name}/work

%pre
# create user storm, if it does not exist
getent group storm > /dev/null || groupadd -r storm
getent passwd storm > /dev/null || useradd -r -g storm \
  -d %{_sysconfdir}/storm -s /sbin/nologin -c "StoRM server account" storm

%post
# when installing
if [ "$1" = "1" ] ; then
  # add the service to chkconfig
  /sbin/chkconfig --add %{name}
# when upgrading
elif [ $1 -gt 1 ] ; then
  # restart the service
  /sbin/service %{name} restart >/dev/null 2>&1 || :
fi

%preun
# when uninstalling
if [ "$1" = "0" ] ; then
  # stop the service
  /sbin/service %{name} stop >/dev/null 2>&1 || :
  # remove the service from chk
  /sbin/chkconfig --del %{name}
fi

%changelog

* Mon Sep 1 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.0.0-0
- Initial packaging
