# http://fedoraproject.org/wiki/Packaging:Guidelines?rd=Packaging/Guidelines#PIE
%global _hardened_build 1
%global commit 5c320501dc048bbcf56480dfc5780fb43dd20de5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapdate 20210907
%global snapshotrel .%{snapdate}git%{shortcommit}
# To make rpmdev-bumpspec work properly
%global baserelease 1

Name:             obs-signd
Summary:          The OBS sign daemon
License:          GPLv2
URL:              https://github.com/openSUSE/obs-sign
Version:          2.6.1
Release:          1
#Release:          %%{baserelease}%%{?snapshotrel}%%{?dist}
Source0:          https://github.com/openSUSE/obs-sign/archive/refs/tags/obs-sign-%{version}.tar.gz
# We renamed the option in gnupg2 to 'file-is-digest'
Patch0:           0001-Rename-option-files-are-digests-to-file-is-digest.patch
# https://github.com/openSUSE/obs-sign/pull/6
Patch1:           0002-fixes-user-id-matching-to-provide-unique-results.patch
# https://github.com/openSUSE/obs-sign/pull/36
Patch2:           0003-Implement-allow-unprivileged-ports-for-the-client.patch
Requires:         gnupg2
Requires(pre):    shadow-utils
BuildRequires:    perl-generators
BuildRequires:    systemd
BuildRequires:    gcc
BuildRequires:    make

%description
The OpenSUSE Build Service sign client and daemon.

This daemon can be used to sign anything via gpg by communicating
with a remote server to avoid the need to host the private key
on the same server.

%prep
%autosetup -n obs-sign-%{version}

%build
%make_build CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}" sign

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
%attr(4750,root,obsrun) %{_bindir}/sign
%{_sbindir}/signd
%{_unitdir}/signd.service
%doc %{_mandir}/man*/*

%changelog
* Mon Nov 14 2022 Miroslav Suchý <msuchy@redhat.com> 2.6.1-1
- rebase patches
- rebase obs-sign to 2.6.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-4.20210907git5c32050
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
                                                                                          
* Tue May 24 2022 Pavel Raiskup <praiskup@redhat.com> - 2.5.10-3.20210907git5c32050
- implemented 'unprivileged-client-port' option for the OpenShift environments

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-2.20210907git5c32050
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 07 2021 Silvie Chlupova <schlupov@redhat.com> - 2.5.10-1
- rebase to 2.5.10

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-7.20190913git5675e23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.4-6.20190913git5675e23
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-5.20190913git5675e23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec  1 15:23:34 CET 2020 msuchy <msuchy@redhat.com> - 2.5.4-4.20190913git5675e23
- Add make to BR - https://fedoraproject.org/wiki/Changes/Remove_make_from_BuildRoot

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-3.20190913git5675e23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-2.20190913git5675e23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 02 2020 Neal Gompa <ngompa13@gmail.com> - 2.5.4-1.20190913git5675e23
- Rebase to 2.5.4 post-release snapshot
- Drop systemd scriptlet requires per updated packaging policy
- Drop useless verification exception

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.3-2.20190613gitc3d5984
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Jakub Kadlčík <jkadlcik@redhat.com> - 2.5.3-1.20180614gitc3d5984
- update to new upstream version 2.5.3
- use Makefile that is provided by upstream nowadays

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-6.20180614git65f9cab
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-5.20180614git65f9cab
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Miroslav Suchý <msuchy@redhat.com> 2.4.2-4.20180614git65f9cab
- re-add BR gcc

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
