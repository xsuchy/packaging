# Created by pyp2rpm-3.3.7
%global pypi_name ibm-cloud-sdk-core
%global pypi_version %{version}

Name:           python-%{pypi_name}
Version:        3.15.1
Release:        1%{?dist}
Summary:        Core library used by SDKs for IBM Cloud Services

License:        ASL 2.0
URL:            https://github.com/IBM/python-sdk-core
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  (python3dist(codecov) >= 2.1 with python3dist(codecov) < 3)
BuildRequires:  python3dist(coverage) >= 4.5.4
BuildRequires:  (python3dist(pyjwt) >= 2.0.1 with python3dist(pyjwt) < 3)
BuildRequires:  (python3dist(pylint) >= 2.6 with python3dist(pylint) < 3)
BuildRequires:  (python3dist(pytest) >= 6.2.1 with python3dist(pytest) < 7)
BuildRequires:  (python3dist(pytest-cov) >= 2.2.1 with python3dist(pytest-cov) < 3)
BuildRequires:  (python3dist(python-dateutil) >= 2.5.3 with python3dist(python-dateutil) < 3)
BuildRequires:  (python3dist(requests) >= 2.20 with python3dist(requests) < 3)
BuildRequires:  (python3dist(responses) >= 0.12.1 with python3dist(responses) < 1)
BuildRequires:  python3dist(setuptools)
BuildRequires:  (python3dist(tox) >= 3.2 with python3dist(tox) < 4)

%description
This project contains core functionality required by Python code generated by
the IBM Cloud OpenAPI SDK Generator (openapi-sdkgen).

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       (python3dist(pyjwt) >= 2.0.1 with python3dist(pyjwt) < 3)
Requires:       (python3dist(python-dateutil) >= 2.5.3 with python3dist(python-dateutil) < 3)
Requires:       (python3dist(requests) >= 2.20 with python3dist(requests) < 3)
%description -n python3-%{pypi_name}
This project contains core functionality required by Python code generated by
the IBM Cloud OpenAPI SDK Generator (openapi-sdkgen).

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
%{python3_sitelib}/ibm_cloud_sdk_core
%{python3_sitelib}/test
%{python3_sitelib}/test_integration
%{python3_sitelib}/ibm_cloud_sdk_core-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Sun May 22 2022 Miroslav Suchý <msuchy@redhat.com> 3.15.1-1
- rebase to 3.15.1

* Tue Jul 27 2021 Miroslav Suchý <msuchy@redhat.com> 3.10.1-1
- new package
