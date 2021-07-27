%global pypi_name ibm-vpc
%global pypi_version %{version}

Name:           python-%{pypi_name}
Version:        0.7.0
Release:        0%{?dist}
Summary:        Python client library for IBM Cloud VPC Services

License:        ASL 2.0
URL:            https://github.com/IBM/vpc-python-sdk
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  (python3dist(codecov) >= 2.1 with python3dist(codecov) < 3)
BuildRequires:  python3dist(coverage) >= 4.5.4
BuildRequires:  python3dist(ibm-cloud-sdk-core) >= 3.10
BuildRequires:  (python3dist(pylint) >= 2.6 with python3dist(pylint) < 3)
BuildRequires:  (python3dist(pytest) >= 6.2.1 with python3dist(pytest) < 7)
BuildRequires:  (python3dist(pytest-cov) >= 2.2.1 with python3dist(pytest-cov) < 3)
BuildRequires:  python3dist(pytest-rerunfailures) >= 3.1
BuildRequires:  (python3dist(python-dateutil) >= 2.5.3 with python3dist(python-dateutil) < 3)
BuildRequires:  (python3dist(responses) >= 0.12.1 with python3dist(responses) < 1)
BuildRequires:  python3dist(setuptools)
BuildRequires:  (python3dist(tox) >= 3.2 with python3dist(tox) < 4)

%description
[![Build Status]( [![License]( [![semantic-release]( IBM Cloud Virtual Private
Cloud (VPC) Python SDK Version 0.7.0Python client library to interact with
various [IBM Cloud Virtual Private Cloud (VPC) Service APIs]( SDK uses
[Semantic Versioning](), and as such there may be backward-incompatible changes
for any new 0.y.z version.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3dist(ibm-cloud-sdk-core) >= 3.10
Requires:       (python3dist(python-dateutil) >= 2.5.3 with python3dist(python-dateutil) < 3)
%description -n python3-%{pypi_name}
[![Build Status]( [![License]( [![semantic-release]( IBM Cloud Virtual Private
Cloud (VPC) Python SDK Version 0.7.0Python client library to interact with
various [IBM Cloud Virtual Private Cloud (VPC) Service APIs]( SDK uses
[Semantic Versioning](), and as such there may be backward-incompatible changes
for any new 0.y.z version.


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/ibm_vpc
%{python3_sitelib}/ibm_vpc-%{pypi_version}-py%{python3_version}.egg-info

%changelog

