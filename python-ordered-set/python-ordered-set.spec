%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%global __python2 python2
%endif
%global short_name ordered-set
%global dir_name ordered_set

Name:           python-%{short_name}
Version:        2.0.2
Release:        0%{?dist}
Summary:        A Custom MutableSet that remembers its order

License:        MIT
URL:            https://github.com/LuminosoInsight/ordered-set
Source0:        https://pypi.python.org/packages/source/o/%{short_name}/%{short_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
%if 0%{?rhel}
BuildRequires:  python-setuptools
%endif # rhel
#test
BuildRequires:  python-nose
%if %{with python3}
BuildRequires:  python3-devel
#test
BuildRequires:  python3-nose
%endif # with python3

%global _description\
An OrderedSet is a custom MutableSet that remembers its order, so that every\
entry has an index that can be looked up.

%description %_description

%package -n python2-%{short_name}
Summary: %summary
%{?python_provide:%python_provide python2-%{short_name}}

%description -n python2-%{short_name} %_description

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
%{__python2} setup.py nosetests
popd

%if %{with python3}
pushd python3
%{__python2} setup.py nosetests
popd
%endif


%files -n python2-%{short_name}
%doc python2/README
%license python2/MIT-LICENSE
%{python_sitelib}/*

%if %{with python3}
%files -n python3-%{short_name} 
%doc python3/README
%license python3/MIT-LICENSE
%{python3_sitelib}/%{dir_name}.py
%{python3_sitelib}/*egg-info/
%{python3_sitelib}/__pycache__/*
%endif # with python3


%changelog
* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.0-8
- Python 2 binary package renamed to python2-ordered-set
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.0.0-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Feb 09 2016 Miroslav Suchý <miroslav@suchy.cz> 2.0.0-3
- fix BR condition

* Tue Feb 09 2016 Miroslav Suchý <miroslav@suchy.cz> 2.0.0-2
- add BR python-nose for test

* Tue Feb 09 2016 Miroslav Suchý <miroslav@suchy.cz> 2.0.0-1
- rebase to 2.0.0

* Tue Sep 22 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-4
- add missing BR on el6
- add missing macro on el6

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-3
- include egg-info again
- fix typo

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-2
- exclude __pycache__/ from filelist

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 1.3.1-1
- new package

