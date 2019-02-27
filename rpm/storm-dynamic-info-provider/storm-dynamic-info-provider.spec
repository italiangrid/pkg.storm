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

%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%define _confdir /etc/storm/info-provider
%define _bdiidir /var/lib/bdii/gip

%global base_version 1.8.1
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-dynamic-info-provider
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM dynamic info provider component

Group: Development/Libraries
License: Apache License 2.0
URL: https://github.com/italiangrid/storm-info-provider

Source:    %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
BuildRequires: python2-devel

Requires: python
Requires: python-ldap
Requires: python-argparse
Requires: bdii
Requires: glite-info-provider-service

%description
This is the installation bundle for the StoRM info provider component.

%prep
%setup -q -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libexecdir}
install -pm 0755 src/storm-info-provider $RPM_BUILD_ROOT%{_libexecdir}

install -d $RPM_BUILD_ROOT%{python2_sitelib}/info_provider
install -d $RPM_BUILD_ROOT%{python2_sitelib}/info_provider/glue
install -d $RPM_BUILD_ROOT%{python2_sitelib}/info_provider/model
install -d $RPM_BUILD_ROOT%{python2_sitelib}/info_provider/utils
install -pm 0644 src/info_provider/glue/* $RPM_BUILD_ROOT%{python2_sitelib}/info_provider/glue
install -pm 0644 src/info_provider/model/* $RPM_BUILD_ROOT%{python2_sitelib}/info_provider/model
install -pm 0644 src/info_provider/utils/* $RPM_BUILD_ROOT%{python2_sitelib}/info_provider/utils
install -pm 0644 src/info_provider/*.py $RPM_BUILD_ROOT%{python2_sitelib}/info_provider

install -d $RPM_BUILD_ROOT%{_confdir}
install -d $RPM_BUILD_ROOT%{_confdir}/templates
install -pm 0755 config/templates/* $RPM_BUILD_ROOT%{_confdir}/templates

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -pm 0644 man/* $RPM_BUILD_ROOT%{_mandir}/man1

%files
%defattr(-,root,root,-)
%{_libexecdir}/storm-info-provider
%{python2_sitelib}/info_provider
%{_confdir}/templates
%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%postun
rm -rf %{_bdiidir}/ldif/storm-glue13-static.ldif
rm -rf %{_bdiidir}/ldif/storm-glue2-static.ldif
rm -rf %{_bdiidir}/provider/storm-glue13-provider
rm -rf %{_bdiidir}/plugin/storm-glue13-plugin
rm -rf %{_bdiidir}/provider/storm-glue2-provider
rm -rf %{_bdiidir}/plugin/storm-glue2-plugin

%changelog
* Tue Oct 9 2018 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.8.1-0
  Bumped version to 1.8.1-0

* Tue Jan 9 2018 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.8.0-1
  Bumped version to 1.8.0 and added command get-report-json

* Mon Jan 18 2016 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.7.9-1
  Bumped version to 1.7.9-1

* Wed Aug 19 2015 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.7.9-0
  Bumped version to 1.7.9-0

* Tue Apr 21 2015 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.7.8-2
  Added required package and bumped version to 1.7.8-2

* Fri Mar 13 2015 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.7.8-1
  Bumped version to 1.7.8-1 for StoRM v1.11.8 release

* Thu Mar 12 2015 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.7.8-0
  Bumped version to 1.7.8-0

* Thu Mar 12 2015 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.7.7-2
- Repackaged to add python-simplejson dependency on EL5

* Wed Nov 12 2014 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.7.7-1
- Packaging for new python-based info provider
