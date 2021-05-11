# Copyright (c) Istituto Nazionale di Fisica Nucleare (INFN). 2006-2010.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## Turn off meaningless jar repackaging (works only on SL6)
%define __jar_repack 0

%global base_version 1.11.21
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

%define _modulename backend-server
%define prefixname storm

Name: storm-backend-server
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM backend server

Group: Applications/File
License:  ASL 2.0
Url: https://github.com/italiangrid/storm
Source: %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}

BuildArch: noarch

BuildRequires: apache-maven
BuildRequires: jpackage-utils
BuildRequires: java-11-openjdk-devel

Requires: java-11-openjdk
Requires: jpackage-utils
Requires: storm-native-libs >= 1.0.6-2
Requires: storm-native-libs-lcmaps >= 1.0.6-2
Requires: storm-native-libs-java >= 1.0.6-2

%description
StoRM provides an SRM interface to any POSIX filesystem with direct file
access ("file:" transport protocol), but can take advantage of special
features of high performance parallel and cluster file systems, as GPFS from
IBM and Lustre from SUN.

This package contains the StoRM backend server.


%prep
%setup -q -n %{name}

%build
mvn -DskipTests -U clean package

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar -C $RPM_BUILD_ROOT -xvzf target/%{name}.tar.gz

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,storm,storm,755)

%attr(755,root,root) %dir %{_javadir}/%{name}
%attr(755,root,root) %{_javadir}/%{name}/*.jar

%dir %{_sysconfdir}/%{prefixname}/%{_modulename}
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_database_config.sh
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_be_ISAM_mysql_update_from_1.0.0_to_1.1.0.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_mysql_grant.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_mysql_tbl.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_mysql_update_from_1.7.0_to_1.7.1.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/db/storm_mysql_update_from_1.7.1_to_1.7.2.sql
%{_sysconfdir}/%{prefixname}/%{_modulename}/lcmaps.db
%config(noreplace) %{_sysconfdir}/%{prefixname}/%{_modulename}/logging.xml
%{_sysconfdir}/%{prefixname}/%{_modulename}/namespace-1.5.0.xsd
%config(noreplace) %{_sysconfdir}/%{prefixname}/%{_modulename}/namespace.xml
%config(noreplace) %{_sysconfdir}/%{prefixname}/%{_modulename}/path-authz.db
%{_sysconfdir}/%{prefixname}/%{_modulename}/storm.properties.template
%{_sysconfdir}/%{prefixname}/%{_modulename}/used-space.ini.template
%{_sysconfdir}/%{prefixname}/%{_modulename}/welcome.txt
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%attr(644,root,root) %{_exec_prefix}/lib/systemd/system/%{name}.service
%dir %attr(644,root,root) %{_sysconfdir}/systemd/system/%{name}.service.d
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/systemd/system/%{name}.service.d/%{name}.conf

%attr(750,storm,storm) %dir %{_localstatedir}/log/%{prefixname}

%pre
# create user storm, if it does not exist
getent group storm > /dev/null || groupadd -r storm
getent passwd storm > /dev/null || useradd -r -g storm \
  -d %{_sysconfdir}/storm -s /sbin/nologin -c "StoRM server account" storm

%post
#during an install, the value of the argument passed in is 1
if [ "$1" = "1" ] ; then
  # start a service at boot
  systemctl enable %{name}.service
fi;
#during an upgrade, the value of the argument passed in is 2
if [ "$1" = "2" ] ; then
  systemctl daemon-reload
  systemctl restart %{name}.service
fi;

%preun
# when uninstalling
if [ "$1" = "0" ] ; then
  # stop and disable service
  systemctl stop %{name}
  systemctl disable %{name}.service
fi;

%postun
#during an upgrade, the value of the argument passed in is 1
#during an uninstall, the value of the argument passed in is 0
if [ "$1" = "1" ] ; then
  echo "A restart of the service is needed to make the new version effective"
fi;
if [ "$1" = "0" ] ; then
  rm -f %{_exec_prefix}/lib/systemd/system/%{name}.service
  rm -rf %{_sysconfdir}/systemd/system/%{name}.service.d
fi;

%changelog
* Tue May 11 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.21-1
- Bumped version to 1.11.21-1

* Fri Apr 23 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.21-0
- Bumped version to 1.11.21-0

* Mon Apr 12 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.20-1
- Added daemon reload on restart

* Thu Apr 1 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.20-1
- Bumped version to 1.11.20-1

* Tue Mar 23 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.20-0
- Requires Java 11

* Mon Mar 15 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.20-0
- Bumped version to 1.11.20-0
- Removed support for CentOS 6
- Requires native libs v1.0.6

* Wed Oct 28 2020 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.19-1
- Bumped version to 1.11.19-1

* Mon Sep 14 2020 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.19-0
- Bumped version to 1.11.19-0

* Fri Aug 07 2020 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.18-1
- Bumped version to 1.11.18-1

* Tue Sep 11 2018 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.15-0
- Bumped packaging version to 1.11.15-0

* Tue Jun 5 2018 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.14-1
- Bumped packaging version to 1.11.14-1

* Wed Apr 18 2018 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.14-0
- Bumped packaging version to 1.11.14-0

* Tue Oct 31 2017 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.13-1
- Bumped packaging version to 1.11.13-1.

* Wed Oct 11 2017 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.13-0
- Bumped packaging version to 1.11.13-0.

* Tue Jun 6 2017 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.12-0
- Bumped packaging version for 1.11.12 release.

* Wed Feb 3 2016 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.11-0
- Bumped packaging version for 1.11.11 release.

* Fri Dec 18 2015 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.11.10-1
- Bumped packaging version for 1.11.10 release.

* Wed Jun 3 2015 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.9-1
- Bumped packaging version for 1.11.9 release.

* Fri Mar 13 2015 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.8-1
- Bumped packaging version for 1.11.8 release.

* Tue Jan 29 2015 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.7-1
- Bumped packaging version for 1.11.7 release.

* Tue Jan 19 2015 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.6-1
- Bumped packaging version for 1.11.6 release.

* Tue Jan 14 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.5-1
- Bumped packaging version for 1.11.5 release.

* Tue Jan 14 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.4-1
- Bumped packaging version for 1.11.4 release.

* Wed Oct 30 2013 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.3-1
- Fix for https://issues.infn.it/jira/browse/STOR-341
- Fix for https://issues.infn.it/jira/browse/STOR-342
- Fix for https://issues.infn.it/jira/browse/STOR-344

* Wed Jun 12 2013 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.11.2-1
- Integrated native libs interface v. 1.0.1
