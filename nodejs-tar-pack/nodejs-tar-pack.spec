# This macro is needed at the start for building on EL6
%{?nodejs_find_provides_and_requires}

%global enable_tests 0

%global barename tar-pack

Name:               nodejs-tar-pack
Version:            2.0.0
Release:            2%{?dist}
Summary:            Package and un-package modules of some sort (in tar/gz bundles)

Group:              Development/Libraries
License:            BSD
URL:                https://www.npmjs.org/package/tar-pack
Source0:            http://registry.npmjs.org/%{barename}/-/%{barename}-%{version}.tgz
BuildArch:          noarch
%if 0%{?fedora} >= 19
ExclusiveArch:      %{nodejs_arches} noarch
%else
ExclusiveArch:      %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:      nodejs-packaging >= 6

BuildRequires:      npm(tar)
BuildRequires:      npm(fstream)
BuildRequires:      npm(graceful-fs)
BuildRequires:      npm(fstream-ignore)
BuildRequires:      npm(uid-number)
BuildRequires:      npm(rimraf)
BuildRequires:      npm(readable-stream)
BuildRequires:      npm(debug)
BuildRequires:      npm(once)

Requires:           npm(tar)
Requires:           npm(fstream)
Requires:           npm(graceful-fs)
Requires:           npm(fstream-ignore)
Requires:           npm(uid-number)
Requires:           npm(rimraf)
Requires:           npm(readable-stream)
Requires:           npm(debug)
Requires:           npm(once)

%if 0%{?enable_tests}
BuildRequires:      npm(mocha)
BuildRequires:      npm(mkdirp)
BuildRequires:      npm(rfile)
%endif


%description
Package and un-package modules of some sort (in tar/gz bundles).  This is
mostly useful for package managers.  Note that it doesn't check for or
touch `package.json` so it can be used even if that's not the way you store
your package info.

%prep
%setup -q -n package
%nodejs_fixdep --caret

%build
%nodejs_symlink_deps --build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/tar-pack
cp -pr package.json index.js \
    %{buildroot}%{nodejs_sitelib}/tar-pack

%nodejs_symlink_deps


%check
%if 0%{?enable_tests}
%nodejs_symlink_deps --check
mocha -R list
%endif


%files
%doc README.md
%{nodejs_sitelib}/tar-pack/

%changelog
* Thu Jan 01 2015 Miroslav Suchý <miroslav@suchy.cz> 2.0.0-2
- initial packaging

