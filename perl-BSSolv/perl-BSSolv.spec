#
# spec file for package perl-BSSolv
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%global gitrev 9ef394f

Name:           perl-BSSolv
Version:        0.18.2
Release:        2.git%{gitrev}%{?dist}
Url:            https://github.com/openSUSE/open-build-service
#Taken from https://github.com/openSUSE/open-build-service/tree/master/src/backend
#from revision %{gitrev}
Source0:        Makefile.PL
Source1:        BSSolv.pm
Source2:        BSSolv.xs
Source3:        typemap

BuildRequires:  libsolv-devel >= 0.3.0-7
Requires:       libsolv
BuildRequires:  libdb4-devel
BuildRequires:  perl
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  expat-devel
%if 0%{?rhel_version} || 0%{?centos_version}
BuildRequires:  db4-devel
%endif
BuildRequires:  cmake
BuildRequires:  perl
BuildRequires:  rpm-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
#RHEL6 moved ExtUtils::MakeMaker outside the main perl package
BuildRequires:  perl(ExtUtils::MakeMaker)
# the testsuite uses the check framework
BuildRequires:  check-devel
Summary:        A new approach to package dependency solving
License:        BSD
Group:          Development/Libraries

%description
Using a Satisfyability Solver to compute package dependencies.

%prep
%setup -c %{name}-%{version}-%{release} -T
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build
perl Makefile.PL
make

%install
make DESTDIR=$RPM_BUILD_ROOT install_vendor
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} \;  
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;  
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'  
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;  
%{_fixperms} $RPM_BUILD_ROOT/*  

%files
%{perl_vendorarch}/BSSolv.pm
%{perl_vendorarch}/auto/BSSolv

%changelog
* Thu Jul 18 2013 Miroslav Suchý <msuchy@redhat.com> 0.18.2-2.git228d412
- Take BSSolv.* from obs-server backend (msuchy@redhat.com)
- Use libsolv 0.3.0 (msuchy@redhat.com)
- add git hash to release and comment how to get source (msuchy@redhat.com)
- perl-BSSolv.src: W: invalid-license BSD-3-Clause (msuchy@redhat.com)
- perl-BSSolv.src:93: W: mixed-use-of-spaces-and-tabs (spaces: line 18, tab:
  line 93) (msuchy@redhat.com)
- perl-BSSolv.src:72: W: setup-not-quiet (msuchy@redhat.com)
- perl-BSSolv.src: W: non-standard-group Development/Libraries/C and C++
  (msuchy@redhat.com)

* Thu Jul 18 2013 Miroslav Suchý <msuchy@redhat.com> 0.18.2-1
- new package

