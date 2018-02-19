Name:       imvirt
Summary:    Detects several virtualizations
Version:    0.9.6
Release:    14%{?dist}
URL:        http://micky.ibh.net/~liske/imvirt.html
Source0:    http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
License:    GPLv2+
Group:      Applications/System
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:   dmidecode
BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::MakeMaker)
Buildroot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
ExclusiveArch: %{ix86} x86_64 ia64

%description
This little Perl script tries to detect if it is called from within 
a virtualization container. This is detected by looking for well known boot 
messages, directories and reading DMI (Desktop Management Interface) data.

The following containers are detected:

    * Virtual PC/Virtual Server
    * VirtualBox
    * VMware
    * QEMU/KVM (experimental)
    * Xen (para and non-para virtualized)
    * OpenVZ/Virtuozzo
    * UML
    * any HVM providing CPUID 0x40000000 detection
    * lguest
    * ARAnyM
    * LXC

%prep
%setup -q

%build
%configure --prefix=%{_prefix} --libexec=%{_libexecdir}/imvirt
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/ImVirt/.packlist
rm $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod

%check
#make check

%clean
rm -rf $RPM_BUILD_ROOT
make clean

%files
%defattr(-,root,root,-)
%{_sbindir}/imvirt-report
%{_bindir}/*
%dir %{_libexecdir}/imvirt
%{_libexecdir}/imvirt/*
%doc AUTHORS COPYING ChangeLog README
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{perl_vendorlib}/*

%changelog
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.9.6-11
- Perl 5.26 rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.9.6-9
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.9.6-6
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.9.6-5
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 26 2013 Miroslav Suchý <msuchy@redhat.com> 0.9.6-2
- tar file already contain name-version prefix

* Mon Aug 26 2013 Miroslav Suchý <msuchy@redhat.com> 0.9.6-1
- rebase to 0.9.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.9.5-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Miroslav Suchý <msuchy@redhat.com> - 0.9.5-1
- rebase to 0.9.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.9.4-2
- Perl 5.16 rebuild

* Wed Jun  6 2012 Miroslav Suchý <msuchy@redhat.com> 0.9.4-1
- rebase to 0.9.4 version from upstream

* Mon Feb  6 2012 Miroslav Suchý <msuchy@redhat.com> 0.9.2-2
- rebase to 0.9.2 version from upstream
- add build requires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Dan Horák <dan[at]danny.cz> - 0.9.0-5
- set supported arches

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9.0-4
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9.0-3
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  1 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.0-1
- rebase to 0.9.0 version from upstream

* Wed Mar 24 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.0-0.1.pre1
- change Source0
- preserve timestamp during packaging

* Mon Mar 22 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.0-0.1.pre1
- remove Vendor

* Sat Mar 20 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.0-pre1
- initial release

