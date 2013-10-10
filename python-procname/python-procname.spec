%if 0%{?fedora} > 12
%global with_python3 1
%endif

%global mod_name procname

Name:           python-procname
Version:        0.3
Release:        2%{?dist}
Summary:        Set process titles in Python programs

License:        LGPLv2+
URL:            http://github.com/lericson/procname/
Source0:        https://pypi.python.org/packages/source/p/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  pytest 

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pytest
%endif

%description
This python module allows you to set the process title of a process under at
least Linux and Mac OS X.

%if 0%{?with_python3}
%package -n python3-whoosh
Summary:    Fast, Python3 full text indexing, search, and spell checking library

%description -n python3-whoosh
This python module allows you to set the process title of a process under at
least Linux and Mac OS X.
%endif

%prep
%setup -q -n %{mod_name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%check
%{__python} setup.py test

%if 0%{with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif

%files
%doc docs/html/ README.txt LICENSE.txt
%{python_sitelib}/*.egg-info/
%{python_sitelib}/whoosh

%if 0%{?with_python3}
%files -n python3-whoosh
%doc README.txt LICENSE.txt docs/html/
%{python3_sitelib}/whoosh
%{python3_sitelib}/*.egg-info/
%endif

%changelog
* Thu Oct 10 2013 Miroslav Suchý <msuchy@redhat.com> 0.3-2
- new package built with tito

* Mon Sep 09 2013 Robert Kuska <rkuska@redhat.com> - 2.5.3-1
- Rebase to 2.5.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 Robert Kuska <rkuska@redhat.com> - 2.5.1-1
- Update source
- Add python3 subpackage (rhbz#979235)

* Mon Apr 08 2013 Robert Kuska <rkuska@redhat.com> - 2.4.1-2
- Review fixes

* Fri Apr 05 2013 Robert Kuska <rkuska@redhat.com> - 2.4.1-1
- Initial package

