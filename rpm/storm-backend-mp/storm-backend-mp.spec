%global base_version 1.3.0
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
Requires: storm-backend-server >= 1.12.0
Requires: cleanup-grid-accounts
Requires: storm-dynamic-info-provider >= 2.0.0
Requires: edg-mkgridmap
Requires: lcas-lcmaps-gt4-interface
Requires: storm-utils

# moved from backend spec file
Requires: nc

%description
StoRM Backend metapackage

%build

%install

%clean

%files

%changelog
* Tue May 11 2021 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.2.0-1
- Bumped version to 1.2.0-1

* Thu May 6 2021 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.2.0-0
- Requires storm-utils
- Bumped version to 1.2.0-0

* Mon Mar 29 2021 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.1.0-2
- Removed CentOS 6 stuff

* Thu Mar 31 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.1.0-1
- Requires yaim-storm for RHEL6 and bumped version to 1.1.0-1

* Mon Oct 07 2019 Enrico Vianello <enrico.vianello@cnaf.infn.it> - 1.0.0-1
- Created from old emi-storm-backend-mp
