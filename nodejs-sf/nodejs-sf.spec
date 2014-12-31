%global npmname sf
%{?nodejs_find_provides_and_requires}

Name:           nodejs-%{npmname}
Version:        0.1.7
Release:        1%{?dist}
Summary:        String formatting library for node.js

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/joeferner/node-sf
Source0:        http://registry.npmjs.org/%{npmname}/-/%{npmname}-%{version}.tgz

BuildRequires:  nodeunit
BuildRequires:  nodejs-packaging
#needed for test, not packaged yet
#BuildRequires:  nodejs-timezone-js

BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches} noarch

%description
String formatting library for node.js.


%prep
%setup -q -n package


%build
#nothing to do

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npmname}
cp -a package.json sf.js %{buildroot}%{nodejs_sitelib}/%{npmname}
%nodejs_symlink_deps

%check
#nodeunit test

%files
%doc README.md
%{nodejs_sitelib}/%{npmname}


%changelog
* Wed Dec 31 2014 Miroslav Suchý <msuchy@redhat.com> - 0.1.7-1
- Initial packaging
