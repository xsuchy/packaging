%global _pkgdescription A python library for manipulation of the proposed module metadata format.

%if 0%{?fedora} > 21 || 0%{?rhel} > 7
%global with_python3 1
%else
%global with_python3 0
%endif

%{!?__python2: %global __python2 /usr/bin/python2}
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}}} 

Name:           modulemd
Version:        1.0.2
Release:        1%{?dist}
Summary:        Module metadata manipulation library
License:        MIT
URL:            https://pagure.io/modulemd
Source0:        https://files.pythonhosted.org/packages/source/m/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  PyYAML
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-PyYAML
BuildRequires:  python3-setuptools
%endif

%description
%{_pkgdescription}

%package -n python2-%{name}
Summary:        %{summary}
Requires:       PyYAML
Provides:       python-%{name} = %{version}-%{release}

%description -n python2-%{name}
%{_pkgdescription}

These are python2 bindings.

%if 0%{?with_python3}
%package -n python3-%{name}
Summary:        %{summary}
Requires:       python3-PyYAML

%description -n python3-%{name}
%{_pkgdescription}

These are python3 bindings.
%endif

%prep
%setup -q

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%files -n python2-%{name}
%doc README.rst spec.yaml
%license LICENSE
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{name}
%doc README.rst spec.yaml
%license LICENSE
%{python3_sitelib}/*
%endif

%changelog
* Tue Nov 08 2016 Petr Šabata <contyk@redhat.com> - 1.0.2-1
- 1.0.2 bugfix release

* Tue Nov 08 2016 Petr Šabata <contyk@redhat.com> - 1.0.1-1
- First official release

* Fri Sep 23 2016 Jan Kaluza <jkaluza@redhat.com> - 0-13
- build without Python 3 support on older distributions that don't have it

* Fri Sep 16 2016 Petr Šabata <contyk@redhat.com> - 0-12
- Update modlint's runtime dependencies
- modlint shouldn't install the README and spec.yaml files

* Wed Aug 03 2016 Jan Kaluza <jkaluza@redhat.com> - 0-11
- Add modlint subpackage

* Tue Jul 19 2016 Petr Šabata <contyk@redhat.com> - 0-10
- Don't fail validation tests
- Use safe_dump() for dumping YAMLs

* Tue Jul 12 2016 Petr Šabata <contyk@redhat.com> - 0-9
- Profiles now support description
- The components section is now truly optional

* Sat Jul 09 2016 Petr Šabata <contyk@redhat.com> - 0-8
- rpms.update_package() now allows updating just one property

* Thu Jun 30 2016 Petr Šabata <contyk@redhat.com> - 0-7
- Adding support for binary package filters

* Tue Jun 21 2016 Petr Šabata <contyk@redhat.com> - 0-6
- New metadata format
   - module use-case profiles are now supported

* Tue Jun 14 2016 Petr Šabata <contyk@redhat.com> - 0-5
- Rename metadata.yaml to spec.yaml

* Tue Jun 14 2016 Petr Šabata <contyk@redhat.com> - 0-4
- New metadata format
   - rpms/api now holds the module RPM-defined API

* Fri Jun 10 2016 Petr Šabata <contyk@redhat.com> - 0-3
- New metadata format
  - rpms/dependencies defaults to False
  - rpms/fulltree was removed

* Thu May 12 2016 Petr Šabata <contyk@redhat.com> - 0-2
- New metadata format, rationale is now required

* Fri May 06 2016 Petr Šabata <contyk@redhat.com> - 0-1
- New metadata format

* Mon May 02 2016 Petr Šabata <contyk@redhat.com> - 0-0
- This package was build automatically.
