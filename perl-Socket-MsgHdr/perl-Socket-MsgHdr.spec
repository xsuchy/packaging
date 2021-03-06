%{?perl_default_filter}
%global __requires_exclude MsgHdr.so

Name:           perl-Socket-MsgHdr
Version:        0.04
Release:        3%{?dist}
Summary:        Sendmsg, recvmsg and ancillary data operations
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Socket-MsgHdr/
Source0:        http://www.cpan.org/authors/id/M/MJ/MJP/Socket-MsgHdr-%{version}.tar.gz
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl
BuildRequires:  perl(bytes)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Socket)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Socket::MsgHdr provides advanced socket messaging operations via sendmsg
and recvmsg. Like their C counterparts, these functions accept few
parameters, instead stuffing a lot of information into a complex structure.

%prep
%setup -q -n Socket-MsgHdr-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Socket*
%{_mandir}/man3/*

%changelog
* Fri Jul 19 2013 Miroslav Suchý <msuchy@redhat.com> 0.04-3
- use DESTDIR instead of PERL_INSTALL_ROOT (msuchy@redhat.com)
- add several BRs (msuchy@redhat.com)

* Fri Jul 19 2013 Miroslav Suchý <msuchy@redhat.com> 0.04-2
- exclude MsgHdr.so()(64bit) from provides (msuchy@redhat.com)

* Fri Jul 19 2013 Miroslav Suchy 0.04-1
- Specfile autogenerated by cpanspec 1.78.
