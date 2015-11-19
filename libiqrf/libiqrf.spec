%global checkout .20130729git%{shortcommit0}
%global commit0 36ac0ef7bc36159e990f62633fd4b9708e741a44
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name: libiqrf
Version: 0
Release: 1%{checkout}%{?dist}
Summary: Interface library to iqrf devices
License: LGPLv2+
URL: http://open-nandra.com/projects/iqrf/libiqrf-library/
Source0: https://github.com/nandra/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Patch0: libdir.patch
BuildRequires: libusb-devel
BuildRequires: cmake
BuildRequires: make

%description
Libiqrf is library for access to/from iqrf devices which are connected to host
PC over USB. This library is also used for IDE and examples.

%package devel
Summary: Development files for libiqrf
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files, libraries and documentation needed to
develop applications that use %{name}.


%prep
%setup -qn %{name}-%{commit0}
%patch0 -p1

%build
%{cmake} .
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README AUTHORS
%{_libdir}/libiqrf.so.*

%files devel
%{_includedir}/iqrf.h
%{_libdir}/libiqrf.so



%changelog
* Thu Nov 19 2015 Miroslav Suchý <miroslav@suchy.cz> 0-1.20130729git36ac0ef
- new package


