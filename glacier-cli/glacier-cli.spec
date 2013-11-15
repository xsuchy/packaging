%global githash e8a2536

Name:		glacier-cli
Version:	0
Release:	3.20131113git%{githash}%{?dist}
Summary:	Command-line interface to Amazon Glacier

Group:		Applications/Internet
License:	MIT
URL:		https://github.com/basak/glacier-cli
# git clone git@github.com:basak/glacier-cli.git && cd glacier-cli
# git archive --format=tar %{githash} | gzip > %{name}-%{githash}.tar.gz
Source0:	glacier-cli-%{githash}.tar.gz
BuildArch:  noarch

Requires:	python-boto
Requires:   python-sqlalchemy
# tests
BuildRequires: python-iso8601
BuildRequires: python-mock
BuildRequires: python-nose
BuildRequires: python-boto
BuildRequires: python-sqlalchemy

%description
This tool provides a sysadmin-friendly command line interface to Amazon
Glacier, turning Glacier into an easy-to-use storage backend. It automates
tasks which would otherwise require a number of separate steps (job submission,
polling for job completion and retrieving the results of jobs). It provides
integration with git-annex, making Glacier even more useful.

%prep
%setup -q -c


%build
# nothing to do here

%install
mkdir -p %{buildroot}%{_bindir}
cp -a glacier-list-duplicates.sh %{buildroot}%{_bindir}/glacier-list-duplicates
cp -a glacier.py %{buildroot}%{_bindir}/glacier-cli
chmod a+x %{buildroot}%{_bindir}/*

%check
nosetests

%files
%doc COPYING README.md
%{_bindir}/glacier-list-duplicates
%{_bindir}/glacier-cli


%changelog
* Fri Nov 15 2013 Miroslav Suchý <miroslav@suchy.cz> 0-3.20131113gite8a2536
- add executable attr to scripts
- rename glacier binary to glacier
- fix filename
- tar does not contain prefix

* Fri Nov 15 2013 Miroslav Suchý <miroslav@suchy.cz> 0-2.20131113gite8a2536
- initial package


