%global pypi_name simplekv
# python3 does not work in this version yet 
%global with_python3 0

Name:           python-%{pypi_name}
Version:        0.9.2
Release:        0%{?dist}
Summary:        A key-value storage for binary data, support many backends

License:        MIT
URL:            http://github.com/mbr/simplekv
Source0:        https://pypi.python.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-devel
 
%if %{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3
 
Requires:       python-six

%description
simplekv is an API for very basic key-value stores used for small, frequently
accessed data or large binary blobs. Its basic interface is easy to implement
and it supports a number of backends, including the filesystem, SQLAlchemy,
MongoDB, Redis and Amazon S3/Google Storage.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        A key-value storage for binary data, support many backends
 
Requires:       python3-six

%description -n python3-%{pypi_name}
simplekv is an API for very basic key-value stores used for small, frequently
accessed data or large binary blobs. Its basic interface is easy to implement
and it supports a number of backends, including the filesystem, SQLAlchemy,
MongoDB, Redis and Amazon S3/Google Storage.

This package include python3 library.
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



%files
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3


%changelog
