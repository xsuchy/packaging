# This macro is needed at the start for building on EL6
%{?nodejs_find_provides_and_requires}

%global enable_tests 0

%global barename serialport

Name:               nodejs-serialport
Version:            1.4.9
Release:            3%{?dist}
Summary:            Simple interface to the low level serial port

Group:              Development/Libraries
License:            MIT
URL:                https://github.com/voodootikigod/node-serialport
Source0:            http://registry.npmjs.org/%{barename}/-/%{barename}-%{version}.tgz
Patch1:             0001-use-static-path.patch
Patch2:             0002-use-nodejs_sitearch.patch
%if 0%{?fedora} >= 19
ExclusiveArch:      %{nodejs_arches} noarch
%else
ExclusiveArch:      %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:      nodejs-packaging >= 6

BuildRequires:      node-gyp
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
%patch1 -p1
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
cp -pr package.json Gruntfile.js serialport.js parsers.js bin \
    %{buildroot}%{nodejs_sitelib}/serialport

mkdir -p %{buildroot}%{nodejs_sitelib}/%{barename}/build/serialport/v1.4.9/Release/node-v11-linux-x64/
cp build/Release/serialport.node %{buildroot}%{nodejs_sitearch}/%{barename}/

mkdir -p %{buildroot}%{_bindir}
ln -s %{nodejs_sitelib}/%{barename}/bin/serialportList.js %{buildroot}%{_bindir}/serialportlist
ln -s %{nodejs_sitelib}/%{barename}/bin/serialportTerminal.js %{buildroot}%{_bindir}/serialportterm

%nodejs_symlink_deps


%check
%if 0%{?enable_tests}
%nodejs_symlink_deps --check
grunt --verbose
%endif


%files
%doc README.md
%license LICENSE
%{_bindir}/*
%{nodejs_sitelib}/%{barename}/
%{nodejs_sitearch}/%{barename}/serialport.node

%changelog
* Sat Jan 03 2015 Miroslav Suchý <miroslav@suchy.cz> 1.4.9-3
- add BR node-gyp

* Fri Jan 02 2015 Miroslav Suchý <miroslav@suchy.cz> 1.4.9-2
- put compiled binary on correct place
- this is binary package
- add bin/* and compiled serialport.node
- use static path
- we really need nan
- add symlink to bin/node-pre-gyp
- update url and license

* Thu Jan 01 2015 Miroslav Suchý <miroslav@suchy.cz> 1.4.9-1
- initial packaging

