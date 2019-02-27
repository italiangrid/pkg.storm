%global base_version 1.2.1
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: emi-storm-backend-mp
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM backend server metapackage

Group: System Environment/Libraries
License:  ASL 2.0
Url: https://github.com/italiangrid/storm-mp

Requires: lcg-expiregridmapdir
Requires: fetch-crl
Requires: emi-version
Requires: yaim-storm
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

* Thu Jun 01 2017 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.2.1-0
- Moved to pkg.storm
