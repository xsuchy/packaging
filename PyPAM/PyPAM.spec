%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Summary:        PAM bindings for Python
Name:           PyPAM
Version:        0.5.0
Release:        19%{?dist}
# Note that the upstream site is dead.
Source0:        http://www.pangalactic.org/PyPAM/%{name}-%{version}.tar.gz
Url:            http://www.pangalactic.org/PyPAM
Patch0:         PyPAM-dlopen.patch
Patch1:         PyPAM-0.5.0-dealloc.patch
Patch2:         PyPAM-0.5.0-nofree.patch
Patch3:         PyPAM-0.5.0-memory-errors.patch
Patch4:         PyPAM-0.5.0-return-value.patch
License:        LGPLv2
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python2-devel pam-devel
Requires:       python
%filter_provides_in %{python_sitearch}/PAMmodule.so$
%filter_setup

%description
PAM (Pluggable Authentication Module) bindings for Python.

%prep
%setup -q
%patch0 -p1 -b .dlopen
%patch1 -p1 -b .dealloc
%patch2 -p1 -b .nofree
%patch3 -p1 -b .memory
%patch4 -p1 -b .retval
# remove prebuild rpm and others binaries
rm -rf build dist

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root=$RPM_BUILD_ROOT
# Make sure we don't include binary files in the docs
chmod 644 examples/pamtest.py
rm -f examples/pamexample

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%{python_sitearch}/PAMmodule.so
%{python_sitearch}/*.egg-info
%doc AUTHORS NEWS README ChangeLog COPYING INSTALL 
%doc examples 

%changelog
* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May  7 2012 Tomáš Mráz <tmraz@redhat.com> - 0.5.0-15
- fix one more memory leak

* Mon May  7 2012 Tomáš Mráz <tmraz@redhat.com> - 0.5.0-14
- always return the error code in exceptions (#819244)

* Fri May  4 2012 Tomáš Mráz <tmraz@redhat.com> - 0.5.0-13
- fix memory manipulation errors (leaks, doublefree CVE-2012-1502)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 23 2011 Miroslav Suchý <msuchy@redhat.com> 0.5.0-10
- 679714 - deallocate the conversation response only in case of error

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Miroslav Suchý <msuchy@redhat.com> 0.5.0-9
- 658955 - fix two bugs in the PAM object deallocation
- add -fno-strict-aliasing to CFLAGS

* Thu Aug 05 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-7
- 612998 - PyPAM do not work with python3 (msuchy@redhat.com)

* Thu Aug 05 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-6
- 612998 - fix condition for BR (msuchy@redhat.com)

* Thu Aug 05 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-5
- 612998 - return back BR for python

* Thu Aug 05 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-4
- 612998 - remove binaries. Just in case
- 612998 - filter provide PAMmodule.so()(64bit)
- 612998 - do not use INSTALLED_FILES feature, and enumerate files manualy
- 612998 - use %%{__python} in %%build section
- 612998 - fix buildrequires for PyPAM
- 612998 - add macros for rhel5

* Fri Jul 09 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-3
- rebuild 

* Fri Jul 09 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-2
- rebase PyPAM-dlopen.patch to latest source

* Fri Jul 09 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-1
- rebase to PyPAM 0.5.0

* Fri Mar 06 2009 Devan Goodwin <dgoodwin@redhat.com> 0.4.2-26
- Fix bad patch whitespace.

* Fri Feb 27 2009 Dennis Gilmore 0.4.2-25
- rebuild to pick up ppc ppc64 ia64 arches

* Fri Feb 27 2009 Devan Goodwin <dgoodwin@redhat.com> 0.4.2-23
- Rebuild for new rel-eng tools.

* Fri May 16 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.2-20
- fixed file ownership

* Tue Jun 22 2004 Mihai Ibanescu <misa@redhat.com> 0.4.2-5
- Rebuilt

* Fri Jul 11 2003 Mihai Ibanescu <misa@redhat.com>
- Adapted the original rpm to build with python 2.2
