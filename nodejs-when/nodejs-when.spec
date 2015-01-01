# This macro is needed at the start for building on EL6
%{?nodejs_find_provides_and_requires}

%global enable_tests 0

%global barename when

Name:               nodejs-when
Version:            3.6.4
Release:            0%{?dist}
Summary:            A lightweight Promises/A+ and when() implementation, plus other async goodies

Group:              Development/Libraries
License:            MIT
URL:                https://github.com/cujojs/when
Source0:            http://registry.npmjs.org/%{barename}/-/%{barename}-%{version}.tgz
BuildArch:          noarch
%if 0%{?fedora} >= 19
ExclusiveArch:      %{nodejs_arches} noarch
%else
ExclusiveArch:      %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:      nodejs-packaging >= 6



%if 0%{?enable_tests}
BuildRequires:      npm(wd)
BuildRequires:      npm(buster)
BuildRequires:      npm(benchmark)
BuildRequires:      npm(promises-aplus-tests)
BuildRequires:      npm(rest)
BuildRequires:      npm(json5)
BuildRequires:      npm(sauce-connect-launcher)
BuildRequires:      npm(jshint)
BuildRequires:      npm(poly)
BuildRequires:      npm(microtime)
BuildRequires:      npm(optimist)
BuildRequires:      npm(browserify)
%endif


%description
When.js is a rock solid, battle-tested Promises/A+ and when() implementation,
including a complete ES6 Promise shim. It's a powerful combination of small
size, high performance, debuggability, and rich features:

 Resolve arrays and hashes of promises, as well as infinite promise sequences
 Execute tasks in parallel or sequentially
 Transform Node-style and other callback-based APIs into promise-based APIs

When.js is one of the many stand-alone components of cujoJS, the JavaScript
Architectural Toolkit. 

%prep
%setup -q -n package

%nodejs_fixdep --caret

%build
%nodejs_symlink_deps --build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/when
cp -pr package.json cancelable.js pipeline.js lib keys.js delay.js function.js unfold.js when.js poll.js timeout.js monitor.js node.js sequence.js parallel.js generator.js callbacks.js guard.js \
monitor es6-shim unfold node \
    %{buildroot}%{nodejs_sitelib}/when

%nodejs_symlink_deps


%check
%if 0%{?enable_tests}
%nodejs_symlink_deps --check
jshint . && buster-test -e node && promises-aplus-tests test/promises-aplus-adapter.js
%endif


%files
%doc README.md
%{nodejs_sitelib}/when/

%changelog
