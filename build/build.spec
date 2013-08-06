#
# spec file for package build
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%global githash 0ec4e58
%global date    20130806

Name:           build
Summary:        A Script to Build SUSE Linux RPMs
License:        GPL-2.0+ and GPL-2.0
Group:          Development/Tools
Version:        %{date}
Release:        2
#!BuildIgnore:  build-mkbaselibs
URL:            https://github.com/openSUSE/obs-build
# git clone git://github.com/openSUSE/obs-build.git && cd obs-build/
# git archive --format=tar %{githash} --prefix=%{name}-%{version} | gzip > obs-build-%{version}.tar.gz
Source:         obs-build-%{version}.tar.gz
#while this package is noarch, you could not have main package
#noarch and subpackage arch.
#BuildArch:      noarch

# Manual requires to avoid hard require to bash-static
%global __requires_exclude ^/bin/bash-static$
# Keep the following dependencies in sync with obs-worker package
Requires:       bash
Requires:       binutils
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       tar
BuildRequires:  glibc-static
%if 0%{?suse_version} > 1000
# None of them are actually required for core features.
# Perl helper scripts use them.
Recommends:     perl(Date::Language)
Recommends:     perl(Date::Parse)
Recommends:     perl(LWP::UserAgent)
Recommends:     perl(Pod::Usage)
Recommends:     perl(Time::Zone)
Recommends:     perl(URI)
Recommends:     perl(XML::Parser)
Recommends:     bsdtar
Recommends:     qemu-linux-user
%endif

%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}
Requires:       build-mkbaselibs
%endif

%if 0%{?suse_version} > 1120 || 0%{?mdkversion}
Recommends:     build-mkdrpms
%endif

%description
This package provides a script for building RPMs for SUSE Linux in a
chroot environment.


%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}

%package mkbaselibs
Summary:        Tools to generate base lib packages
BuildArch:      noarch
# NOTE: this package must not have dependencies which may break boot strapping (eg. perl modules)

%description mkbaselibs
This package contains the parts which may be installed in the inner build system
for generating base lib packages.

%package mkdrpms
Summary:        Tools to generate delta rpms
BuildArch:      noarch
Requires:       deltarpm
# XXX: we wanted to avoid that but mkdrpms needs Build::Rpm::rpmq
Requires:       build

%description mkdrpms
This package contains the parts which may be installed in the inner build system
for generating delta rpm packages.

%endif

%define initvm_arch %{_host_cpu}
%if %{_host_cpu} == "i686"
%define initvm_arch i586
%endif
%package initvm-%{initvm_arch}
Summary:        Virtualization initializer for emulated cross architecture builds
Requires:       build
BuildRequires:  gcc
BuildRequires:  glibc-devel
Provides:       build-initvm = %{version}
Obsoletes:      build-initvm <= 20130402
%if 0%{?suse_version} > 1200
BuildRequires:  glibc-devel-static
%endif
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:  glibc-static
%endif

%description initvm-%{initvm_arch}
This package provides a script for building RPMs for SUSE Linux in a
chroot or a secure virtualized

%prep
%setup -q -n obs-build-%version

%build
make CFLAGS="%{optflags}" initvm-all

%install
#mkdir -p %{buildroot}%{_libdir}
# initvm
make DESTDIR=%{buildroot} initvm-install
#cp -a %{buildroot}/usr/lib/build %{buildroot}%{_libdir}
#strip %{buildroot}%{_libdir}/build/initvm.*
strip %{buildroot}/usr/lib/build/initvm.*
export NO_BRP_STRIP_DEBUG="true"
chmod 0644 %{buildroot}/usr/lib/build/initvm.*

# main
make DESTDIR=%{buildroot} install
cd %{buildroot}/usr/lib/build/configs/
%if 0%{?suse_version}
%if 0%{?sles_version}
 ln -s sles%{sles_version}.conf default.conf
%else
 V=%suse_version
 ln -s sl${V:0:2}.${V:2:1}.conf default.conf
%endif
test -e default.conf
%endif

%files
%doc README
/usr/bin/build
/usr/bin/buildvc
/usr/bin/unrpm
/usr/lib/build
%exclude /usr/lib/build/emulator/emulator.sh
%config(noreplace) /usr/lib/build/emulator/emulator.sh
%{_mandir}/man1/build.1*
%exclude /usr/lib/build/initvm.*
#%{perl_vendorlib}/Build

