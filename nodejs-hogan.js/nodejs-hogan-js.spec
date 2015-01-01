# This macro is needed at the start for building on EL6
%{?nodejs_find_provides_and_requires}

%global barename hogan.js

Name:               nodejs-hogan-js
Version:            3.0.2
Release:            0%{?dist}
Summary:            Compiler for the Mustache templating language

Group:              Development/Libraries
License:            ASL 2.0
URL:                https://www.npmjs.org/package/hogan.js
Source0:            http://registry.npmjs.org/%{barename}/-/%{barename}-%{version}.tgz
BuildArch:          noarch
%if 0%{?fedora} >= 19
ExclusiveArch:      %{nodejs_arches} noarch
%else
ExclusiveArch:      %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:      nodejs-packaging >= 6

BuildRequires:      npm(nopt)
BuildRequires:      npm(mkdirp)

Requires:           npm(nopt)
Requires:           npm(mkdirp)


%description
Hogan.js is a compiler for the Mustache templating language.

Hogan.js was written to meet three templating library requirements: good
performance, standalone template objects, and a parser API.

%prep
%setup -q -n package

%nodejs_fixdep --caret
%nodejs_fixdep nopt

%build
%nodejs_symlink_deps --build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/hogan.js
cp -pr package.json inheritance.js test.js lib \
    %{buildroot}%{nodejs_sitelib}/hogan.js

%nodejs_symlink_deps



%files
%doc README.md
%license LICENSE
%{nodejs_sitelib}/hogan.js/

%changelog
