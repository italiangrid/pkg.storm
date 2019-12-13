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

%global base_version 1.2.1
%global base_release 1

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
License:  ASL 2.0
Url: https://github.com/italiangrid/storm-webdav
Source:    %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: apache-maven
BuildRequires: jpackage-utils
BuildRequires: java-1.8.0-openjdk-devel

Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts

Requires: java-1.8.0-openjdk
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
%if %{el7}
  rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{name}
%else
  rm -f $RPM_BUILD_ROOT%{_exec_prefix}/lib/systemd/system/%{name}.service
%endif

%clean
cd $HOME/sources/%{name}
mvn clean
rm -rf $RPM_BUILD_ROOT

%files

%if %{el7}
  %attr(644,root,root) %{_exec_prefix}/lib/systemd/system/%{name}.service
%else
  %attr(755,root,root) %{_sysconfdir}/init.d/%{name}
%endif

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

%dir %{_sysconfdir}/%{slash_name}/config
%{_sysconfdir}/%{slash_name}/config/README.md
%{_sysconfdir}/%{slash_name}/config/application.yml

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
  %if %{el7}
    systemctl enable %{name}.service
  %else
    /sbin/chkconfig --add %{name}
  %endif
# when upgrading
elif [ $1 -gt 1 ] ; then
  # restart the service
  %if %{el7}
    systemctl restart %{name}.service
  %else
    /sbin/service %{name} restart >/dev/null 2>&1 || :
  %endif
fi

%preun
# when uninstalling
if [ "$1" = "0" ] ; then
  # stop and disable service
  %if %{el7}
    systemctl stop %{name}.service
    systemctl disable %{name}.service
  %else
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
  %endif
fi

%changelog

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
