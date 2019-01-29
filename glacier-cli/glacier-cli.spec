%global githash e8a2536

Name:		glacier-cli
Version:	0
Release:	13.20131113git%{githash}%{?dist}
Summary:	Command-line interface to Amazon Glacier

License:	MIT
URL:		https://github.com/basak/glacier-cli
# git clone git@github.com:basak/glacier-cli.git && cd glacier-cli
# git archive --format=tar %%{githash} | gzip > %%{name}-%%{githash}.tar.gz
Source0:	glacier-cli-%{githash}.tar.gz
BuildArch:  noarch

Requires:	python-boto
Requires:   python-iso8601
Requires:   python-sqlalchemy
%if 0%{?rhel} == 6
Requires:   python-argparse
BuildRequires: python-argparse
%endif
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
sed -i '1s|#!/usr/bin/env python|#!%{__python}|' glacier.py

%install
mkdir -p %{buildroot}%{_bindir}
cp -a glacier-list-duplicates.sh %{buildroot}%{_bindir}/glacier-list-duplicates
cp -a glacier.py %{buildroot}%{_bindir}/glacier-cli
chmod a+x %{buildroot}%{_bindir}/*

%check
%if 0%{?fedora} > 19
#due old python-mock on older fedoras
nosetests
%endif

%files
%doc COPYING README.md
%{_bindir}/glacier-list-duplicates
%{_bindir}/glacier-cli


%changelog
* Fri Sep 02 2016 Miroslav Suchý 0-13.20131113gite8a2536
- correctly require argparse only on rhel6

* Tue Nov 26 2013 Miroslav Suchý <msuchy@redhat.com> 0-8.20131113gite8a2536
- add requires of python-iso8601

* Tue Nov 19 2013 Miroslav Suchý <msuchy@redhat.com> 0-7.20131113gite8a2536
- correct conditon

* Tue Nov 19 2013 Miroslav Suchý <msuchy@redhat.com> 0-6.20131113gite8a2536
- require argparse for el6 and do not run test on F19 due old python-mock

* Tue Nov 19 2013 Miroslav Suchý <msuchy@redhat.com> 0-5.20131113gite8a2536
- 1031019 - replace env with direct python calling
- 1031019 - escape macro in comments

* Fri Nov 15 2013 Miroslav Suchý <miroslav@suchy.cz> 0-4.20131113gite8a2536
- add requires to BR for test

* Fri Nov 15 2013 Miroslav Suchý <miroslav@suchy.cz> 0-3.20131113gite8a2536
- add executable attr to scripts
- rename glacier binary to glacier
- fix filename
- tar does not contain prefix

* Fri Nov 15 2013 Miroslav Suchý <miroslav@suchy.cz> 0-2.20131113gite8a2536
- initial package


