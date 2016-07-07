%global modname marshmallow
%global _docdir_fmt %{name}

Name:           python-%{modname}
Version:        2.9.0
Release:        1%{?dist}
Summary:        Python library for converting complex datatypes to and from primitive types
License:        MIT
URL:            http://marshmallow.readthedocs.org/
# Using Github instead of PyPI because the PyPI tarballs don't include tests, 
# docs, or examples, and upstream does not want to change that.
# https://github.com/marshmallow-code/marshmallow/issues/201
Source0:        https://github.com/marshmallow-code/marshmallow/archive/%{version}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

%global _description \
Marshmallow is a framework-agnostic library for converting complex datatypes,\
such as objects, to and from primitive Python datatypes.\
\
Marshmallow schemas can be used to:\
* Validate input data.\
* Deserialize input data to app-level objects.\
* Serialize app-level objects to primitive Python types. The serialized objects\
  can then be rendered to standard formats such as JSON for use in an HTTP API.

%description %{_description}

%package doc
Summary:        Documentation for %{name}
Provides:       python3-%{modname}-doc = %{version}
Obsoletes:      python3-%{modname}-doc < 2.8.0-1
BuildRequires:  /usr/bin/sphinx-build

%description doc
Documentation for %{name}.

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# for tests
BuildRequires:  python2-pytest
BuildRequires:  python2-pytz
BuildRequires:  python-ordered-set
BuildRequires:  python2-dateutil
BuildRequires:  python-simplejson
Requires:       python-ordered-set
Recommends:     python2-dateutil
Recommends:     python-simplejson

%description -n python2-%{modname} %{_description}

Python 2 version.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# for tests
BuildRequires:  python3-pytest
BuildRequires:  python3-pytz
BuildRequires:  python3-ordered-set
BuildRequires:  python3-dateutil
BuildRequires:  python3-simplejson
Requires:       python3-ordered-set
Recommends:     python3-dateutil
Recommends:     python3-simplejson

%description -n python3-%{modname} %{_description}

Python 3 version.

%prep
%autosetup -n %{modname}-%{version}

# remove bundled library
# instead of orderedsett we patch code to usu python-ordered-set
# ordereddict.py is used only for compatibility with python2.6,
# which we do not need
rm -f ./marshmallow/ordereddict.py ./marshmallow/orderedset.py
sed -i -e "s/from marshmallow.orderedset/from ordered_set/g" %{modname}/schema.py

# Drop support for sphinx-issues as it's not yet packaged
sed -i -e "/sphinx_issues/d" docs/conf.py

%build
%py2_build
%py3_build
sphinx-build -b html docs html

%install
%py2_install
%py3_install
rm -rf html/{.buildinfo,.doctrees}

%check
py.test-%{python2_version} -v
py.test-%{python3_version} -v

%files doc
%license LICENSE
%doc html examples

%files -n python2-%{modname}
%license LICENSE
%doc CHANGELOG.rst README.rst
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/%{modname}-*.egg-info/

%files -n python3-%{modname}
%license LICENSE
%doc CHANGELOG.rst README.rst
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-*.egg-info/

%changelog
* Thu Jul 07 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.9.0-1
- Update to 2.9.0

* Wed Jul 06 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.8.0-1
- Update to 2.8.0
- Add recommends
- Modernize spec

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-0.3.gitea1def9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Miroslav Suchý <msuchy@redhat.com> 2.2.1-0.2.gitea1def9
- add BR simplejson
- add BR python-tox

* Wed Nov 18 2015 Miroslav Suchý <msuchy@redhat.com> 2.2.1-0.1.gitea1def9
- rebase to 2.2.1

* Wed Nov 18 2015 Miroslav Suchý <miroslav@suchy.cz> 2.2.1-0.0.gitea1def9
- rebase to 2.2.1

* Fri Sep 11 2015 Miroslav Suchý <miroslav@suchy.cz> 2.0.0-0.6.gita8b3385
- 1219288 - fix ownership of docdir and use correct release number

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
