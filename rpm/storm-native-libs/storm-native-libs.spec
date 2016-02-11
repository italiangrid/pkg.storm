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


%global base_version 1.0.4
%global base_release 0

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.dev.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-native-libs
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM backend server interface to native libraries

Group: Development/Libraries
License: ASL 2.0
URL: https://github.com/italiangrid/storm-native-libs
Source: %{name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: apache-maven
BuildRequires: jpackage-utils
BuildRequires: swig
BuildRequires: libacl-devel
BuildRequires: lcmaps-without-gsi-devel
BuildRequires: lcmaps-interface
BuildRequires: java-1.6.0-openjdk-devel
BuildRequires: gpfs.base >= 3.3

%description
This package provides the StoRM backend interface to posix libraries.

%package java
Summary: The StoRM backend server interface to native libraries (java part)
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: java-1.6.0-openjdk

%description java
This package provides the StoRM backend interface to posix libraries.
In particular, this package provides the Java swig stubs.

%package gpfs
Summary: The StoRM backend server interface to GPFS native libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libacl
Requires: gpfs.base >= 3.3

%description gpfs
This package provides the StoRM backend interface to GPFS libraries.

%package lcmaps
Summary: The StoRM backend server interface to LCMAPS native libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: lcmaps
Requires: lcmaps-without-gsi
Requires: lcas-lcmaps-gt4-interface
Requires: lcmaps-plugins-basic
Requires: lcmaps-plugins-voms

%description lcmaps
This package provides the StoRM backend interface to LCMAPS libraries.

%prep
%setup -q -n %{name}

%build
pushd native
./bootstrap
export CFLAGS="-O0 -ggdb -Wall"
export CXXFLAGS="-O0 -ggdb -Wall"
%configure --with-java_home=%{java_home} --enable-gpfs
make
popd

mvn -DskipTests -U package

%install
rm -rf $RPM_BUILD_ROOT
pushd native
make install DESTDIR=$RPM_BUILD_ROOT
popd

install -dm 755 $RPM_BUILD_ROOT%{_javadir}/storm-backend-server
install -m 644 target/storm-native-interface-%{pom_version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/storm-backend-server

# Move libraries
install -dm 755 $RPM_BUILD_ROOT%{_libdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/libgpfs.*
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libposixapi_interface.so.0*
%{_libdir}/libposixapi_interface.so

%{_libdir}/libstorm-xattrs.so.0*
%{_libdir}/libstorm-xattrs.so

%files java
%defattr(-,root,root,-)
%{_javadir}/storm-backend-server/storm-native-interface-%{pom_version}.jar

%files gpfs
%defattr(-,root,root,-)
%{_libdir}/libgpfsapi_interface.so.0*
%{_libdir}/libgpfsapi_interface.so

%files lcmaps
%defattr(-,root,root,-)
%{_libdir}/libstorm_lcmaps.so.0*
%{_libdir}/libstorm_lcmaps.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gpfs -p /sbin/ldconfig
%postun gpfs -p /sbin/ldconfig

%post lcmaps -p /sbin/ldconfig
%postun lcmaps -p /sbin/ldconfig

%changelog
* Tue Apr 14 2015 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.0.4-1
  Fix for https://issues.infn.it/jira/browse/STOR-474
* Wed Nov 12 2014 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.0.3-1
  Fix for https://issues.infn.it/jira/browse/STOR-419
* Wed Jun 26 2014 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.0.2-1
- Force dependency on GPFS v. 3.3
* Wed Jun 12 2013 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.0.1-1
- Fix for https://issues.infn.it/jira/browse/STOR-250
* Fri Mar 1 2013 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.0.0-1
- StoRM native libraries first packaging
