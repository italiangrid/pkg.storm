%global base_version 1.1.0
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: storm-globus-gridftp-mp
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: The StoRM GridFTP server metapackage

Group: System Environment/Libraries
License:  ASL 2.0
Url: https://github.com/italiangrid/storm-mp

Requires: lcas-lcmaps-gt4-interface
Requires: lcas-plugins-basic
Requires: lcg-expiregridmapdir
Requires: umd-release
Requires: fetch-crl
Requires: lcmaps
Requires: lcas-plugins-voms
Requires: storm-globus-gridftp-server
Requires: lcmaps-without-gsi
Requires: lcmaps-plugins-basic
Requires: cleanup-grid-accounts
Requires: edg-mkgridmap
Requires: lcmaps-plugins-voms
Requires: lcas

%if 0%{?rhel} == 6
Requires: yaim-storm
%endif

%description
StoRM GridFTP metapackage

%build

%install

%clean

%files

%changelog
* Thu Mar 31 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.1.0-1
- Requires yaim-storm for RHEL6 and bumped version to 1.1.0-1

* Mon Oct 07 2019 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.0.0-1
- Created from old emi-storm-globus-mp
