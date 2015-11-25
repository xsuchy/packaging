Name:           perl-Schedule-Cron-Events
Version:        1.94
Release:        0%{?dist}
Summary:        Take a line from a crontab and find out when events will occur
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Schedule-Cron-Events/
# http://www.cpan.org/modules/by-module/Schedule/Schedule-Cron-Events-%{version}.tar.gz
# is the original upstream source. Unfortunately Schedule-Cron-Events includes the file
# cron_event_predict.plx - being not covered by any of the license statements inside of
# the upstream tarball. And per Fedora Legal, we have to remove this file once upstream
# has clarified the licensing of this file. Cleaning sources can be simply done using:
#   tar zxvf Schedule-Cron-Events-<version>.tar.gz
#   rm Schedule-Cron-Events-<version>/cron_event_predict.plx
#   comment out some lines in Schedule-Cron-Events-1.93/Makefile.PL
#   tar cvfz Schedule-Cron-Events-<version>-noplx.tar.gz Schedule-Cron-Events-<version>
Source0:        Schedule-Cron-Events-%{version}-noplx.tar.gz
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(Carp)
BuildRequires:  perl(Set::Crontab)
BuildRequires:  perl(Time::Local)
# Tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Given a line from a crontab, tells you the time at which cron will next run
the line, or when the last event occurred, relative to any date you choose.
The object keeps that reference date internally, and updates it when you
call nextEvent() or previousEvent() - such that successive calls will give
you a sequence of events going forward, or backwards, in time.

%prep
%setup -q -n Schedule-Cron-Events-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jun 18 2015 Miroslav Suchy <msuchy@redhat.com> 1.93-1
- rebase to 1.93

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.8-32
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.8-31
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.8-28
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.8-25
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.8-23
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.8-21
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.8-20
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.8-19
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Robert Scheck <robert@fedoraproject.org> 1.8-16
- removed not clearly licensed *.plx file (#483390 #c11)

* Thu Sep 11 2008 Miroslav Suchý <msuchy@redhat.com> 1.8-15
- add build requires ExtUtils::MakeMaker

* Wed Sep 10 2008 Miroslav Suchý <msuchy@redhat.com> 1.8-14
- fix mixed tab and space

* Thu Sep  4 2008 Miroslav Suchý <msuchy@redhat.com> 1.8-12
- add build requires

* Fri Aug 29 2008 Miroslav Suchý <msuchy@redhat.com> 1.8-2
- Specfile autogenerated by cpanspec 1.77.
