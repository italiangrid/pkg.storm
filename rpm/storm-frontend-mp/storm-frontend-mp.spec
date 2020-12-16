%global base_version 1.3.0
%global base_release 0

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-frontend-mp
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM frontend server metapackage

Group: System Environment/Libraries
License:  ASL 2.0
Url: https://github.com/italiangrid/storm-mp

Requires: lcg-expiregridmapdir
Requires: fetch-crl
Requires: umd-release
Requires: storm-frontend-server
Requires: cleanup-grid-accounts
Requires: edg-mkgridmap

%description
StoRM Frontend metapackage

%build

%install

%clean

%files

%changelog

* Wed Dec 16 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.3.0-0
- Removed CentOS 6 support. Bumped version to 1.3.0-0

* Thu Mar 31 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.2.0-1
- Renamed to storm-frontend-mp and replaced emi-release with umd-release. Bumped version to 1.2.0-1

* Thu Jun 05 2017 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.1.0-2
- Moved to pkg.storm
