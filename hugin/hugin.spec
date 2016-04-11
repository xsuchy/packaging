%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
Summary: A panoramic photo stitcher and more
Name: hugin
Version: 2016.0.0
Release: 0%{?dist}
License: GPLv2+
Group: Applications/Multimedia
Source: http://downloads.sourceforge.net/hugin/%{name}-%{version}.tar.bz2
URL: http://hugin.sourceforge.net/
Requires: shared-mime-info
Requires: webclient
Requires: wxPython
Requires: %{name}-base = %{version}-%{release}
BuildRequires: libpano13-devel >= 2.9.19 zlib-devel libtiff-devel libjpeg-devel
BuildRequires: libpng-devel gettext-devel wxGTK-devel >= 2.7.0 boost-devel freeglut-devel
BuildRequires: cmake desktop-file-utils OpenEXR-devel exiv2-devel glew-devel
BuildRequires: python-devel swig flann-devel perl-Image-ExifTool >= 9.09
BuildRequires: mesa-libGLU-devel libXmu-devel sqlite-devel vigra-devel >= 1.9.0
BuildRequires: perl-podlators fftw-devel

%description
hugin can be used to stitch multiple images together. The resulting image can
span 360 degrees. Another common use is the creation of very high resolution
pictures by combining multiple images. It uses the Panorama Tools as back-end
to create high quality images

%package base
Summary: Command-line tools and libraries required by hugin
Group: Applications/Multimedia
Requires: enblend >= 3.2 perl-Image-ExifTool >= 9.09

%description base
Command-line tools used to generate panoramic images, install this package
separately from hugin if you want to batch-process hugin projects on a machine
without a GUI environment.

%prep
%setup -q

%build
%cmake . -DBUILD_HSI=1
make VERBOSE=1 %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

desktop-file-install --vendor="" --delete-original \
  --dir=%{buildroot}/%{_datadir}/applications \
  %{buildroot}/%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" --delete-original \
  --dir=%{buildroot}/%{_datadir}/applications \
  %{buildroot}/%{_datadir}/applications/PTBatcherGUI.desktop
desktop-file-install --vendor="" --delete-original \
  --dir=%{buildroot}/%{_datadir}/applications \
  %{buildroot}/%{_datadir}/applications/pto_gen.desktop
%find_lang %{name}

# Merge applications into one software center item
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/calibrate_lens_gui.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<component type="desktop">
  <metadata_license>CC0-1.0</metadata_license>
  <id>calibrate_lens_gui.desktop</id>
  <metadata>
    <value key="X-Merge-With-Parent">hugin.desktop</value>
  </metadata>
</component>
EOF

%post
update-desktop-database &> /dev/null ||:
/bin/touch --no-create %{_datadir}/icons/gnome &>/dev/null || :
/bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
update-desktop-database &> /dev/null ||:
if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_datadir}/icons/gnome &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
  /bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  /usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%post base -p /sbin/ldconfig

