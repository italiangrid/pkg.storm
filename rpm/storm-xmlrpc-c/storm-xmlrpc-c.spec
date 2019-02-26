%global base_version 1.39.12
%global base_release 2

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-xmlrpc-c
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: A lightweight RPC library based on XML and HTTP.

License: BSD and MIT
Vendor: EMI
Group: System Environment/Libraries
Packager: Elisabetta Ronchieri
BuildArch: x86_64
BuildRoot: %{_builddir}/var/tmp/%{name}-%{version}
AutoReqProv: yes

Source: %name-%version.tar.gz

BuildRequires: curl-devel
BuildRequires: libxml2-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: autoconf

%package c++
Summary:  C++ libraries for emi storm xmlrpc-c
Group:    System Environment/Libraries
Requires: %name = %version-%release
Requires: %name-c++ = %version-%release

%package client
Summary:  C client libraries for xmlrpc-c
Group:    System Environment/Libraries
Requires: %name = %version-%release

%package client++
Summary:  C++ client libraries for xmlrpc-c
Group:    System Environment/Libraries
Requires: %name = %version-%release
Requires: %name-c++ = %version-%release
Requires: %name-client = %version-%release

%package devel
Summary:  Development files for xmlrpc-c based programs
Group:    Development/Libraries
Requires: %name = %version-%release
Requires: %name-c++ = %version-%release
Requires: %name-client = %version-%release
Requires: %name-client++ = %version-%release
Requires: libxml2-devel curl-devel
Requires: pkgconfig

%package apps
Summary:  Sample XML-RPC applications
Group:    Applications/Internet
Requires: %name = %version-%release
Requires: %name-c++ = %version-%release
Requires: %name-client = %version-%release
Requires: %name-client++ = %version-%release

%description
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.
This library provides a modular implementation of XML-RPC for C.

%description c++
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.
This library provides a modular implementation of XML-RPC for C++.

%description client
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.
This library provides a modular implementation of XML-RPC for C
clients.
%description client++
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.
This library provides a modular implementation of XML-RPC for C++
clients.

%description devel
Static libraries and header files for writing XML-RPC applications in
C and C++.

%description apps
XML-RPC is a quick-and-easy way to make procedure calls over the
Internet. It converts the procedure call into XML document, sends it
to a remote server using HTTP, and gets back the response as XML.
This package contains some handy XML-RPC demo applications.

%prep
%setup -q -n %{name}-%{version}
rm doc/{INSTALL,configure_doc}

%build
CFLAGS="${CFLAGS:--O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:--O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:--O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -I/usr/lib64/gfortran/modules}" ; export FFLAGS ;
./configure \
	--program-prefix= \
	--prefix=/usr \
	--exec-prefix=/usr \
	--sysconfdir=/etc \
	--datadir=/usr/share \
	--includedir=/usr/include \
	--libdir=/usr/lib64 \
	--libexecdir=/usr/libexec \
	--localstatedir=/var \
	--sharedstatedir=/var/lib \
	--mandir=/usr/share/man \
	--infodir=/usr/share/info \
	--enable-curl-client  \
	--disable-libwww-client \
	--enable-cplusplus \
	--enable-shared-libs \
	--includedir=/usr/include/storm \
	--libdir=/usr/lib64/storm \
	--mandir=/usr/man/storm \
	--localstatedir=/usr/var/storm \
	--bindir=/usr/bin/storm \
	--sbindir=/usr/sbin/storm

make VERBOSE=1
cd tools
make
cd ..

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd tools
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

chmod +x $RPM_BUILD_ROOT%_libdir/storm/*.so
rm -f $RPM_BUILD_ROOT%_libdir/storm/*.a

mkdir -p $RPM_BUILD_ROOT%_mandir/storm/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post client -p /sbin/ldconfig
%postun client -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%post client++ -p /sbin/ldconfig
%postun client++ -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%_libdir/storm/*.so.3*
%exclude %_libdir/storm/libxmlrpc_client.so*

%files client
%defattr(-,root,root,-)
%_libdir/storm/libxmlrpc_client.so.*

%files c++
%defattr(-,root,root,-)
%_libdir/storm/*.so.8*
%exclude %_libdir/storm/libxmlrpc_client++.so*

%files client++
%defattr(-,root,root,-)
%_libdir/storm/libxmlrpc_client++.so.*

%files devel
%defattr(-,root,root,-)
%_bindir/storm/xmlrpc-c-config
%_includedir/storm/xmlrpc-c
%_includedir/storm/*.h
%_libdir/storm/*.so

%files apps
%defattr(-,root,root,-)
%_bindir/storm/xmlrpc
%_bindir/storm/xmlrpc_transport
%_bindir/storm/xml-rpc-api2cpp
%_bindir/storm/xmlrpc_cpp_proxy
%_bindir/storm/xml-rpc-api2txt
%_bindir/storm/xmlrpc_parsecall
%_bindir/storm/xmlrpc_pstream

%exclude /usr/man/storm/man1/*

%changelog
* Tue Jun 5 2018 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.39.12-1
- Bumped version to 1.39.12-1

* Thu May 10 2018 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.39.12-0
- Repackaged latest super-stable release

* Mon Jun 22 2015 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> - 1.33.0-1
- Repackaged latest super-stable release
