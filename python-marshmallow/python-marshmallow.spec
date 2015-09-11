%global upstream_name marshmallow
%global commit a8b33850c74975250fa81308ce3aa4868128d3ba
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{upstream_name}
Version:        2.0.0
Release:        0.5.%{shortcommit}%{?dist}
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
BuildRequires:  python3-ordered-set
%endif

%description
Marshmallow is a framework-agnostic library for converting complex datatypes, 
such as objects, to and from primitive Python datatypes.

Marshmallow schemas can be used to:
* Validate input data.
* Deserialize input data to app-level objects.
* Serialize app-level objects to primitive Python types. The serialized objects 
  can then be rendered to standard formats such as JSON for use in an HTTP API.

%package doc
Summary: Documentation for %{name}
BuildArch: noarch

%description doc
Documentation for %{name}.

%if %{with python3}
%package -n python3-%{upstream_name}
Summary:        Python 3 library for converting complex datatypes to and from primitive types
Requires:       python3-dateutil
Requires:       python3-ordered-set

%description -n python3-%{upstream_name}
Marshmallow is a framework-agnostic library for converting complex datatypes, 
such as objects, to and from primitive Python datatypes.

Marshmallow schemas can be used to:
* Validate input data.
* Deserialize input data to app-level objects.
* Serialize app-level objects to primitive Python types. The serialized objects 
  can then be rendered to standard formats such as JSON for use in an HTTP API.

%package -n python3-%{upstream_name}-doc
Summary: Documentation for python3-%{upstream_name}
BuildArch: noarch

%description -n python3-%{upstream_name}-doc
Documentation for %{name}.

%endif # with python3

%prep
%setup -q -n %{upstream_name}-%{commit}
%patch0

# remove bundled library
# instead of orderedsett we patch code to usu python-ordered-set
# ordereddict.py is used only for compatibility with python2.6,
# which we do not need
rm -f ./marshmallow/ordereddict.py ./marshmallow/orderedset.py


%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
mkdir -p %{buildroot}%{_docdir}/python-%{upstream_name}
cp -a docs/* examples %{buildroot}%{_docdir}/python-%{upstream_name}/

%if %{with python3}
%py3_install
mkdir -p %{buildroot}%{_docdir}/python3-%{upstream_name}
cp -a docs/* examples %{buildroot}%{_docdir}/python3-%{upstream_name}/
%endif

%check
%{__python2} setup.py test
%if %{with python3}
%{__python3} setup.py test
%endif

%files
%doc CHANGELOG.rst AUTHORS.rst README.rst
%exclude %{_docdir}/python-%{upstream_name}
%exclude %{_docdir}/python-%{upstream_name}/*.pyc
%exclude %{_docdir}/python-%{upstream_name}/*.pyo
%exclude %{_docdir}/python-%{upstream_name}/examples/*.pyc
%exclude %{_docdir}/python-%{upstream_name}/examples/*.pyo
%license LICENSE
%{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}*.egg-info

%files doc
%license LICENSE
%doc %{_docdir}/python-%{upstream_name}
%exclude %{_docdir}/python-%{upstream_name}/CHANGELOG.rst
%exclude %{_docdir}/python-%{upstream_name}/AUTHORS.rst
%exclude %{_docdir}/python-%{upstream_name}/README.rst

%if %{with python3}
%files -n python3-%{upstream_name}
%doc CHANGELOG.rst AUTHORS.rst README.rst
%exclude %{_docdir}/python3-%{upstream_name}
%exclude %{_docdir}/python3-%{upstream_name}/*.pyc
%exclude %{_docdir}/python3-%{upstream_name}/*.pyo
%exclude %{_docdir}/python3-%{upstream_name}/examples/*.pyc
%exclude %{_docdir}/python3-%{upstream_name}/examples/*.pyo
%license LICENSE
%{python3_sitelib}/%{upstream_name}
%{python3_sitelib}/%{upstream_name}*.egg-info

%files -n python3-%{upstream_name}-doc
%license LICENSE
%doc %{_docdir}/python3-%{upstream_name}
%exclude %{_docdir}/python3-%{upstream_name}/CHANGELOG.rst
%exclude %{_docdir}/python3-%{upstream_name}/AUTHORS.rst
%exclude %{_docdir}/python3-%{upstream_name}/README.rst
%endif

%changelog
* Fri Sep 11 2015 Miroslav Suchý <msuchy@redhat.com> 2.0.0-0.5.a8b3385
- add short git hash to release number

* Fri Sep 11 2015 Miroslav Suchý <msuchy@redhat.com> 2.0.0b5-4
- create -doc subpackages
- 1219288 - reorganize spec file

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 2.0.0b5-3
- explicitely list docdir

* Mon Sep 07 2015 Miroslav Suchý <msuchy@redhat.com> 2.0.0b5-2
- unbundle ordereddict and ordered set
- add documentation

* Mon Aug 24 2015 Valentin Gologuzov <vgologuz@redhat.com> - 2.0.0b5-1
- Rebuild with the newest upstream version

* Thu May 07 2015 Dan Callaghan <dcallagh@redhat.com> - 1.2.6-1
- initial version
