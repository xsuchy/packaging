# This macro is needed at the start for building on EL6
%{?nodejs_find_provides_and_requires}



%global barename spark-cli

Name:               spark-cli
Version:            0.4.92
Release:            0%{?dist}
Summary:            Simple commandline application for working with your Spark Cores and using the Spark Cloud

Group:              Development/Libraries
# and/or / execptions? check the license more deeply
License:            LGPLv3 and GPLv3
URL:                https://github.com/spark/spark-cli
Source0:            http://registry.npmjs.org/%{barename}/-/%{barename}-%{version}.tgz
BuildArch:          noarch
%if 0%{?fedora} >= 19
ExclusiveArch:      %{nodejs_arches} noarch
%else
ExclusiveArch:      %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:      nodejs-packaging >= 6

BuildRequires:      npm(moment)
BuildRequires:      npm(xtend)
BuildRequires:      npm(when)
BuildRequires:      npm(glob)
BuildRequires:      npm(request)
BuildRequires:      npm(hogan.js)
BuildRequires:      npm(serialport)

Requires:           npm(moment)
Requires:           npm(xtend)
Requires:           npm(when)
Requires:           npm(glob)
Requires:           npm(request)
Requires:           npm(hogan.js)
Requires:           npm(serialport)


%description
The Spark CLI is a powerful tool for interacting with your Spark cores and
the Spark Cloud.

%prep
%setup -q -n package

%nodejs_fixdep serialport
%nodejs_fixdep request
%nodejs_fixdep hogan.js
%nodejs_fixdep glob

%build
%nodejs_symlink_deps --build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/spark-cli
cp -pr package.json settings.js app.js lib commands bin mappings.json \
    %{buildroot}%{nodejs_sitelib}/spark-cli

mkdir -p %{buildroot}%{_bindir}
ln -s %{nodejs_sitelib}/%{barename}/bin/spark.js %{buildroot}%{_bindir}/spark

%nodejs_symlink_deps

%files
%doc README.md
%{_bindir}/spark
%{nodejs_sitelib}/spark-cli/

%changelog
