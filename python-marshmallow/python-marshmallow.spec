%global upstream_name marshmallow
%global commit a8b33850c74975250fa81308ce3aa4868128d3ba
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{upstream_name}
Version:        2.0.0b5
Release:        2%{?dist}
Summary:        Python library for converting complex datatypes to and from primitive types
License:        MIT
URL:            http://marshmallow.readthedocs.org/
# Using Github instead of PyPI because the PyPI tarballs don't include tests, 
# docs, or examples, and upstream does not want to change that.
# https://github.com/marshmallow-code/marshmallow/issues/201
Source0:        https://github.com/marshmallow-code/marshmallow/archive/%{commit}/%{upstream_name}-%{commit}.tar.gz
# remove dependency on bundled ordered_set
Patch0:         ordered_set.patch
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-dateutil
Requires:       python-ordered-set
# for tests
BuildRequires:  pytest
BuildRequires:  pytz
BuildRequires:  python-dateutil
BuildRequires:  python-ordered-set
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# for tests
BuildRequires:  python3-pytest
BuildRequires:  python3-pytz
BuildRequires:  python3-dateutil
BuildRequires:  python-ordered-set
%endif

%description
Marshmallow is a framework-agnostic library for converting complex datatypes, 
such as objects, to and from primitive Python datatypes.

Marshmallow schemas can be used to:
* Validate input data.
* Deserialize input data to app-level objects.
* Serialize app-level objects to primitive Python types. The serialized objects 
  can then be rendered to standard formats such as JSON for use in an HTTP API.

%if %{with python3}
%package -n python3-%{upstream_name}
Summary:        Python 3 library for converting complex datatypes to and from primitive types
%if %{with python3}
Requires:       python3-dateutil
Requires:       python3-ordered-set
%endif

%description -n python3-%{upstream_name}
Marshmallow is a framework-agnostic library for converting complex datatypes, 
such as objects, to and from primitive Python datatypes.

Marshmallow schemas can be used to:
* Validate input data.
* Deserialize input data to app-level objects.
* Serialize app-level objects to primitive Python types. The serialized objects 
  can then be rendered to standard formats such as JSON for use in an HTTP API.
%endif

%prep
%setup -q -n %{upstream_name}-%{commit}
%patch0

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_docdir}/python3-%{upstream_name}
cp -a docs/* examples %{buildroot}%{_docdir}/python3-%{upstream_name}/
popd
rm -f %{buildroot}%{python3_sitelib}/%{upstream_name}/ordereddict.py*
rm -f %{buildroot}%{python3_sitelib}/%{upstream_name}/orderedset.py*
%endif

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_docdir}/python-%{upstream_name}
cp -a docs/* examples %{buildroot}%{_docdir}/python-%{upstream_name}/
rm -f %{buildroot}%{python_sitelib}/%{upstream_name}/ordereddict.py*
rm -f %{buildroot}%{python_sitelib}/%{upstream_name}/orderedset.py*

%check
PYTHONPATH=%{buildroot}%{python_sitelib} %{__python} setup.py test

%if %{with python3}
pushd %{py3dir}
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} setup.py test
popd
%endif

%files
%doc CHANGELOG.rst AUTHORS.rst README.rst
#%doc %{_docdir}/python-%{upstream_name}
%exclude %{_docdir}/python-%{upstream_name}/*.pyc
%exclude %{_docdir}/python-%{upstream_name}/*.pyo
%exclude %{_docdir}/python-%{upstream_name}/examples/*.pyc
%exclude %{_docdir}/python-%{upstream_name}/examples/*.pyo
%license LICENSE
%{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}*.egg-info

%if %{with python3}
%files -n python3-%{upstream_name}
%doc CHANGELOG.rst AUTHORS.rst README.rst
#%doc %{_docdir}/python3-%{upstream_name}
%exclude %{_docdir}/python3-%{upstream_name}/*.pyc
%exclude %{_docdir}/python3-%{upstream_name}/*.pyo
%exclude %{_docdir}/python3-%{upstream_name}/examples/*.pyc
%exclude %{_docdir}/python3-%{upstream_name}/examples/*.pyo
%license LICENSE
%{python3_sitelib}/%{upstream_name}
%{python3_sitelib}/%{upstream_name}*.egg-info
%endif

%changelog
* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 2.0.0b5-2
- unbundle ordereddict and ordered set
- add documentation

* Mon Aug 24 2015 Valentin Gologuzov <vgologuz@redhat.com> - 2.0.0b5-1
- Rebuild with the newest upstream version

* Thu May 07 2015 Dan Callaghan <dcallagh@redhat.com> - 1.2.6-1
- initial version
