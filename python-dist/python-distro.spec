%global pypi_name distro

Name:           python-%{pypi_name}
Version:        1.0.0
Release:        0%{?dist}
Summary:        Linux Distribution - a Linux OS platform information API

License:        ASL 2.0
URL:            https://github.com/nir0s/distro
Source0:        https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
 
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel

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

%package -n     python3-%{pypi_name}
Summary:        Linux Distribution - a Linux OS platform information API
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3-setuptools
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

This package provides python2 module.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%py3_build

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%py3_install
cp %{buildroot}/%{_bindir}/distro %{buildroot}/%{_bindir}/distro-3
ln -sf %{_bindir}/distro-3 %{buildroot}/%{_bindir}/distro-%{python3_version}

%py2_install
cp %{buildroot}/%{_bindir}/distro %{buildroot}/%{_bindir}/distro-2
ln -sf %{_bindir}/distro-2 %{buildroot}/%{_bindir}/distro-%{python2_version}


%files -n python2-%{pypi_name}
%doc README.rst
# not include in tar.gz
# see https://github.com/nir0s/distro/issues/139
#%license LICENSE
%{_bindir}/distro
%{_bindir}/distro-2
%{_bindir}/distro-%{python2_version}

%{python2_sitelib}/%{pypi_name}.py*
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python3-%{pypi_name}
%doc README.rst
#%license LICENSE
%{_bindir}/distro-3
%{_bindir}/distro-%{python3_version}
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