%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}
%exclude /usr/lib/build/mkbaselibs
%exclude /usr/lib/build/baselibs*
%exclude /usr/lib/build/mkdrpms

%files mkbaselibs
%defattr(-,root,root)
%dir /usr/lib/build
/usr/lib/build/mkbaselibs
/usr/lib/build/baselibs*

%files mkdrpms
%defattr(-,root,root)
%dir /usr/lib/build
/usr/lib/build/mkdrpms
%endif

%files initvm-%{initvm_arch}
%defattr(-,root,root)
/usr/lib/build/initvm.*

%changelog
* Tue Aug 06 2013 Miroslav Suchý <msuchy@redhat.com> 20130806-2
- swich on autoreqprov and filter out bash-static
- BR glibc-static

* Tue Aug 06 2013 Miroslav Suchý <msuchy@redhat.com> 20130806-1
- specify from where the package is build
- version provides and obsoletes
- no need to specify group several times
- because one subpackage is arch, main package must be arch as well
- list emulator.sh only once

* Fri Aug 02 2013 Miroslav Suchý <msuchy@redhat.com> 20130630-18.2
- initial package for Fedora

* Sun Feb  3 2013 adrian@suse.com
- add generic emulator stub
* Fri Nov  9 2012 adrian@suse.de
- move old initscript_qemu_vm script into own -compat package, to
  be able to use automatic req/prov scripts again
