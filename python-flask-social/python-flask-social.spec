# Created by pyp2rpm-1.1.1
%global pypi_name Flask-Social
%global with_python3 1

Name:           python-%{pypi_name}
Version:        1.6.2
Release:        1%{?dist}
Summary:        Simple OAuth provider integration for Flask-Security

License:        MIT
URL:            https://github.com/mattupstate/flask-social
Source0:        https://pypi.python.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-devel
BuildRequires:  python-nose
BuildRequires:  python-mock
BuildRequires:  python-flask-sqlalchemy
BuildRequires:  python-flask-mongoengine
BuildRequires:  python-flask-Peewee
 
%if %{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-mock
BuildRequires:  python3-Flask-SQLAlchemy
BuildRequires:  python3-Flask-MongoEngine
BuildRequires:  python3-Flask-Peewee
%endif # if with_python3
 
Requires:       python-Flask-Security >= 1.6.3
Requires:       python-Flask-OAuth >= 0.12

%description
Flask-Social
============

Oauth provider login and APIs for use with
`Flask-
Security <http://packages.python.org/Flask-Security/>`_

Resources
---------

-
`Documentation <http://packages.python.org/Flask-Social/>`_
- `Issue Tracker
<http://github.com/mattupstate/flask-social/issues>`_
- `Code
<http://github.com/mattupstate/flask-social/>`_
- `Development Version
  ...

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Simple OAuth provider integration for Flask-Security
 
Requires:       python3-Flask-Security >= 1.6.3
Requires:       python3-Flask-OAuth >= 0.12

%description -n python3-%{pypi_name}
Flask-Social
============

Oauth provider login and APIs for use with
`Flask-
Security <http://packages.python.org/Flask-Security/>`_

Resources
---------

-
`Documentation <http://packages.python.org/Flask-Social/>`_
- `Issue Tracker
<http://github.com/mattupstate/flask-social/issues>`_
- `Code
<http://github.com/mattupstate/flask-social/>`_
- `Development Version
  ...
%endif # with_python3


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}


%check
%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3


%files
%doc README.rst
%{python2_sitelib}/Flask-Social
%{python2_sitelib}/Flask_Social-%{version}-py?.?.egg-info
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%{python3_sitelib}/Flask-Social
%{python3_sitelib}/Flask_Social-%{version}-py?.?.egg-info
%endif # with_python3


%changelog
* Sat Jan 03 2015 Miroslav Suchy,,, <msuchy@redhat.com> - 1.6.2-1
- Initial package.
