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

%define libtype      %{_libdir}

%define prefixname   storm
%define shortname    storm-globus-gridftp
%define longname     storm-globus-gridftp-server

%global base_version 1.2.4
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-globus-gridftp-server
Version: %{base_version}
Release: %{release_version}%{?dist}

Group: Applications/Libraries
License: ASL 2.0
URL: https://github.com/italiangrid/storm-gridftp-dsi.git

Source: %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Summary: The StoRM GridFtp DSI component

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: zlib
BuildRequires: openssl-devel
BuildRequires: libattr-devel
BuildRequires: globus-gridftp-server-devel
BuildRequires: globus-ftp-control-devel
BuildRequires: globus-ftp-client-devel

Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts

Requires: globus-gssapi-gsi
Requires: openssl
Requires: zlib
Requires: globus-gridftp-server-progs

%define debug_package %{nil}

%description
GridFTP2 DSI calculates checksum on the fly for StoRM

%prep
%setup -q -n %{name}

%build
./bootstrap
./configure --prefix=/usr --sysconfdir=/etc --datadir=/usr/share --localstatedir=/var
make

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{libtype}/libglobus_gridftp_server_StoRM.la
rm -f $RPM_BUILD_ROOT/%{libtype}/libglobus_gridftp_server_StoRM.a
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/log/%{prefixname}
%if 0%{?rhel} == 7
  mkdir -p $RPM_BUILD_ROOT%{_exec_prefix}/lib/systemd/system
  cp config/systemd/storm-globus-gridftp.service $RPM_BUILD_ROOT%{_exec_prefix}/lib/systemd/system/%{shortname}.service
  rm -rf $RPM_BUILD_ROOT/etc/init.d/%{shortname}
%endif

%post
#during an install, the value of the argument passed in is 1
#during an unupgrade, the value of the argument passed in is 2
if [ "$1" = "1" ] ; then
  echo 'Enable service to start at boot'
  %if 0%{?rhel} == 7
    systemctl enable %{shortname}.service
  %else
    /sbin/chkconfig --add %{shortname}
  %endif
fi;
if [ "$1" = "2" ] ; then
  echo 'stop service'
  %if 0%{?rhel} == 7
    systemctl stop %{shortname}.service
  %else
    /sbin/service %{shortname} stop >/dev/null 2>&1 || :
  %endif
fi;

%preun
#during an upgrade, the value of the argument passed in is 1
#during an uninstall, the value of the argument passed in is 0
if [ "$1" = "0" ] ; then
  echo 'stop service and disable automatic boot'
  %if 0%{?rhel} == 7
    systemctl stop %{shortname}.service
    systemctl disable %{shortname}.service
  %else
    /sbin/service %{shortname} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{shortname}
  %endif
fi;
if [ "$1" = "1" ] ; then
  echo 'stop service'
  %if 0%{?rhel} == 7
    systemctl stop %{shortname}.service
  %else
    /sbin/service %{shortname} stop >/dev/null 2>&1 || :
  %endif
  /sbin/service %{shortname} stop >/dev/null 2>&1 || :
fi;

%postun
#during an upgrade, the value of the argument passed in is 1
#during an uninstall, the value of the argument passed in is 0
if [ "$1" = "1" ] ; then
  echo 'stop service'
  %if 0%{?rhel} == 7
    systemctl stop %{shortname}.service
  %else
    /sbin/service %{shortname} stop >/dev/null 2>&1 || :
  %endif
fi;
if [ "$1" = "0" ] ; then
  %if 0%{?rhel} == 7
    rm -f %{_exec_prefix}/lib/systemd/system/%{shortname}.service
  %else
    echo 'remove old file'
    rm -f /etc/init.d/%{shortname}.*
  %endif
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%if 0%{?rhel} == 7
  %attr(644,root,root) %{_exec_prefix}/lib/systemd/system/%{shortname}.service
%else
  %{_sysconfdir}/init.d/%{shortname}
%endif

%config(noreplace) %attr(644,root,root) %{_sysconfdir}/logrotate.d/%{shortname}

%{libtype}/libglobus_gridftp_server_StoRM.so
%{libtype}/libglobus_gridftp_server_StoRM.so.0
%{libtype}/libglobus_gridftp_server_StoRM.so.0.0.0

%doc %dir %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}-%{version}/ChangeLog
%doc %{_datadir}/doc/%{name}-%{version}/CREDITS
%doc %{_datadir}/doc/%{name}-%{version}/LICENSE
%doc %{_datadir}/doc/%{name}-%{version}/README

%attr(750,storm,storm) %dir %{_localstatedir}/log/%{prefixname}

%changelog
* Fri Aug 07 2020 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.2.4-1
- Bumped version to 1.2.4-1

* Mon Mar 23 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.2.4-0
- Bumped version to 1.2.4-0

* Fri Dec 13 2019 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.2.3-1
- Bumped version to 1.2.3-1

* Fri Jul 26 2019 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.2.2-1
- Bumped version to 1.2.2-1

* Fri Mar 1 2019 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.2.2-0
- Bumped version to 1.2.2-0

* Tue Jul 24 2018 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.2.1-1
- Bumped version to 1.2.1-1

* Mon May 02 2011 Elisabetta Roncheiri <elisabetta.ronchieri@cnaf.infn.it> - 1.1.0-5.sl5
- Added BuildRequires in spec file
- Added src in the src tar file
- Cleaned configuration file

* Thu Apr 07 2011 Elisabetta Ronchieri> <elisabetta.ronchieri@cnaf.infn.it> - 1.1.0-4.sl5
- Renamed globus-gridftp in storm-globus-gridftp
- Changed log path and log file names

* Fri Feb 24 2011 Elisabetta Ronchieri> <elisabetta.ronchieri@cnaf.infn.it> - 1.1.0-2.sl5
- Added Fedora guidelines
