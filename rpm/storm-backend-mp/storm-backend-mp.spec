%global base_version 1.0.0
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-backend-mp
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM backend server metapackage

Group: System Environment/Libraries
License:  ASL 2.0
Url: https://github.com/italiangrid/storm-mp

Requires: lcg-expiregridmapdir
Requires: fetch-crl
Requires: umd-release
Requires: storm-backend-server
Requires: cleanup-grid-accounts
Requires: storm-dynamic-info-provider
Requires: glite-yaim-bdii
Requires: edg-mkgridmap
Requires: lcas-lcmaps-gt4-interface

%description
StoRM Backend metapackage

%build

%install

%clean

%files

%changelog

* Mon Oct 07 2019 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.0.0-1
- Created from old emi-storm-backend-mp
