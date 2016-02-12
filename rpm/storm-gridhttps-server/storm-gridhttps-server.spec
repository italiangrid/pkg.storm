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

%global base_version 3.0.4
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-gridhttps-server
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM GridHTTPS server

Group: Development/Libraries
License: Apache License 2.0
URL: https://github.com/italiangrid/storm-gridhttps-server

Source:    %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: apache-maven
BuildRequires: java-1.6.0-openjdk-devel

Requires: java-1.6.0-openjdk

%description
The StoRM GridHTTPS component providing plain http(s) access and WebDAV access to StoRM managed files

%define _sysconfdir /etc
%define _javadir /usr/share/java
%define _docdir /usr/share/doc
%define default_user gridhttps
%define storm_user storm

%define conf_dir /etc/storm
%define short_name gridhttps-server
%define log_dir /var/log/storm

%prep

%setup -q -n %{name}

%build
mvn -DskipTests -U package

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar -C $RPM_BUILD_ROOT -xvzf target/%{name}.tar.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post

#during an install, the value of the argument passed in is 1
#during an upgrade, the value of the argument passed in is 2

%preun

#during an upgrade, the value of the argument passed in is 1
#during an uninstall, the value of the argument passed in is 0
if [ "$1" = "0" ] ; then
   if [ -f %{conf_dir}/%{short_name}/server.ini ]; then
      rm -f %{conf_dir}/%{short_name}/server.ini
   fi
   ls %{conf_dir}/%{short_name}/server.ini.bkp_* &> /dev/null
   if [ $? -eq 0 ]; then
      rm -f %{conf_dir}/%{short_name}/server.ini.bkp_*
   fi
fi

%files
%defattr(-,%{default_user},%{default_user})
%dir %{conf_dir}/
%dir %{conf_dir}/%{short_name}/
%config %{conf_dir}/%{short_name}/logging.xml
%attr(640,root,root) %config %{conf_dir}/%{short_name}/server.ini.template
%attr(755,%{default_user},%{default_user}) %{_sysconfdir}/init.d/%{name}

%dir %{_docdir}/%{name}-%{base_version}
%{_docdir}/%{name}-%{base_version}/LICENSE.txt

%dir %{_javadir}/%{name}
%{_javadir}/%{name}/storm-gridhttps-server.jar
%dir %{_javadir}/%{name}/lib
%{_javadir}/%{name}/lib/*.jar

%attr(755,%{storm_user},%{storm_user}) %dir %{log_dir}
