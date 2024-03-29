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

## Turn off meaningless jar repackaging
%define __jar_repack 0

%global base_version 1.4.2
%global base_release 0

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

%global slash_name storm/webdav

Name:    storm-webdav
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM WebDAV server

Group: Applications/File
License: ASL 2.0
Url: https://github.com/italiangrid/storm-webdav
Source:    %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: apache-maven
BuildRequires: jpackage-utils
BuildRequires: java-11-openjdk-devel

Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts

Requires: java-11-openjdk
Requires: jpackage-utils

%description
StoRM provides an SRM interface to any POSIX filesystem with direct file
access ("file:" transport protocol), but can take advantage of special
features of high performance parallel and cluster file systems, as GPFS from
IBM and Lustre from SUN.

This package provides the StoRM WebDAV server.

%prep
# %setup -q -n %{name}

%build

## This is needed since the storm-webdav git-commit-id maven plugin
## requires the .git folder to extract info, and such folder is not
## available in the source archive produced by pkg.base.
## As a 'temporary' workaround we build directly from the sources folder
cd $HOME/sources/%{name}
mvn -DskipTests -U clean package

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar -C $RPM_BUILD_ROOT -xvzf $HOME/sources/%{name}/target/%{name}-server.tar.gz

%clean
cd $HOME/sources/%{name}
mvn clean
rm -rf $RPM_BUILD_ROOT

%files

%attr(644,root,root) %{_exec_prefix}/lib/systemd/system/%{name}.service

%attr(755,root,root) %dir %{_javadir}/%{name}
%attr(644,root,root) %{_javadir}/%{name}/%{name}-server.jar

%defattr(640,root,storm,755)

%config(noreplace) %{_sysconfdir}/%{slash_name}/logback.xml
%config(noreplace) %{_sysconfdir}/%{slash_name}/logback-access.xml
%config(noreplace) %{_sysconfdir}/%{slash_name}/config/application.yml

%{_sysconfdir}/%{slash_name}/README.md

%dir %{_sysconfdir}/%{slash_name}/sa.d
%{_sysconfdir}/%{slash_name}/sa.d/README.md
%{_sysconfdir}/%{slash_name}/sa.d/*.template

%dir %{_sysconfdir}/%{slash_name}/config
%{_sysconfdir}/%{slash_name}/config/README.md

%dir %{_sysconfdir}/%{slash_name}/vo-mapfiles.d
%{_sysconfdir}/%{slash_name}/vo-mapfiles.d/README.md

%attr(750,storm,storm) %dir %{_localstatedir}/log/storm
%attr(750,storm,storm) %dir %{_localstatedir}/log/storm/webdav
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
  systemctl enable %{name}.service
# when upgrading
elif [ $1 -gt 1 ] ; then
  # restart the service
  systemctl daemon-reload
  systemctl restart %{name}.service
fi

%preun
# when uninstalling
if [ "$1" = "0" ] ; then
  # stop and disable service
  systemctl stop %{name}.service
fi

%changelog
* Mon May 9 2022 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.4.2-0
- Removed systemd drop-in files. Only directory will be created.

* Fri Oct 1 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.4.2-0
- Packaging for version 1.4.2-0

* Tue May 11 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.4.1-1
- Packaging for version 1.4.1-1

* Wed Apr 28 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.4.1-0
- Packaging for version 1.4.1-0

* Thu Apr 1 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.4.0-1
- Packaging for version 1.4.0-1

* Mon Feb 1 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.4.0-0
- Removed stuff related to centos6: init script and sysconfig file, service commands and others
- Added right permissions and ownership to log parent directory

* Mon Dec 11 2020 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.4.0-0
- Packaging for version 1.4.0-0

* Mon Sep 14 2020 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.3.1-1
- Packaging for version 1.3.1-1

* Fri Aug 07 2020 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.3.0-1
- Packaging for version to 1.3.0-1

* Fri Mar 27 2020 Enrico Vianello <enrico.vianello at cnaf.intn.it> - 1.3.0-0
- Packaging for version 1.3.0-0

* Fri Dec 13 2019 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.2.1-1
- Packaging for version 1.2.1

* Wed Nov 13 2019 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.2.0-0
- Fixed preun and post phases by addind el7 specific commands

* Tue Jun 11 2019 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.2.0-0
- Packaging for version 1.2.0

* Fri Oct 12 2018 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.1.0-0
- Packaging for version 1.1.0

* Mon Sep 1 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.0.0-0
- Initial packaging
