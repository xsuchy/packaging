%global srcname ordered-set
%global dir_name ordered_set

Name:           python-%{srcname}
Version:        4.1.0
Release:        4%{?dist}
Summary:        Custom MutableSet that remembers its order

License:        MIT
URL:            https://github.com/rspeer/ordered-set
Source0:        %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
#tests
BuildRequires:  python3-nose
BuildRequires:  python3-pytest

%global _description\
An OrderedSet is a custom MutableSet that remembers its order, so that every\
entry has an index that can be looked up.

%description %_description

%package     -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%pytest

%files -n python3-%{srcname}
%license MIT-LICENSE
%doc README.md
%{python3_sitelib}/%{dir_name}-*.egg-info/
%dir %{python3_sitelib}/%{dir_name}
%{python3_sitelib}/%{dir_name}/*.py
%{python3_sitelib}/%{dir_name}/__pycache__

%changelog
* Wed Nov 30 2022 Miroslav Suchý <msuchy@redhat.com> 4.1.0-4
- use spdx license 

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.1.0-2
- Rebuilt for Python 3.11

* Thu Jan 27 2022 Miroslav Suchý <msuchy@redhat.com> 4.1.0-1
- remove old changelog entries
- change files section
- rebase to 4.1.0
- change of upstream url
- run pytest instead of nose

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 4.0.1-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.1-2
- Rebuilt for Python 3.9

* Thu Apr 30 2020 Miroslav Suchý <msuchy@redhat.com> 4.0.1-1
- Update to 4.0.1 (#1829620)

* Fri Mar 13 2020 Miroslav Suchý <miroslav@suchy.cz> 3.1.1-2
- rebase to 3.1.1

* Fri Mar 13 2020 Miroslav Suchý 3.1.1-1
- rebase to 3.1.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
