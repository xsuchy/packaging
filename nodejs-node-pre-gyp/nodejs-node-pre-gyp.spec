# This macro is needed at the start for building on EL6
%{?nodejs_find_provides_and_requires}

%global enable_tests 0

%global barename node-pre-gyp

Name:               nodejs-node-pre-gyp
Version:            0.6.1
Release:            2%{?dist}
Summary:            Node.js native addon binary install tool

Group:              Development/Libraries
License:            BSD
URL:                https://www.npmjs.org/package/node-pre-gyp
Source0:            http://registry.npmjs.org/%{barename}/-/%{barename}-%{version}.tgz
BuildArch:          noarch
%if 0%{?fedora} >= 19
ExclusiveArch:      %{nodejs_arches} noarch
%else
ExclusiveArch:      %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:      nodejs-packaging >= 6

BuildRequires:      npm(npmlog)
BuildRequires:      npm(semver)
BuildRequires:      npm(tar)
BuildRequires:      npm(request)
BuildRequires:      npm(nopt)
BuildRequires:      npm(mkdirp)
BuildRequires:      npm(rimraf)
BuildRequires:      npm(rc)
BuildRequires:      npm(tar-pack)

Requires:           npm(npmlog)
Requires:           npm(semver)
Requires:           npm(tar)
Requires:           npm(request)
Requires:           npm(nopt)
Requires:           npm(mkdirp)
Requires:           npm(rimraf)
Requires:           npm(rc)
Requires:           npm(tar-pack)

%if 0%{?enable_tests}
BuildRequires:      npm(aws-sdk)
BuildRequires:      npm(mocha)
%endif


%description
node-pre-gyp makes it easy to publish and install Node.js C++ addons from binaries.

node-pre-gyp stands between npm and node-gyp and offers a cross-platform method of binary deployment.

%prep
%setup -q -n package

# Remove bundled node_modules
rm -rf node_modules/

%nodejs_fixdep --caret
%nodejs_fixdep mkdirp
%nodejs_fixdep nopt 
%nodejs_fixdep npmlog
%nodejs_fixdep rimraf
%nodejs_fixdep semver
%nodejs_fixdep tar


%build
%nodejs_symlink_deps --build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/node-pre-gyp
cp -pr package.json lib bin \
    %{buildroot}%{nodejs_sitelib}/node-pre-gyp

mkdir -p %{buildroot}%{_bindir}
ln -s %{nodejs_sitelib}/%{barename}/bin/node-pre-gyp %{buildroot}%{_bindir}/node-pre-gyp

%nodejs_symlink_deps


%check
%if 0%{?enable_tests}
%nodejs_symlink_deps --check
mocha -R spec --timeout 100000
%endif


%files
%doc CHANGELOG.md README.md
%license LICENSE
%{_bindir}/node-pre-gyp
%{nodejs_sitelib}/node-pre-gyp/

%changelog
* Fri Jan 02 2015 Miroslav Suchý <miroslav@suchy.cz> 0.6.1-2
- add symlink to bin/node-pre-gyp

* Thu Jan 01 2015 Miroslav Suchý <miroslav@suchy.cz> 0.6.1-1
- initial packaging

