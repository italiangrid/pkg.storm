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


%global base_version 1.6.1
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-srm-client
Version: %{base_version}
Release: %{release_version}%{?dist}
Vendor: EMI
License: ASL 2.0
URL: https://github.com/italiangrid/storm-client.git
Source: %{name}.tar.gz
Group: Applications/System
AutoReqProv: yes
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Summary: Provides the the StoRM SRM v2.2 clients

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: globus-gss-assist-devel
BuildRequires: gsoap-devel
BuildRequires: CGSI-gSOAP-devel
BuildRequires: voms

Requires: globus-gssapi-gsi
Requires: voms
Requires: CGSI-gSOAP
Requires: gsoap

%define debug_package %{nil}

%description
This is the installation bundle for the StoRM SRM v2.2 clients.
This bundle is part of the StoRM utility package that implements an SRM
interface to a GPFS parallel filesystem.

%prep
%setup -n storm-srm-client

%build
./bootstrap
./configure --bindir=/usr/bin --datadir=/usr/share
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc %dir %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}-%{version}/ChangeLog
%doc %{_datadir}/doc/%{name}-%{version}/CREDITS
%doc %{_datadir}/doc/%{name}-%{version}/LICENSE
%doc %{_datadir}/doc/%{name}-%{version}/README

%defattr(755,root,root)
%{_bindir}/clientSRM


%changelog
* Wed Oct 23 2013 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.6.1-1
- More informative error messages

* Mon May 27 2013 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.6.0-8
- Refactored packaging

* Mon May 02 2011 Elisabetta Roncheiri <elisabetta.ronchieri@cnaf.infn.it> - 1.5.0-5.sl5
- Added BuildRequires in spec file
- Added src in the src tar file
- Cleaned configuration file

* Tue Apr 05 2011 Elisabetta Ronchieri> <elisabetta.ronchieri@cnaf.infn.it> - 1.5.0
- Removed prefix
- Updated requires
