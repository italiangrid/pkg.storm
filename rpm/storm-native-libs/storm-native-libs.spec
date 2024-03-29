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


%global base_version 1.0.7
%global base_release 0

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
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
BuildRequires: java-11-openjdk-devel
BuildRequires: gpfs.base >= 3.4.0

%description
This package provides the StoRM backend interface to posix libraries.

%package java
Summary: The StoRM backend server interface to native libraries (java part)
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: java-11-openjdk

%description java
This package provides the StoRM backend interface to posix libraries.
In particular, this package provides the Java swig stubs.

%package gpfs
Summary: The StoRM backend server interface to GPFS native libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libacl
Requires: gpfs.base >= 3.4

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
install -m 644 target/storm-native-interface-%{base_version}.jar \
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
%{_javadir}/storm-backend-server/storm-native-interface-%{base_version}.jar

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
* Fri Nov 19 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.0.7-0
- Bump version to 1.0.7-0
* Mon Mar 29 2021 Enrico Vianello <enrico.vianello at cnaf.infn.it> - 1.0.6-2
- Java 11 required
* Tue Aug 4 2020 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.0.6-1
- Use posix acl calls also for GPFS filesystems
* Tue May 15 2018 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 1.0.5-2
- Require GPFS-3.4.0 at build time
