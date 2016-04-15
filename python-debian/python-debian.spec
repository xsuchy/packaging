%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?fedora}
%global with_python3 1
%else
%global with_python3 0
%endif

Name:           python-debian
Version:        0.1.27
Release:        4%{?dist}
Summary:        Modules for Debian-related data formats
# debfile.py, arfile.py, debtags.py are release under GPL v3 or above
# everything else is GPLv2+
License:        GPLv2+ and GPLv3+
Group:          Development/Libraries
Source0:        http://ftp.debian.org/debian/pool/main/p/python-debian/python-debian_%{version}.tar.xz
Patch1:			0001-add-support-for-lzma.patch
URL:            http://git.debian.org/?p=pkg-python-debian/python-debian.git
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
Requires:       python >= 2.4
Requires:		python-chardet
Requires:       xz
Requires:       python-six
#not available now
#Recommends:    python-apt
Suggests:       gnupg
BuildRequires:  python-devel, python-setuptools, python-chardet
BuildRequires:  python-six

%description
This package provides Python modules that abstract many formats of Debian 
related files. Currently handled are:
* Debtags information (debian.debtags module)
* debian/changelog (debian.changelog module)
* Packages files, pdiffs (debian.debian_support module)
* Control files of single or multiple RFC822-style paragraphs, e.g.
  debian/control, .changes, .dsc, Packages, Sources, Release, etc.
  (debian.deb822 module)
* Raw .deb and .ar files, with (read-only) access to contained
  files and meta-information

%if 0%{?with_python3}
%package -n python3-debian
Summary:        Modules for Debian-related data formats
BuildRequires:  python3-devel

%description -n python3-debian
This package provides Python modules that abstract many formats of Debian
related files. Currently handled are:
* Debtags information (debian.debtags module)
* debian/changelog (debian.changelog module)
* Packages files, pdiffs (debian.debian_support module)
* Control files of single or multiple RFC822-style paragraphs, e.g.
  debian/control, .changes, .dsc, Packages, Sources, Release, etc.
  (debian.deb822 module)
* Raw .deb and .ar files, with (read-only) access to contained
  files and meta-information
%endif


%prep
%setup -q
%patch1 -p1

%if 0%{with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
sed -e 's/__CHANGELOG_VERSION__/$(VERSION)/' < setup.py.in > setup.py
%{__python} setup.py build

%if 0%{with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --root=$RPM_BUILD_ROOT
popd
%endif


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%{__python} setup.py clean

%check
cd tests;
#./test_deb822.py
#TODO - fix this test
#./test_debfile.py
./test_debtags.py
./test_changelog.py
#./test_debian_support.py

%if 0%{with_python3}
pushd %{py3dir}
cd tests;
#./test_deb822.py
#TODO - fix this test
#./test_debfile.py
./test_debtags.py
./test_changelog.py
#./test_debian_support.py
popd
%endif

%files
%defattr(-,root,root,-)
%dir %{python_sitelib}/debian
%dir %{python_sitelib}/debian_bundle
%{python_sitelib}/*.py*
%{python_sitelib}/debian/*.py*
%{python_sitelib}/debian_bundle/__init__.py*
%{python_sitelib}/python_debian*
%doc README README.changelog README.deb822 HISTORY.deb822 ACKNOWLEDGEMENTS

%if 0%{?with_python3}
%files -n python3-debian
%defattr(-,root,root,-)
%dir %{python3_sitelib}/debian
%dir %{python3_sitelib}/debian_bundle
%{python3_sitelib}/*.py*
%{python3_sitelib}/__pycache__
%{python3_sitelib}/debian/*.py*
%{python3_sitelib}/debian/__pycache__
%{python3_sitelib}/debian_bundle/__init__.py*
%{python3_sitelib}/debian_bundle/__pycache__
%{python3_sitelib}/python_debian*
%doc README README.changelog README.deb822 HISTORY.deb822 ACKNOWLEDGEMENTS
%endif

%changelog
* Fri Apr 15 2016 Miroslav Suchý <msuchy@redhat.com> 0.1.27-4
- bump up release 

* Thu Apr 14 2016 Miroslav Suchý <msuchy@redhat.com> 0.1.27-3
- 1021625 - add support for lzma

* Thu Oct 08 2015 Miroslav Suchý <msuchy@redhat.com> 0.1.27-2
- define macro for epel

* Thu Oct 08 2015 Miroslav Suchý <msuchy@redhat.com> 0.1.27-1
- rebase to python-debian_0.1.27
- add python3 subpackage

* Mon Apr 13 2015 Miroslav Suchý <msuchy@redhat.com> 0.1.26-2
- rebase to 0.1.26

* Mon Apr 13 2015 Miroslav Suchý <msuchy@redhat.com> 0.1.26-1
- rebase to 0.1.26

* Thu Nov 28 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.21-10
- add dependency on python-six

* Thu Nov 28 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.21-9
- specify patch level
- specify prefix of tar

* Thu Nov 28 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.21-8
- rebase to nmu2 release

* Thu Nov 28 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.21-7
- 1021625 - recognize xz compression

* Mon Oct  3 2011 Miroslav Suchy <msuchy@redhat.com> 0.1.21-2
- rebase to 0.1.21 release
- require python-chardet

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri May  7 2010 Miroslav Suchy <msuchy@redhat.com> 0.1.16-4
- rebuild for python 2.7

* Fri May  7 2010 Miroslav Suchy <msuchy@redhat.com> 0.1.16-3
- use proper tar.gz from upstream
- add %%check section

* Fri Apr 30 2010 Miroslav Suchy <msuchy@redhat.com> 0.1.16-2
- add dist tag

* Thu Apr 22 2010 Lukáš Ďurfina <lukas.durfina@gmail.com> 0.1.16-1
- Creation of package
