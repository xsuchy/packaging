Name:           python-ibm-cloud-sdk-core
Version:        3.16.0
Release:        1%{?dist}
Summary:        Core library used by SDKs for IBM Cloud Services

License:        Apache-2.0
URL:            https://github.com/IBM/python-sdk-core
Source0:        %{pypi_source ibm-cloud-sdk-core}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
The python-sdk-core repository contains core functionality required by Python
code generated by the IBM OpenAPI SDK Generator.
}


%description %_description

%package -n     python3-ibm-cloud-sdk-core
Summary:        %{summary}

%description -n python3-ibm-cloud-sdk-core %_description


%prep
%autosetup -p1 -n ibm-cloud-sdk-core-%{version}
echo > requirements-dev.txt

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install


%check
# some tests requires internet connections or credentials
# %%pytest --strict-markers --verbose --tb=long test

%files -n python3-ibm-cloud-sdk-core
%doc README.md
%license LICENSE
%{python3_sitelib}/ibm_cloud_sdk_core
%{python3_sitelib}/ibm_cloud_sdk_core-%{version}.dist-info/
%exclude %{python3_sitelib}/test
%exclude %{python3_sitelib}/test_integration

%changelog
* Wed Nov 30 2022 Miroslav Suchý <msuchy@redhat.com> 3.16.0-1
- rebase to 3.16.0
- use spdx license

* Mon May 23 2022 Miroslav Suchý <msuchy@redhat.com> 3.15.1-2
- do not use dev requirements

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 msuchy <msuchy@redhat.com> - 3.13.2-2
- changed description
- updated license

* Tue Dec 07 2021 msuchy <msuchy@redhat.com> - 3.13.2-1
- Package generated with pyp2spec
