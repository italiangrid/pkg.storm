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

%global base_version 0.1.1
%global base_release 0

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

%global slash_name storm/cdmi

Name:    cdmi-storm
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM CDMI plugin

Group: Applications/File
License:  ASL 2.0
Url: https://github.com/italiangrid/cdmi-storm
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

Requires: cdmi-server
Requires: java-1.8.0-openjdk
Requires: jpackage-utils

%description

%prep
%setup -q -n %{name}

%build
mvn -DskipTests -U clean package

%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/cdmi-server/plugins
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cdmi-server/plugins/capabilities/container
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cdmi-server/plugins/capabilities/dataobject
cp target/%{name}-%{base_version}-jar-with-dependencies.jar $RPM_BUILD_ROOT/usr/lib/cdmi-server/plugins
cp config/capabilities/exports.json $RPM_BUILD_ROOT%{_sysconfdir}/cdmi-server/plugins/capabilities/exports.json
cp config/capabilities/container/diskonly.json $RPM_BUILD_ROOT%{_sysconfdir}/cdmi-server/plugins/capabilities/container/diskonly.json
cp config/capabilities/dataobject/diskonly.json $RPM_BUILD_ROOT%{_sysconfdir}/cdmi-server/plugins/capabilities/dataobject/diskonly.json
cp config/capabilities/dataobject/diskandtape.json $RPM_BUILD_ROOT%{_sysconfdir}/cdmi-server/plugins/capabilities/dataobject/diskandtape.json
cp config/capabilities/dataobject/tapeonly.json $RPM_BUILD_ROOT%{_sysconfdir}/cdmi-server/plugins/capabilities/dataobject/tapeonly.json
cp config/storm-properties.json $RPM_BUILD_ROOT%{_sysconfdir}/cdmi-server/plugins/storm-properties.json

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/lib/cdmi-server/plugins/%{name}-%{base_version}-jar-with-dependencies.jar
%config(noreplace) %{_sysconfdir}/cdmi-server/plugins/storm-properties.json
%config(noreplace) %{_sysconfdir}/cdmi-server/plugins/capabilities/exports.json
%config(noreplace) %{_sysconfdir}/cdmi-server/plugins/capabilities/container/diskonly.json
%config(noreplace) %{_sysconfdir}/cdmi-server/plugins/capabilities/dataobject/diskonly.json
%config(noreplace) %{_sysconfdir}/cdmi-server/plugins/capabilities/dataobject/diskandtape.json
%config(noreplace) %{_sysconfdir}/cdmi-server/plugins/capabilities/dataobject/tapeonly.json

%pre

%post

%preun

%changelog

* Tue Jun 30 2020 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 0.1.1-0
- Bumped version to 0.1.1-0

* Mon May 1 2017 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 0.1.0-0
- Initial packaging
