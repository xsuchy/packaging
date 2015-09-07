%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif
%global short_name ordered-set
%global dir_name ordered_set

Name:           python-%{short_name}
Version:        1.3.1
Release:        3%{?dist}
Summary:        A Custom MutableSet that remembers its order

License:        MIT
URL:            https://github.com/LuminosoInsight/ordered-set
Source0:        https://pypi.python.org/packages/source/o/%{short_name}/%{short_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
%if %{with python3}
BuildRequires:  python3-devel
%endif # with python3

%description
An OrderedSet is a custom MutableSet that remembers its order, so that every
entry has an index that can be looked up.

%if %{with python3}
%package     -n python3-%{short_name}
Summary:        A Custom MutableSet that remembers its order

%description -n python3-%{short_name}
An OrderedSet is a custom MutableSet that remembers its order, so that every
entry has an index that can be looked up.

This package contains python3 bindings.
%endif # with python3


%prep
%setup -qc
mv %{short_name}-%{version} python2

%if %{with python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
%{__python2} setup.py build
popd

%if %{with python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with python3

%install
%if %{with python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif # with python3

pushd python2
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
popd


%check
pushd python2
%{__python2} setup.py test
popd

%if %{with python3}
pushd python3
%{__python2} setup.py test
popd
%endif


%files
%doc python2/README
%{python_sitelib}/*

%if %{with python3}
%files -n python3-%{short_name} 
%doc python3/README
%{python3_sitelib}/%{dir_name}.py
%{python3_sitelib}/*egg-info/
%{python3_sitelib}/__pycache__/*
%endif # with python3


%changelog
* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-3
- include egg-info again
- fix typo

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-2
- exclude __pycache__/ from filelist

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-1
- new package

