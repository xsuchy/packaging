%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-debian
Version:        0.1.21
Release:        8%{?dist}
Summary:        Modules for Debian-related data formats
# debfile.py, arfile.py, debtags.py are release under GPL v3 or above
# everything else is GPLv2+
License:        GPLv2+ and GPLv3+
Group:          Development/Libraries
Source0:        http://ftp.debian.org/debian/pool/main/p/python-debian/python-debian_%{version}+nmu2.tar.gz
URL:            http://git.debian.org/?p=pkg-python-debian/python-debian.git
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
Requires:       python >= 2.4
Requires:		python-chardet
Requires:       xz
BuildRequires:  python-devel, python-setuptools, python-chardet
Patch1:         xz-member.patch

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


%prep
%setup -q
%patch1

%build
sed -e 's/__CHANGELOG_VERSION__/$(VERSION)/' < setup.py.in > setup.py
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%{__python} setup.py clean

%check
cd tests;
./test_deb822.py
#TODO - fix this test
#./test_debfile.py
./test_debtags.py
./test_changelog.py
./test_debian_support.py


%files
%defattr(-,root,root,-)
%dir %{python_sitelib}/debian
%dir %{python_sitelib}/debian_bundle
%{python_sitelib}/*.py*
%{python_sitelib}/debian/*.py*
%{python_sitelib}/debian_bundle/__init__.py*
%{python_sitelib}/python_debian*

%doc README README.changelog README.deb822 HISTORY.deb822 ACKNOWLEDGEMENTS

%changelog
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
