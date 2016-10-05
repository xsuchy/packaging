%global pypi_name distro

# EPEL7 support: default Python is Python 2, and Python2 packages prefix
# is unversioned.
%if 0%{?rhel} && 0%{?rhel} <= 7
%global py2_namespace python
%global with_python3 0
%else
%global py2_namespace python2
%global with_python3 1
%endif


Name:           python-%{pypi_name}
Version:        1.0.0
Release:        3%{?dist}
Summary:        Linux Distribution - a Linux OS platform information API

License:        ASL 2.0
URL:            https://github.com/nir0s/distro
Source0:        https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-setuptools
BuildRequires:  python2-devel

%if 0%{with_python3}
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
%endif

%description
The distro (for: Linux Distribution) package provides information about the
Linux distribution it runs on, such as a reliable machine-readable ID, or
version information.

It is a renewed alternative implementation for Python's original
platform.linux_distribution function, but it also provides much more
functionality. An alternative implementation became necessary because
Python 3.5 deprecated this function, and Python 3.7 is expected to remove it
altogether. Its predecessor function platform.dist was already deprecated since
Python 2.6 and is also expected to be removed in Python 3.7. Still, there are
many cases in which access to that information is needed. See Python issue 1322
for more information.

%package -n     python2-%{pypi_name}
Summary:        Linux Distribution - a Linux OS platform information API
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python-setuptools
Requires:       /usr/bin/lsb_release

%description -n python2-%{pypi_name}
The distro (for: Linux Distribution) package provides information about the
Linux distribution it runs on, such as a reliable machine-readable ID, or
version information.

It is a renewed alternative implementation for Python's original
platform.linux_distribution function, but it also provides much more
functionality. An alternative implementation became necessary because
Python 3.5 deprecated this function, and Python 3.7 is expected to remove it
altogether. Its predecessor function platform.dist was already deprecated since
Python 2.6 and is also expected to be removed in Python 3.7. Still, there are
many cases in which access to that information is needed. See Python issue 1322
for more information.

This package provides python2 module.

%if 0%{with_python3}
%package -n     python3-%{pypi_name}
Summary:        Linux Distribution - a Linux OS platform information API
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3-setuptools
Requires:       /usr/bin/lsb_release

%description -n python3-%{pypi_name}
The distro (for: Linux Distribution) package provides information about the
Linux distribution it runs on, such as a reliable machine-readable ID, or
version information.

It is a renewed alternative implementation for Python's original
platform.linux_distribution function, but it also provides much more
functionality. An alternative implementation became necessary because
Python 3.5 deprecated this function, and Python 3.7 is expected to remove it
altogether. Its predecessor function platform.dist was already deprecated since
Python 2.6 and is also expected to be removed in Python 3.7. Still, there are
many cases in which access to that information is needed. See Python issue 1322
for more information.

This package provides python3 module.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{with_python3}
%py3_build
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if 0%{with_python3}
%py3_install
cp %{buildroot}/%{_bindir}/distro %{buildroot}/%{_bindir}/distro-3
ln -sf %{_bindir}/distro-3 %{buildroot}/%{_bindir}/distro-%{python3_version}
%endif

%py2_install
cp %{buildroot}/%{_bindir}/distro %{buildroot}/%{_bindir}/distro-2
ln -sf %{_bindir}/distro-2 %{buildroot}/%{_bindir}/distro-%{python2_version}

%if 0%{with_python3}
sed -i 's|^#!.\+python$|#!/usr/bin/python3|' %{buildroot}/%{_bindir}/distro
%endif

%files -n python2-%{pypi_name}
%doc README.rst
# not included in tar.gz
# see https://github.com/nir0s/distro/issues/139
#%license LICENSE
%{_bindir}/distro
%{_bindir}/distro-2
%{_bindir}/distro-%{python2_version}

%{python2_sitelib}/%{pypi_name}.py*
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
#%license LICENSE
%{_bindir}/distro-3
%{_bindir}/distro-%{python3_version}
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Wed Oct 05 2016 Miroslav Suchý 1.0.0-3
- python2 subpackages only on rhel
- correct description

* Wed Oct 05 2016 Miroslav Suchý 1.0.0-2
- require lsb_release

* Wed Oct 05 2016 Miroslav Suchý 1.0.0-1
- initial packaging

