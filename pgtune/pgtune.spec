%global githash da57e00
Summary:	PostgreSQL Config Tuner
Name:		pgtune
Version:	0.9.3
Release:	9.%{githash}%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgfoundry.org/projects/pgtune
#Source0:	http://pgfoundry.org/frs/download.php/2449/%{name}-%{version}.tar.gz
# Created using:
# git archive --format=tar --prefix=pgtune-0.9.3/ -o pgtune-0.9.3.tar.gz %{githash}:./
Source:		%{name}-%{version}.tar.gz
Source1:    pgtune.8.asciidoc
Patch0:		pgtune-settingsdir.patch
Requires:	postgresql-server
BuildRequires: asciidoc
BuildRequires: libxslt
Buildarch:	noarch

%description
pgtune takes the wimpy default postgresql.conf and expands the database server
to be as powerful as the hardware it's being deployed on.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0
cp %{SOURCE1} .

%build
a2x -d manpage -f manpage pgtune.8.asciidoc

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/%{name}

install -m 755 pgtune %{buildroot}%{_bindir}
install -m 644 -p pg_settings* %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}/%{_mandir}/man8
install -m 644 pgtune.8 %{buildroot}/%{_mandir}/man8

%clean

%files
%doc TODO COPYRIGHT
%doc %{_mandir}/man8/pgtune.8*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%attr(755,root,root) %{_bindir}/pgtune

%changelog
* Thu Nov 06 2014 Miroslav Suchý <msuchy@redhat.com> 0.9.3-9.da57e00
- add missing source

* Thu Nov 06 2014 Miroslav Suchý <msuchy@redhat.com> 0.9.3-8.da57e00
- include pg 9.x configs

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar  6 2012 Miroslav Suchy <msuchy@redhat.com> 0.9.3-3
- 797930 - change email of Gunduz in changelog

* Mon Feb 27 2012 Miroslav Suchy <msuchy@redhat.com> 0.9.3-2
- package for Fedora
- add man page

* Wed Oct 28 2009 Devrim Gunduz <devrim@gunduz.com> 0.9.1-1
- Initial packaging for PostgreSQL RPM Repository

* Wed Oct 28 2009 Greg Smith <gsmith@gregsmith.com> 0.9.2-1
- Added copyright file, doesn't install sample postgresql.conf file.