%postun base -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root,-)
%{_bindir}/PTBatcherGUI
%{_bindir}/hugin
%{_bindir}/hugin_stitch_project
%{_bindir}/icpfind
%{_bindir}/calibrate_lens_gui
%{_bindir}/hugin_executor
%{_libdir}/%{name}/libhuginbasewx.so*
%{_libdir}/%{name}/libicpfindlib.so*
%{_datadir}/%{name}/xrc
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/PTBatcherGUI.desktop
%{_datadir}/applications/calibrate_lens_gui.desktop
%{_datadir}/applications/pto_gen.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/icons/gnome/48x48/mimetypes/*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/%{name}/data/default.setting
%{_datadir}/%{name}/data/plugins/README_*.txt
%{_datadir}/%{name}/data/plugins/*.py*
%{_datadir}/%{name}/data/plugins-templates/*.py*
%{_datadir}/%{name}/data/hugin_exiftool_copy.arg
%{_datadir}/appdata/PTBatcherGUI.appdata.xml
%{_datadir}/appdata/calibrate_lens_gui.appdata.xml
%{_datadir}/appdata/hugin.appdata.xml
%{_mandir}/man1/PTBatcherGUI.*
%{_mandir}/man1/calibrate_lens_gui.*
%{_mandir}/man1/hugin.*
%{_mandir}/man1/hugin_stitch_project.*
%{_mandir}/man1/icpfind.*
%{_mandir}/man1/hugin_executor.*

%doc AUTHORS COPYING README README_JP TODO src/celeste/LICENCE_LIBSVM doc/nona.txt doc/fulla.html src/hugin1/hugin/xrc/data/help_en_EN/LICENCE.manual

%files base
%defattr(-, root, root,-)
%{_bindir}/align_image_stack
%{_bindir}/autooptimiser
%{_bindir}/celeste_standalone
%{_bindir}/fulla
%{_bindir}/hugin_hdrmerge
%{_bindir}/nona
%{_bindir}/tca_correct
%{_bindir}/vig_optimize
%{_bindir}/cpclean
%{_bindir}/deghosting_mask
%{_bindir}/pano_trafo
%{_bindir}/pano_modify
%{_bindir}/pto_merge
%{_bindir}/checkpto
%{_bindir}/cpfind
%{_bindir}/linefind
%{_bindir}/pto_gen
%{_bindir}/pto_lensstack
%{_bindir}/pto_var
%{_bindir}/geocpset
%{_bindir}/pto_mask
%{_bindir}/pto_move
%{_bindir}/pto_template
%{_bindir}/verdandi
%{_bindir}/hugin_lensdb

%{_libdir}/%{name}/libhuginbase.so*
%{_libdir}/%{name}/libceleste.so*
%{_libdir}/%{name}/liblocalfeatures.so*
%{_libdir}/%{name}/libhuginlines.so*
%{_libdir}/%{name}/libhugin_python_interface.so*
%{python_sitearch}/_hsi.so
%{python_sitearch}/hsi.py*
%{python_sitearch}/hpi.py*

%{_datadir}/%{name}/data/celeste.model
%{_datadir}/%{name}/data/hugin_exiftool_copy.arg
%{_mandir}/man1/align_image_stack.*
%{_mandir}/man1/autooptimiser.*
%{_mandir}/man1/cpclean.*
%{_mandir}/man1/celeste_standalone.*
%{_mandir}/man1/fulla.*
%{_mandir}/man1/hugin_hdrmerge.*
%{_mandir}/man1/nona.*
%{_mandir}/man1/tca_correct.*
%{_mandir}/man1/vig_optimize.*
%{_mandir}/man1/deghosting_mask.*
%{_mandir}/man1/pano_trafo.*
%{_mandir}/man1/pano_modify.*
%{_mandir}/man1/pto_merge.*
%{_mandir}/man1/checkpto.*
%{_mandir}/man1/cpfind.*
%{_mandir}/man1/linefind.*
%{_mandir}/man1/pto_gen.*
%{_mandir}/man1/pto_lensstack.*
%{_mandir}/man1/pto_var.*
%{_mandir}/man1/geocpset.*
%{_mandir}/man1/pto_mask.*
%{_mandir}/man1/pto_move.*
%{_mandir}/man1/pto_template.*
%{_mandir}/man1/verdandi.*
%{_mandir}/man1/hugin_lensdb.*

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2015.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 2015.0.0-4
- Rebuilt for Boost 1.60

* Thu Jan 14 2016 Adam Jackson <ajax@redhat.com> - 2015.0.0-3
- Rebuild for glew 1.13

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 2015.0.0-2
- Rebuilt for Boost 1.59

* Wed Aug 19 2015 Bruno Postle <bruno@postle.net> - 2015.0.0-1
- upstream release

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 2014.0.0-9
- rebuild for Boost 1.58

* Wed Jun 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 2014.0.0-8
- rebuild (exiv2)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Nils Philippsen <nils@redhat.com> - 2014.0.0-6
- rebuild for lensfun-0.3.1

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2014.0.0-5
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 2014.0.0-4
- Add an AppData file for the software center

* Tue Feb 03 2015 Petr Machata <pmachata@redhat.com> - 2014.0.0-3
- Rebuild for boost 1.57.0
- Apply an upstream patch that ports expression parser to
  Boost.Phoenix V3 (hugin-2013.0.0-boost-phoenix3.patch)

* Mon Feb 02 2015 Bruno Postle <bruno@postle.net> - 2014.0.0-2
- Upstream release

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 2013.0.0-12
- Rebuild for boost 1.57.0

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> 2013.0.0-11
- FTBFS against lensfun-0.3 (#1168239)

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 2013.0.0-10
- rebuild (openexr)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 09 2014 Rex Dieter <rdieter@fedoraproject.org> 2013.0.0-8
- update icon/mime scriptlets

* Sat Jun 07 2014 Bruno Postle <bruno@postle.net> - 2013.0.0-7
- Rebuild for rebuilt libpano13

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 2013.0.0-6
- Rebuild for boost 1.55.0

* Sun Dec 15 2013 Bruno Postle <bruno@postle.net> - 2013.0.0-5
- fix to re-enable .pto file association

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 2013.0.0-4
- rebuild (exiv2)

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 2013.0.0-3
- rebuild (openexr)

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 2013.0.0-2
- rebuilt for GLEW 1.10

* Thu Oct 31 2013 Bruno Postle <bruno@postle.net> - 2013.0.0-1
- upstream stable release

* Sun Sep 08 2013 Rex Dieter <rdieter@fedoraproject.org> 2012.0.0-11
- rebuild (openexr)

* Mon Aug 26 2013 Rex Dieter <rdieter@fedoraproject.org> 2012.0.0-10
- fix FTBFS wrt perl pod encoding issue(s) (#991875)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 2012.0.0-8
- Rebuild for boost 1.54.0

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> 2012.0.0-7
- rebuild (openEXR)

* Wed Feb 13 2013 Bruno Postle 2012.0.0-6
- perl-podlators is now split from perl

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 2012.0.0-5
- Rebuild for Boost-1.53.0

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2012.0.0-4
- rebuild due to "jpeg8-ABI" feature drop

* Wed Dec 26 2012 Kevin Fenzi <kevin@scrye.com> 2012.0.0-3
- Rebuild for new libflann_cpp

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 2012.0.0-2
- Rebuild for glew 1.9.0

* Mon Nov 05 2012 Bruno Postle 2012.0.0-1
- Stable release, no longer contains a bundled flann

* Sun Aug 12 2012 Kevin Fenzi <kevin@scrye.com> 2011.4.0-9
- Rebuild for new boost

* Wed Aug 01 2012 Adam Jackson <ajax@redhat.com> 2011.4.0-8
- Rebuild for new glew

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Bruno Postle - 2011.4.0-6
- backported fix for bug that prevented python plugin 'Actions' menu appearing

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 2011.4.0-5
- rebuild (exiv2)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.4.0-4
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Bruno Postle 2011.4.0-3
- Patch to build with gcc-4.7.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Bruno Postle 2011.4.0-1
- upstream release

* Sun Nov 20 2011 Thomas <thomas.spura@googlemail.com> - 2011.2.0-4
- rebuild for https://fedoraproject.org/wiki/Features/F17Boost148

* Sun Oct 30 2011 Bruno Postle 2011.2.0-3
- remove tclap patch since tclap is now in fedora

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 2011.2.0-2
- rebuild (exiv2)

* Fri Sep 30 2011 Bruno Postle 2011.2.0-1
- upstream release. tclap patch ported forward from 2011.0.0, see bug #683591

* Sun Jul 24 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 2011.0.0-3
- Rebuilt for boost 1.47.0 soname bump

* Mon Jun 20 2011 ajax@redhat.com - 2011.0.0-2
- Rebuild for new glew soname

* Mon May 30 2011 Bruno Postle 2011.0.0-1
- upstream release

* Sun Apr 17 2011 Kalev Lember <kalev@smartlink.ee> - 2010.4.0-5
- Rebuilt for boost 1.46.1 soname bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2010.4.0-3
- Rebuild for new Boost

* Fri Feb 04 2011 Bruno Postle <bruno@postle.net> - 2010.4.0-2
- Backport gcc-4.6.0 patch from upstream

* Wed Jan 12 2011 Bruno Postle <bruno@postle.net> - 2010.4.0-1
- Upstream release (2010.4.0)

* Sun Jan 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 2010.2.0-2
- rebuild (exiv2)

* Sun Nov 07 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 2010.2.0-1
- Upstream release (2010.2.0)

* Mon Aug 23 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 2010.0.0-5
- The xorg-x11-devel package is not available on Fedora. So,
   removed it.

* Wed Aug 04 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 2010.0.0-4
- Rebuild for Boost soname bump
- Update to match current guidelines and drop obsolete ifdefs

* Wed Jul 14 2010 Dan Horák <dan@danny.cz> - 2010.0.0-3
- rebuilt against wxGTK-2.8.11-2

* Mon May 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 2010.0.0-2 
- rebuild (exiv2)

* Tue Mar 23 2010 Bruno Postle <bruno@postle.net> 2010.0.0-1
- 2010.0.0 release
- Thanks to Terry Duell for updated .spec

* Fri Feb 05 2010 Bruno Postle <bruno@postle.net> 2009.4.0-1
- Fixes for push to fedora
 
* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 2009.2.0-2
- Rebuild for Boost soname bump

* Tue Oct 20 2009 Bruno Postle <bruno@postle.net> 2009.2.0-1
- 2009.2.0 release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Bruno Postle <bruno@postle.net> 0.8.0-1
- 0.8.0 release

* Thu May 28 2009 Bruno Postle <bruno@postle.net> - 0.7.0-7
- Rebuild for libpano13 soname change

* Fri May 22 2009 Bruno Postle <bruno@postle.net> - 0.7.0-6
- Rebuild for boost soname change.
- Remove trademark from summary, remove .desktop vendor.

* Sun Mar 01 2009 Caolán McNamara <caolanm@redhat.com> - 0.7.0-5
- include stdio.h for snprintf and cstdio for std::sprintf

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-3 
- respin (eviv2)

* Thu Dec 18 2008 Petr Machata <pmachata@redhat.com> - 0.7.0-2
- rebuild for new boost

* Tue Oct 07 2008 Bruno Postle <bruno@postle.net> 0.7.0-1
- 0.7.0 release

* Thu Jun 26 2008 Bruno Postle <bruno@postle.net> 0.7.0-0.4.20080528svn
- rawhide rebuild for updated libexiv2

* Wed May 28 2008 Bruno Postle <bruno@postle.net> 0.7.0-0.3.20080528svn
- SVN snapshot, 0.7 beta. New tools matchpoint tca_correct

* Mon Feb 18 2008 Bruno Postle <bruno@postle.net> 0.7.0-0.3.20080218svn
- SVN snapshot, 0.7 beta, gcc-4.3.0 fixes

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.0-0.3.20080216svn
- Autorebuild for GCC 4.3

* Tue Feb 05 2008 Bruno Postle <bruno@postle.net> 0.7.0-0.2.20080205svn
- SVN snapshot, 0.7 beta.

* Tue Jan 22 2008 Bruno Postle <bruno@postle.net> 0.7.0-0.2.20080121svn
- SVN snapshot, 0.7 beta. move cli dependencies to hugin-base package

* Mon Jan 21 2008 Bruno Postle <bruno@postle.net> 0.7.0-0.1.20080121svn
- SVN snapshot, add LICENCE.manual

* Sat Jan 19 2008 Bruno Postle <bruno@postle.net> 0.7.0-0.1.20080119svn
- SVN snapshot, split to hugin and hugin-base packages

* Wed Jan 16 2008 Bruno Postle <bruno@postle.net> 0.7.0-0.1.20080116svn
- remove autopano-sift-C dependency, use autopano-noop.sh instead
- delete devel .so symlinks

* Mon Jan 14 2008 Bruno Postle <bruno@postle.net> 0.7.0-0.1.20080112svn
- SVN snapshot, switch to fedora naming scheme, add exiftool dependency

* Sat Oct 27 2007 Bruno Postle <bruno@postle.net> 0.7.0-0svn20071029
- revert to trunk
- ldconfig as we are installing libs
- libpano13-tools & make dependency

* Wed Oct 24 2007 Bruno Postle <bruno@postle.net> 0.7.0-0svn20071024
- lib64 issue should be fixed, lots of .so.0 files now, release has decremented

* Mon Oct 22 2007 Bruno Postle <bruno@postle.net> 0.7.1-0svn20071022
- ippei branch, switch to cmake

* Mon Apr 16 2007 Bruno Postle <bruno@postle.net> 0.7.0_beta5-0cvs20070416
- CVS snapshot
- add shared-mime-info, desktop-file-utils dependencies
- use desktop-file-install for .desktop file

* Mon Jan 29 2007 Bruno Postle <bruno@postle.net> 0.7.0_beta3-2cvs20070129
- CVS snapshot of 0.7 beta, switch to libpano13

* Sun Sep 17 2006 Bruno Postle <bruno@postle.net> 0.6.1-4
- Fix spec typos and cruft, use find_lang, post and postun fixes

* Fri Sep 15 2006 Bruno Postle <bruno@postle.net> 0.6.1-2
- replace mono autopanog patch with sed

* Thu Aug 24 2006 Bruno Postle <bruno@postle.net> 0.6.1-1
- 0.6.1 release

* Mon Jul 24 2006 Bruno Postle <bruno@postle.net> 0.6-4
- 0.6 release, tidy spec file, add post-release autopano-sift patch

* Mon Jul 24 2006 Bruno Postle <bruno@postle.net> 0.6-3
- 0.6 release

* Mon Jun 19 2006 Bruno postle <bruno@postle.net> 0.6-2cvs20060611
- Recompile to link to libpano12-2.8.4. use find_lang macro. remove repo tag. use dist tag

* Wed Apr 19 2006 Bruno Postle <bruno@postle.net>
- 0.6 CVS snapshot + gcc 4.1 hack.
- batch processing for fulla.
- requires latest pano12 > 2.8.0 for direct access to optimiser

* Thu Mar 09 2006 Bruno Postle <bruno@postle.net>
- 0.6 CVS snapshot + hack to fix charset of cs_CZ translation

* Thu Mar 09 2006 Bruno Postle <bruno@postle.net>
- 0.6 CVS snapshot. new vignetting/aberation/lens correction tool: fulla

* Tue Mar 07 2006 Bruno Postle <bruno@postle.net>
- 0.6 CVS snapshot, add missing docs

* Thu Jan 12 2006 Bruno Postle <bruno@postle.net>
- 0.6 CVS snapshot. Philippe Thomins color correction tool. fix for ptoptimizer

* Mon Jan 09 2006 Bruno Postle <bruno@postle.net>
- 0.6 CVS snapshot. nona vignetting correction

* Mon Nov 14 2005 Bruno Postle <bruno@postle.net>
- new build from CVS. included ca_ES catalan translation

* Thu Nov 10 2005 Bruno Postle <bruno@postle.net>
- new build from CVS. included hu hungarian translation

* Fri Sep 16 2005 Bruno Postle <bruno@postle.net>
- new build from CVS. includes zh_CN Chinese translation

* Fri Sep 16 2005 Bruno Postle <bruno@postle.net>
- new build from CVS. includes nl dutch translation

* Wed Aug 17 2005 Bruno Postle <bruno@postle.net>
- new build from CVS.
- Remove patch that turns off enblend compression, as compression
  is now disabled by default.

* Thu Mar 10 2005 Bruno Postle <bruno@postle.net>
- new build from CVS. This is approximately hugin 0.5 beta3

* Mon Feb 28 2005 Bruno Postle <bruno@postle.net>
- new build from CVS. Removed fftw dependency

* Mon Nov 22 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs. patch to call enblend without compression.
  patch to call autopanog.exe via mono.

* Thu Oct 21 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs.  Should fix bug where fov can't be optimised

* Wed Oct 20 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs.  Updated French translation.
  add enblend dependency.

* Thu Oct 14 2004 Bruno Postle  <bruno@postle.net>
- New build for fedora fc2.
  Now uses automake/autoconf
  Switch dependency from panorama-tools to libpano12 & libpano12-devel

* Thu Sep 09 2004 Bruno Postle <bruno@postle.net>
- new build from cvs.  point picker can do rotation matching, various bugfixes.
  panoviewer doesn't get built anymore.

* Tue Aug 31 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs.  Should fix bug where enblend isn't executed from the gui.

* Fri Jul 23 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs, removed vigra dependency.

* Tue Jul 13 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs, still requires vigra, though the vigra stuff is now
  in the hugin tree. Installs utilities: mergepto pta2hugin.py run-autopano-sift.sh

* Fri Jul 02 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs, needs a newer patched vigra
- install various (nonworking?) tools automatch autooptimiser panosifter
  autopano_old

* Tue Jun 15 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs, requires a vigra with 16bit unsigned tiff support
     remove: autopano_old, automatch, autooptimiser, panosifter

* Sun Apr 04 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs, new features:
     autopano integration
     delete control points between selected images
     reset positions of all selected images

* Sun Mar 14 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs, this is post 0.4b release with nona_gui

* Sun Feb 08 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs.  Now doesn't depend on vigra

* Wed Feb 04 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs.  Now depends on vigra

* Tue Feb 03 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs.  Two new tools autooptimiser and panosifter

* Thu Jan 15 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs. now includes automatch

* Sat Jan 03 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs.  This is the 0.4pre release

* Thu Jan 01 2004 Bruno Postle  <bruno@postle.net>
- new build from cvs.  autopano now requires fftw.

* Sun Nov 30 2003 Bruno Postle <bruno@postle.net>
- The vigra library when compiled with shared libraries isn't actually
  necessary to run nona, so it's now only a build requirement.  The
  panorama-tools package is now split with the nonfree package now
  required to run hugin.

* Sat Nov 29 2003  Bruno Postle  <bruno@postle.net>
- new build from cvs; stitcher is now called nona

* Mon Nov 24 2003 Bruno Postle  <bruno@postle.net>
- new build from cvs; add vigra dependency for stitcher

* Sun Nov 16 2003 Bruno Postle <bruno@postle.net>
- new build from cvs; patch to build with gtk2

* Sun Nov 09 2003 Bruno Postle <bruno@postle.net>
- new build from cvs; first build with fedora1

* Mon Oct 27 2003 Bruno Postle <bruno@postle.net>
- new build from cvs, added manual.html to doc and [de] translation to .desktop

* Mon Oct 13 2003 Bruno Postle <bruno@postle.net>
- build of hugin-0-3-beta release, sorry no time to fix numbering.

* Sat Oct 04 2003 Bruno Postle <bruno@postle.net>
- new build from cvs, patch0 adds a shortcut to gnome/kde menu

* Thu Sep 25 2003 Bruno Postle <bruno@postle.net>
- build now requires panorama tools include headers.

* Wed Aug 06 2003 Bruno Postle <bruno@postle.net>
- new build from cvs. po/mo files still not getting built

* Sat Aug 02 2003 Bruno Postle <bruno@postle.net>
- new build from cvs, panoviewer now gets built by default. removed
  useless .po installation.

* Sat Jul 26 2003 Bruno Postle <bruno@postle.net>
- new build from cvs, panoviewer built as well

* Sat May 24 2003 Bruno Postle <bruno@postle.net>
- build of wxGTK version

* Sat May 10 2003 Bruno Postle
- Initial RPM release.
