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

%global base_version 4.3.10
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

%define default_user root
%define default_prefix /opt/glite

Name:           yaim-storm
Version:        %{base_version}
Release:        %{release_version}%{?dist}
Vendor:         EMI
License:        Apache License
URL:            http://grid-it.cnaf.infn.it
Source:         %{name}.tar.gz
Group:          System Environment/Shells
AutoReqProv:    yes
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Summary:        Provides the utility files

BuildRequires: libtool
BuildRequires: automake
BuildRequires: autoconf
Requires: glite-yaim-core

%define debug_package %{nil}

%description
This contains information to configure StoRM nodes.

%prep
%setup -q -n yaim-storm

%build
./bootstrap
./configure --prefix=%{default_prefix}
make

%pre

%post

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{default_user},%{default_user},-)

%dir %{default_prefix}/yaim/
%dir %{default_prefix}/yaim/defaults
%{default_prefix}/yaim/defaults

%dir %{default_prefix}/yaim/etc
%dir %{default_prefix}/yaim/etc/versions
%{default_prefix}/yaim/etc/versions/%{name}

%dir %{default_prefix}/yaim/examples
%dir %{default_prefix}/yaim/examples/siteinfo
%dir %{default_prefix}/yaim/examples/siteinfo/services
%{default_prefix}/yaim/examples/siteinfo/services

%dir %{default_prefix}/yaim/functions
%dir %{default_prefix}/yaim/functions/local
%dir %{default_prefix}/yaim/functions/utils
%{default_prefix}/yaim/functions/local
%{default_prefix}/yaim/functions/utils

%dir %{default_prefix}/yaim/node-info.d
%{default_prefix}/yaim/node-info.d

%changelog
* Wed Jun 7 2017 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 4.3.9-1
- Fix for https://issues.infn.it/jira/browse/STOR-946

* Thu Jan 16 2014 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 4.3.5-1
- Fix for https://issues.infn.it/jira/browse/STOR-560
- Fix for https://issues.infn.it/jira/browse/STOR-506
