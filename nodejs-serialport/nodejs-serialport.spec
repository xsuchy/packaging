# This macro is needed at the start for building on EL6
%{?nodejs_find_provides_and_requires}

%global enable_tests 0

%global barename serialport

Name:               nodejs-serialport
Version:            1.4.9
Release:            1%{?dist}
Summary:            Simple interface to the low level serial port

Group:              Development/Libraries
License:            MIT
URL:                https://github.com/voodootikigod/node-serialport
Source0:            http://registry.npmjs.org/%{barename}/-/%{barename}-%{version}.tgz
BuildArch:          noarch
%if 0%{?fedora} >= 19
ExclusiveArch:      %{nodejs_arches} noarch
%else
ExclusiveArch:      %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:      nodejs-packaging >= 6

BuildRequires:      npm(node-pre-gyp)
BuildRequires:      npm(optimist)
BuildRequires:      npm(async)
BuildRequires:      npm(bindings)
BuildRequires:      npm(nan)
BuildRequires:      npm(sf)

Requires:           npm(node-pre-gyp)
Requires:           npm(optimist)
Requires:           npm(async)
Requires:           npm(bindings)
Requires:           npm(nan)
Requires:           npm(sf)

%if 0%{?enable_tests}
BuildRequires:      npm(chai)
BuildRequires:      npm(grunt-contrib-jshint)
BuildRequires:      npm(sandboxed-module)
BuildRequires:      npm(grunt-mocha-test)
BuildRequires:      npm(mocha)
BuildRequires:      npm(sinon-chai)
BuildRequires:      npm(sinon)
BuildRequires:      npm(grunt-cli)
BuildRequires:      npm(grunt)
%endif


%description
Very simple interface to the low level serial port code necessary to program
Arduino chipsets, X10 wireless communications, or even the rising Z-Wave and
Zigbee standards. 

%prep
%setup -q -n package
# Remove bundled node_modules
rm -rf node_modules/

%nodejs_fixdep --caret
%nodejs_fixdep async
%nodejs_fixdep bindings
%nodejs_fixdep node-pre-gyp
%nodejs_fixdep optimist

%build
%nodejs_symlink_deps --build
node-pre-gyp build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/serialport
cp -pr package.json Gruntfile.js serialport.js parsers.js \
    %{buildroot}%{nodejs_sitelib}/serialport

%nodejs_symlink_deps


%check
%if 0%{?enable_tests}
%nodejs_symlink_deps --check
grunt --verbose
%endif


%files
%doc README.md
%license LICENSE
%{nodejs_sitelib}/serialport/

%changelog
* Thu Jan 01 2015 Miroslav Suchý <miroslav@suchy.cz> 1.4.9-1
- initial packaging

