# http://fedoraproject.org/wiki/Packaging:Guidelines?rd=Packaging/Guidelines#PIE
%global _hardened_build 1
%global commit 65f9cab3937822234e214e4ed5442db73f640f0c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapdate 20180614
%global snapshotrel .%{snapdate}git%{shortcommit}

Name:             obs-signd
Summary:          The OBS sign daemon
License:          GPLv2
Url:              https://github.com/openSUSE/obs-sign
Version:          2.4.2
Release:          3%{?snapshotrel}%{?dist}
Source0:          https://github.com/openSUSE/obs-sign/archive/%{commit}/obs-sign-%{shortcommit}.tar.gz
# We renamed the option in gnupg2 to 'file-is-digest'
Patch0:           0001-Rename-option-files-are-digests-to-file-is-digest.patch
# https://github.com/openSUSE/obs-sign/pull/6
Patch1:			  0002-fixes-user-id-matching-to-provide-unique-results.patch
Requires:         gnupg2
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils
BuildRequires:    perl-generators
BuildRequires:    systemd

%description
The OpenSUSE Build Service sign client and daemon.

This daemon can be used to sign anything via gpg by communicating
with a remote server to avoid the need to host the private key
on the same server.

%prep
%autosetup -n obs-sign-%{commit}

%build
gcc %{optflags} -fPIC -pie -o sign sign.c

%install
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_sysconfdir}
install -d -m 0755 %{buildroot}%{_bindir}

# binaries and configuration
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_bindir} %{buildroot}%{_sysconfdir}
install -m 0755 signd %{buildroot}%{_sbindir}
install -m 0750 sign %{buildroot}%{_bindir}
install -m 0644 sign.conf %{buildroot}%{_sysconfdir}

# systemd service
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 dist/signd.service %{buildroot}%{_unitdir}

# man pages
install -d -m 0755 %{buildroot}%{_mandir}/man{5,8}

for f in 5 8; do
  install -m 0644 sig*.${f} %{buildroot}%{_mandir}/man${f}/
done

%pre
getent group obsrun >/dev/null || %{_sbindir}/groupadd -r obsrun
getent passwd obsrun >/dev/null || \
  %{_sbindir}/useradd -r -s /bin/false -c "User for Open Build Service backend" \
                         -d %{_libdir}/obs -g obsrun obsrun
exit 0

%post
%systemd_post signd.service

%preun
%systemd_preun signd.service

%postun
%systemd_postun_with_restart signd.service

%files
%config(noreplace) %{_sysconfdir}/sign.conf
%verify(not mode) %attr(4750,root,obsrun) %{_bindir}/sign
%{_sbindir}/signd
%{_unitdir}/signd.service
%doc %{_mandir}/man*/*

%changelog
* Thu Jun 21 2018 Miroslav Suchý <msuchy@redhat.com> 2.4.2-3.20180614git65f9cab
- update to snapshot of 20180614

* Thu Jun 21 2018 Miroslav Suchý <msuchy@redhat.com>
- rebase patches
- update to snapshot of 20180614

* Tue May 22 2018 Miroslav Suchý <msuchy@redhat.com> 2.4.2-1
- rebase to 2.4.2

* Mon Feb 19 2018 Miroslav Suchý <msuchy@redhat.com> 2.2.1-14
- fix broken build 

* Mon Feb 19 2018 Miroslav Suchý <msuchy@redhat.com> 2.2.1-13
- BR gcc
- require shadow-utils because of adding user

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Apr 26 2016 Miroslav Suchy <msuchy@redhat.com> - 2.2.1-8
- fix id matching (Patch1)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 03 2014 Josef Stribny <jstribny@redhat.com> - 2.2.1-5
- Add install section to unit file

* Tue Aug 26 2014 Josef Stribny <jstribny@redhat.com> - 2.2.1-4
- Enable Position-independent code (PIC)

* Mon Aug 25 2014 Josef Stribny <jstribny@redhat.com> - 2.2.1-3
- Create group or user only if it doesn't exist yet
- Remove explicit gzip of man pages

* Fri Aug 22 2014 Josef Stribny <jstribny@redhat.com> - 2.2.1-2
- Use macros where possible

* Fri May 23 2014 Josef Stribny <jstribny@redhat.com> 2.2.1-1
- Initial package
