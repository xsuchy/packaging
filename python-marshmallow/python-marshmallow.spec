%bcond_with    python2
%bcond_without python3

%global modname marshmallow
%global _docdir_fmt %{name}

Name:           python-%{modname}
Version:        3.11.1
Release:        1%{?dist}
Summary:        Python library for converting complex datatypes to and from primitive types
License:        MIT
URL:            http://marshmallow.readthedocs.org/
Source0:        https://github.com/marshmallow-code/marshmallow/archive/%{version}/%{modname}-%{version}.tar.gz
Patch0:         ordered_set.patch
Patch1:         versionwarning-disable.patch
# python3-autodocsumm is not in Fedora
# This is needed only for doc subpackage.
Patch2:         disable-autodocsumm.patch

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
BuildRequires:  python3-sphinx

%description doc
Documentation for %{name}.


%if %{with python2}
%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# for tests
BuildRequires:  python2-pytest
BuildRequires:  python2-pytz
BuildRequires:  python2-ordered-set
BuildRequires:  python2-dateutil
BuildRequires:  python2-simplejson
Requires:       python2-ordered-set
Recommends:     python2-dateutil
Recommends:     python2-simplejson

%description -n python2-%{modname} %{_description}

Python 2 version.
%endif


%if %{with python3}
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
%endif

%prep
%autosetup -n %{modname}-%{version} -p1

# remove bundled library
# instead of orderedsett we patch code to usu python-ordered-set
rm -f ./marshmallow/orderedset.py

# Drop support for sphinx-issues as it's not yet packaged
sed -i -e "/sphinx_issues/d" docs/conf.py

# unsupported theme option 'donate_url' given
sed -i -e "/donate_url/d" docs/conf.py

%build
%{?with_python2:%py2_build}
%{?with_python3:%py3_build}
sphinx-build -b html docs html

%install
%{?with_python2:%py2_install}
%{?with_python3:%py3_install}
rm -rf html/{.buildinfo,.doctrees}


%check
%{?with_python2:py.test-%{python2_version} -v --ignore tests/test_py3/}
%{?with_pythoN3:py.test-%{python3_version} -v}


%files doc
%license LICENSE
%doc html examples


%if %{with python2}
%files -n python2-%{modname}
%license LICENSE
%doc CHANGELOG.rst README.rst
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/%{modname}-*.egg-info/
%endif

%if %{with python3}
%files -n python3-%{modname}
%license LICENSE
%doc CHANGELOG.rst README.rst
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-*.egg-info/
%endif


%changelog
* Tue Mar 30 2021 Miroslav Suchý <msuchy@redhat.com> 3.11.1-1
- rebase to 3.11.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 16 2020 Miroslav Suchý <msuchy@redhat.com> 3.8.0-1
- disable autodocsumm in doc
- rebase to 3.8.0

* Tue Mar 24 2020 Miroslav Suchý <miroslav@suchy.cz> 3.5.1-1
- rebase to 3.5.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Miroslav Suchý <msuchy@redhat.com> 3.1.1-1
- rebase to python-marshmallow 3.1.1

* Wed Aug 21 2019 Miro Hrončok <mhroncok@redhat.com> - 2.20.0-2
- Rebuilt for Python 3.8

* Mon Aug 19 2019 Pavel Raiskup <praiskup@redhat.com> - 2.20.0-1
- latest upstream release

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.19.4-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Pavel Raiskup <praiskup@redhat.com> - 2.19.4-1
- new upstream release

* Sun Mar 31 2019 Pavel Raiskup <praiskup@redhat.com> - 2.19.2-1
- new upstream release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 Pavel Raiskup <praiskup@redhat.com> - 2.11.1-9
- add rpmbuild --wit{,hout}=python{2,3} options
- generate docs by python3-sphinx
- don't build Python 2 subpackage by default

* Fri Sep 21 2018 Miroslav Suchý <msuchy@redhat.com> 2.11.1-8
- add patch for CVE-2018-17175.patch

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.11.1-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.11.1-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.11.1-1
- Update to 2.11.1 (RHBZ #1411181)

* Tue Dec 27 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.10.5-1
- Update to 2.10.5 (RHBZ #1408340)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.10.4-2
- Rebuild for Python 3.6

* Thu Dec 01 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.10.4-1
- Update to 2.10.4 (RHBZ #1400189)

* Tue Oct 04 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.10.3-1
- Update to 2.10.3 (RHBZ #1381098)

* Thu Sep 15 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.10.1-2
- Update to 2.10.1 (RHBZ #1376432)

* Tue Sep 06 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.10.0-2
- Trivial fix in spec

* Tue Sep 06 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.10.0-1
- Update to 2.10.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

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
