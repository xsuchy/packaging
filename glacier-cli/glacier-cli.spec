%global githash e8a2536

Name:		glacier-cli
Version:	0
Release:	1.20131113git%{githash}%{?dist}
Summary:	Command-line interface to Amazon Glacier

Group:		Applications/Internet
License:	MIT
URL:		https://github.com/basak/glacier-cli
# git clone git@github.com:basak/glacier-cli.git && cd glacier-cli
# git archive --format=tar %{githash} | gzip > %{name}-%{githash}.tar.gz
Source0:	glacier-cli-%{githash}.tar.gz

Requires:	python-boto
Requires:   python-sqlalchemy
# tests
BuildRequires: python-iso8601
BuildRequires: python-mock
BuildRequires: python-nose

%description
This tool provides a sysadmin-friendly command line interface to Amazon
Glacier, turning Glacier into an easy-to-use storage backend. It automates
tasks which would otherwise require a number of separate steps (job submission,
polling for job completion and retrieving the results of jobs). It provides
integration with git-annex, making Glacier even more useful.

%prep
%setup -q


%build
# nothing to do here

%install
mkdir -p %{buildroot}%{_bindir}
cp -a glacier-list-duplicates.sh %{buildroot}%{_bindir}/glacier-list-duplicates
cp -a glacier.sh %{buildroot}%{_bindir}/glacier

%check
nosetests

%files
%doc COPYING README.md
%{_bindir}/glacier-list-duplicates
%{_bindir}/glacier


%changelog