* Fri Sep 28 2012 adrian@suse.de
- run test cases during build
* Fri Jun 29 2012 coolo@suse.com
- fix keep for preinstalled images
* Wed Jun 27 2012 adrian@suse.de
- support preinstall images
* Tue Oct 25 2011 adrian@suse.de
- use github.com as git repo now
- fix build for rpmv5
* Mon Oct 10 2011 mls@suse.de
- add sles11sp2 build config and adapt autodetection [bnc#711770]
* Tue Oct  4 2011 adrian@suse.de
- use new qemu-*-binfmt handler to run commands with correct $0
- fix build for Factory
* Mon Sep 26 2011 adrian@suse.de
- fixing kvm cpuid setting for AMD and Intel CPU's
- support new xen tools
- fixed qemu build initialisation
* Sun Aug  7 2011 opensuse@cboltz.de
- Requires:/Recommends: were part of the package description.
  Moved them to the correct place.
* Fri Jul  1 2011 adrian@suse.de
- compat mode for broken kiwi of openSUSE 11.4
* Thu Jun 30 2011 adrian@suse.de
- fixed kiwi execution call for some versions
* Fri Jun 17 2011 adrian@suse.de
- support new kiwi command line mode
* Mon Jun  6 2011 adrian@suse.de
- do not build ia64 baselibs packages for openSUSE anymore
* Wed May 25 2011 adrian@suse.de
- allow to use simple spec file parser via Build::show
* Thu May 12 2011 adrian@suse.de
- conflict with old bsdtar (not supporting --chroot)
* Wed Apr 27 2011 adrian@suse.de
- revert to single cpu build default for debian packages
* Fri Apr 15 2011 adrian@suse.de
- switch back to single process build for debian to be conform with
  their policy
- use cpuid kvm64 on kvm for 64bit as workaround for a cpuid bug
* Tue Mar 29 2011 lnussel@suse.de
- make sure default.conf is no stale symlink
* Tue Mar  1 2011 adrian@suse.de
- support new cross build initvm. Done by James Perkins from LinuxFoundation
- do not use loop device anymore when using block devices directly
* Thu Nov 11 2010 adrian@suse.de
- workaround for distros with appstart like Ubuntu 10.10
* Tue Nov  2 2010 lnussel@suse.de
- delta size limit 80%%
- actually unlink the delta file if the delta is too big
* Wed Oct 27 2010 lnussel@suse.de
- use '.drpm' suffix instead of '.delta.rpm' for delta rpms
- makedeltarpms -> mkdrpms and also rename subpackage to match
  script name
- since mkdrpms needs Build.pm make perl-TimeDate dependency of
  build optional
* Mon Oct 18 2010 lnussel@suse.de
- add missing optional perl dependencies
* Fri Oct 15 2010 adrian@suse.de
- update to current git
  * export also fallback archs as exclusive archs for kiwi product
    building, fixes factory dvd5 64bit media
  * cross build fixes by Martin Mohring
  * correct disk image file creation, it was one byte too large by James Perkins
* Tue Sep 21 2010 adrian@suse.de
- update to current git
  * workaround for supporting rpm install on cross build with native
    acceleration
* Mon Sep 20 2010 lnussel@suse.de
- package mkdrpms script in separate package
* Tue Aug 24 2010 adrian@suse.de
- update to current git
  * support for mips cross build
* Wed Aug  4 2010 adrian@suse.de
- update to current git
  * replace release number macros with 0 if not specified
* Wed Jul 28 2010 mls@suse.de
- update to current git
  * document --repo and --dist
  * update wiki links
  * fix bugs in repo handling
  * fix distribution autodetection code
* Thu Jul 22 2010 adrian@suse.de
- update to current git
  * support for Files provide
* Thu Jul  8 2010 adrian@suse.de
- update to current git
  * export BUILD_DEBUG so rpmlint can check for it (bnc#618004)
* Tue Jun 29 2010 mls@suse.de
- update to current git
  * add 11.3 config
  * fix repo creation in --noinit case
  * support ovf files directly
  * allow multiple --oldpackages
  * delta rpm support
* Mon Jun 21 2010 adrian@suse.de
- update to current git
  * fixes for image building for SLE 10
  * fix parsing of macros that contain {} blocks
  * support xz decoder helper script
  * don't substitute in lines with %%(), the parser cannot handle it (bnc#613965)
  * run kvm instance with the right number of cpus according to given parallel build jobs
* Sat May 29 2010 adrian@suse.de
- update to current git
  * noatime VM mount
  * _service file rename happens inside of chroot/vm now.
* Tue May  4 2010 adrian@suse.de
- update to current git
  * CBinstall and CBPreninstall directive support from Jan-Simon
* Wed Apr 21 2010 adrian@suse.de
- detect kvm virtio initrds on SUSE systems automatically
* Sun Apr 18 2010 ro@suse.de
- build-mkbaselibs: also move baselibs*conf to subpackage
* Thu Apr 15 2010 ro@suse.de
- add BuildIgnore build-mkbaselibs to be able to bootstrap
* Thu Apr 15 2010 adrian@suse.de
- split out -mkbaselibs package to avoid build dependency problems
  on perl version updates in future.
- update to current git
  * added armv6el to emulator archs by Jan-Simon.
  * fixing a logic error in arch= attribute handling for kiwi
* Fri Apr  9 2010 adrian@suse.de
- update to current git
  * Support for remote yum repos by yi.y.yang@intel.com
  * fixed kiwi file parsing for arch= attributes
* Wed Mar 31 2010 adrian@suse.de
- update to current git
  * kvm autosetup enhancements
  * multiple bugfixes and refactoring
* Wed Mar 10 2010 adrian@suse.de
- update to current git
  * Kiwi exclude arch handling
* Mon Mar  8 2010 adrian@suse.de
- create default.conf symlink to correct *.conf based on
  %%suse_version and %%sles_version macros
* Thu Feb 25 2010 adrian@suse.de
- add dependency to tar (needed for deb builds)
- use current git
  * Added '--uid uid:gid' feature to specify abuild id in chroot
    (by David Greaves)
* Sat Feb 20 2010 adrian@suse.de
- update to current git
  * fix for permissions for debian (done by Jan-Simon)
* Thu Feb 11 2010 adrian@suse.de
- update to current git
  * fixed handling of kiwi build results
* Mon Feb  8 2010 adrian@suse.de
- update to current git
  * support kiwi 4.1 schema files
* Tue Jan 19 2010 adrian@suse.de
- update to current git
  * fixed missing --root parameter for substitutedeps call
* Mon Jan 18 2010 adrian@suse.de
- update to current git
  * create .sha256 files for kiwi image results
* Wed Jan 13 2010 adrian@suse.de
- update to current git repo
  * unbreaking kiwi builds again
* Sun Jan  3 2010 adrian@suse.de
- update to current git repo, update to commit 549cf6c6e148b7f8c05c12ee06f3094cb67149f9
  * minor bugfixes
  * sparc support fixes
* Thu Dec 10 2009 adrian@suse.de
- switch to git repository, update to commit c8b33e430bfb40b80df43249279bd561d874d786
  * product building via abuild user
  * prodoct building speedup
* Fri Nov 27 2009 adrian@suse.de
- update to svn(r9279)
  Debian packages get configured at install time  again now.
  But keeping additional configuration step afterwards for failed
  configutions (due to dep cycles)
* Fri Nov 27 2009 adrian@suse.de
- add requires to perl-TimeDate for changelog2spec app
* Wed Nov 25 2009 adrian@suse.de
- update to svn(r9238)
  * Debian chroot enviroments are running post installation scripts
    now after all packages got installed, not after each installation
    (partly fixes Ubuntu 9.10 setup)
* Sat Nov 21 2009 adrian@suse.de
- update to current svn(r9154)
  * add support for xz compressed rpms (Fedora 12) on platforms without xz support in
    rpm.
  * speed up install by disabling fsync in rpm config
* Thu Nov  5 2009 adrian@suse.de
- update to current svn (r8506)
  - product iso generation is done by kiwi now
  - debs get generated via "make install"
* Wed Sep 23 2009 mls@suse.de
- update to current svn (r8048)
  - support openSUSE 11.2 [bnc#539914]
* Mon Jul 27 2009 ro@suse.de
- update to current svn (r7751)
  - support for legacy releasepkg mechanism
  - only print parse warnings if $config->{'warnings'} is set
  - set warnings for expanddeps/substitutedeps
  - use UTC as default timezone
  - also consider patches as sources
  - do not call depmod until we use also the native kernel,
    it can't match otherwise
  - return with value 3, if basic file system creation fails.
    bs_worker will mark the build host as bad and retries on another one.
  - handle files from service correctly and strip their prefix.
  - - also add rpmv3 compatibility hack to createrpmdeps
  - mount proc filesystem for build compare run
  - fix for ccache support from
  - add build-ids for debuginfo packages for subpacks
* Wed Jun  3 2009 adrian@suse.de
- update to current svn (r7483)
  * Jan-Simons "ChangeTarget" support
  * fix for handling missing self provides with rpm format 3.0.6
* Thu Apr 23 2009 adrian@suse.de
- update to current svn (r7164)
  * package vc tool correctly
  * avoid running fsck on vm instances after 23 build runs
- install files via Makefile instead of manual calls in spec file
* Mon Apr 20 2009 adrian@suse.de
- update to current svn (r7126)
  * new blocklist based build result export
  * Martin Mohrings cross build extensions
  * vc tool included now
* Mon Mar 23 2009 adrian@suse.de
- Fix for "Requires(pre/post)" tags
- fix missing abuild group in /etc/gshadow on debian like distros
* Wed Feb 25 2009 adrian@suse.de
- Update for bug fix for image build with additional packages in --create step
  (fix from cthiel, bnc#479537)
* Fri Feb 20 2009 adrian@suse.de
- Fix kvm support together with Alexander
- Support for new disturl containing a complete pointer to build
  service instance resource
- add support for package compare to allow Build Service to drop
  same packages after build
- image repack support from Christoph
* Tue Jan 27 2009 adrian@suse.de
- update to current buildservice/1.5 branch
- More fixes for kiwi image build
- Move Susetags.pm to correct Build:: namespace
* Wed Dec 10 2008 froh@suse.de
- update to r5853:
- added: new armv7el arch for all binaries for up to ARMv7 EABI with VFP
- Fix kiwi image build support within osc
* Fri Dec  5 2008 froh@suse.de
- remove baselibs.conf from the spec file, too
* Fri Dec  5 2008 ro@suse.de
- delete baselibs.conf (nowadays stored in package sources)
* Wed Dec  3 2008 ro@suse.de
- delete automatic requires for debuginfo-xxbit
* Wed Dec  3 2008 froh@suse.de
- config update
* Fri Nov 28 2008 froh@suse.de
- many kiwi fixes
- _no_ cross build support yet
* Thu Nov 13 2008 ro@suse.de
- update mkbaselibs broken by previous debuginfo change
- various fixes for kiwi build
- add sl11.1.conf
- add support for --disturl
- also save .desktopfiles for coolo
* Thu Oct 23 2008 ro@suse.de
- disable ppc:ia32 stuff again, causes trouble and can not work
* Tue Oct 21 2008 jblunck@suse.de
- Generate debuginfo packages for baselibs (bnc #396196)
* Mon Oct 20 2008 ro@suse.de
- update to svn trunk of today:
- init_buildsystem: check for some left space before calling rpmbuild
  - create dev/shm as directory
- baselibs_global.conf: update to current internal revision
  - add ia32 stuff for x86 binaries on ppc
  - add ldconfig for all non-devel baselibs packages
- changed: to function also with emulators better use fakeroot-tcp
  for debian build
- fixed: changed basis for memory calculation to assume also a stack
  which can be swapped well. gcc often needs much memory here
- recognize SLES10
- fix boolification in && and ||
- re-preinstall critical packages on update
- fix creation of buildenv to do it the same time with and without VM.
- fixes installation-images build for ppc
- fixed #406596: don't ignore BuildRequires in subpackages
- print finished message
- set BUILD_USER depending on the suse_version like it is done in
  old autobuild
- added documentation for specfile control comments for build(1)
- add --incarnation
- add --create-build-binaries
- support badarch (aka excludearch)
- add support for Requires(pre) or (post) semantic
* Mon Aug 11 2008 adrian@suse.de
  Update from current svn trunk:
- Improved XEN support (XEN call only once per build)
- Add post build check hooks
- rpmlint support
- added kvm support
- refactored code in various places
* Tue Jun  3 2008 mls@suse.de
- fix debtransform bug [bnc#396766]
* Thu May 29 2008 mls@suse.de
- add 11.0 config
- fix debian provides
- fix rpm tag parsing
- add with/without/define/ccache/icecream/debug options
- update mkbaselibs
* Fri Sep 14 2007 mls@suse.de
- add sl10.3 config [#310089]
- also look for BuildRequires in subpackage definitions [#305568]
- allow removal of more config parameters
* Thu Aug  2 2007 mls@suse.de
- support 'order' config option
- support 'patterntype' config option
- new setdeps() method
- support for flexible query options
- support 'description' query
- fix bug in changelog2spec time cutoff
- make debtransform understand Debtransform-Tar/Debtransform-Files-Tar/
  Debtransform-Series
- fix bug in substitutedeps
* Wed Jun 13 2007 mls@suse.de
- implement rpm installation order calculation in perl
- make substitute code modify requires, too
- add filelist query support
- add prereq parsing support
- speed up version comparison a bit
* Thu May 10 2007 mls@suse.de
- add _vendor to configs
- fix deban dependency compare
- allow not operator in configs
- fix build from source rpms
* Thu Apr 12 2007 mls@suse.de
- add --root to rpm call in rpm to work around a bug in rpm [#255720]
* Thu Apr  5 2007 mls@suse.de
- update to 1561:
  * support architecture dependand requires in dsc files
  * support "global" definitions for rpm
  * support vminstall config option
* Mon Mar 12 2007 mls@suse.de
- update to r1419:
  * fix buildroot in debtransform
  * obey version numbers when expanding
* Fri Mar  2 2007 mls@suse.de
- transform suse changes file to rpm specfile format
- improved debian support
* Fri Jan 26 2007 poeml@suse.de
- update to r1114:
  - re-add the lost unrpm script
* Fri Jan 26 2007 poeml@suse.de
- update to r1110:
  - make exclarch an array
  - remount root rw in xen case, needed if root is not reiserfs
  - add repotype/runscripts options
  - remove devs in sl10.1/10.2
  - fix boolean test to make "00" false like rpm does
  - add rpm_verscmp for version comparison
  - runscripts
  - macro blocks
  - read_config_dist
  - useful xen exit status
  - add --kill
  - update 10.2 config
  - extend spec/dsc parser
  - fixed two bugs in the specfile parser
* Fri Nov 24 2006 mls@suse.de
- fix suse_version in sl10.1/sles10 config
- add sl10.2 config
- make dist autodetection work with opensuse
- fix macro sequencing and expression parser bugs
- treat preinstalls as keep
* Wed Aug 23 2006 ro@suse.de
- init_buildsystem: when preinstalling, handle only sh scripts
* Wed Jun 14 2006 mls@suse.de
- support for buildservice and debian packages
* Fri Apr 28 2006 mls@suse.de
- add ndeps back to expansion calls
- save original macro name so that other regexp calls don't destroy
  it
* Wed Apr 19 2006 mls@suse.de
- add --list-state option [#119869]
- suppress stat messages when deleting rpms [#154385]
- delete not-ready flag when rpm expansion failes [#133568]
- update baselibs.conf
* Tue Apr 11 2006 mls@suse.de
- fix typo in configs
- fix macro handling
* Fri Apr  7 2006 mls@suse.de
- mkbaselibs: do not leave .src.rpm in the release [#158816]
* Tue Apr  4 2006 mls@suse.de
- add update-alternatives to java2-devel-packages macro [#156137]
* Mon Mar 27 2006 mls@suse.de
- run zic to set default timezone [#142363]
- update baselibs.conf
* Fri Mar 24 2006 mls@suse.de
- fix handling of "keep" [#160346]
- fix old configs [#159947]
* Mon Mar 20 2006 mls@suse.de
- make mkbaselibs use the right version for the srcrpm
- update mkbaselibs configuration files
* Fri Mar 10 2006 mls@suse.de
- add package expansion and dependency substitution support
* Wed Feb  8 2006 agruen@suse.de
- Adjust the package lists so that the build script can at least
  be used again.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Sep 12 2005 mls@suse.de
- also search for ix86 packages when building x86_64 [#116069]
* Mon Sep  5 2005 mls@suse.de
- add --baselibs option
- fix --extra-packs
* Thu May 12 2005 mls@suse.de
- Fix typo in init_buildsystem that prevented the reuse of the build
  environment [#74714]
* Fri Mar 11 2005 mls@suse.de
- integrated patches into tarball
- allowed build for older dists [#65506]
* Wed Mar  2 2005 agruen@suse.de
- Some more cleanups for 9.3.
- When using the default list of packages, also try to include the
  packages in neededforbuild.
* Mon Feb 28 2005 agruen@suse.de
- ldconfig must be called with its absolute path.
* Tue May 25 2004 mls@suse.de
- overhaul the manpage
* Thu Mar 25 2004 mls@suse.de
- incorporate ro's diff
* Wed Mar 24 2004 mls@suse.de
- really adapt to 9.1
- add --root and --extra-packs options
- use BuildRequires: line
- use user 'abuild' if norootforbuild found
- fix BUILD_DIR security issue (#35281)
* Thu Mar 11 2004 ro@suse.de
- adapted for 9.1
* Mon Nov 10 2003 mmj@suse.de
- Accept "-h" for help
- rpm -ba is now rpmbuild -ba
- Add Maximum RPM reference
* Mon Nov 10 2003 mmj@suse.de
- Update the default USEDFORBUILD to match todays packages
- Don't build as root
* Wed Oct 15 2003 mmj@suse.de
- Fix to work on amd64 (from mls) [#32229]
* Fri Sep  5 2003 mls@suse.de
- select i586 on i686 is user didn't specify arch
- complain if user wan't to build i686 on a not-i686 processor
- patch rpmrc so that i686 rpms are written if building for i686
* Thu Sep  4 2003 mls@suse.de
- port to sl90
- allow path for BUILD_RPMS
- add BUILD_ARCH and autodetection
- add --jobs and --target options
* Fri Aug 29 2003 nashif@suse.de
- fixed call for "head"
* Thu Aug  7 2003 schwab@suse.de
- Fix typo.
* Thu Aug  7 2003 mmj@suse.de
- Enhance build.1 a bit
* Sat Mar  8 2003 kukuk@suse.de
- Fix build on 8.2 (coreutils) [Bug #24895]
* Fri Jan 31 2003 kukuk@suse.de
- Fix build patch from bk.
* Wed Jan 29 2003 kukuk@suse.de
- Add workaround for duplicate packages for different archs
- Add support for upcoming 8.2
* Fri Oct  4 2002 bk@suse.de
- integrate 8.1 diff into tarball and update README
- build.dif: init_buildsystem: add support for earlyer distributions
* Mon Sep  9 2002 mls@suse.de
- Adjust for SuSE Linux 8.1 again
- Fix parameter parsing
- Changed build to accept .src.rpm sources
* Mon Aug 19 2002 kukuk@suse.de
- Adjust for SuSE Linux 8.1
* Tue Jul 30 2002 kukuk@suse.de
- Fix get_version_number.sh
* Thu Jul 18 2002 kukuk@suse.de
- Don't create /etc/rc.config
* Wed Jul  3 2002 kukuk@suse.de
- Add default package list for new spec files without usedforbuild
- Make it work with gcc 2.95 and gcc 3.1
* Thu Mar  7 2002 kukuk@suse.de
- Fix build/init_buildsystem
* Mon Jan 14 2002 kukuk@suse.de
- Add manual page from Gerd Knorr
* Fri Dec 14 2001 kukuk@suse.de
- Fix file list
- Ignore new RPMs from pre-8.0 on 7.3
* Fri Dec 14 2001 kukuk@suse.de
- More fixes
* Tue Nov 27 2001 kukuk@suse.de
- New build script which uses "usedforbuild"
* Thu Jan 18 2001 kukuk@suse.de
- Update Readme and init_buildsystem for 7.1
* Thu Nov 30 2000 kukuk@suse.de
- Update init_buildsystem, add README
* Wed Nov 15 2000 kukuk@suse.de
- First version
