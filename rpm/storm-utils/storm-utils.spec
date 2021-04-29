%global base_version 1.0.0
%global base_release 0

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-utils
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: A StoRM set of commands

Group: System Environment/Libraries
License:  ASL 2.0
Url: https://github.com/italiangrid/storm-utils

%description
StoRM utils

%build

%install
mkdir -p %{buildroot}/usr/local/sbin
cd %{_sourcedir}
ls -latr
tar -zxvf %{name}.tar.gz
install -m 755 %{_sourcedir}/%{name}/space-reporting/storm-get-space-aliases.sh %{buildroot}/usr/local/sbin/storm-get-space-aliases.sh
install -m 755 %{_sourcedir}/%{name}/space-reporting/storm-update-used-space.sh %{buildroot}/usr/local/sbin/storm-update-used-space.sh

%clean

%files
/usr/local/sbin/storm-get-space-aliases.sh
/usr/local/sbin/storm-update-used-space.sh

%changelog

* Thu Apr 29 2021 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.0.0-0
- First 2 scripts added
- Bumped version to v1.0.0-0