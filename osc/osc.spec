Name:           osc
Version:        0.140.1
Release:        107.1.0%{?dist}
Group:          Development/Tools
License:        GPLv2+
Url:            https://github.com/openSUSE/osc
#the tarball come from gitourious.
#i check out the latest version, same as openSUSE version.
#git clone git@github.com:openSUSE/osc.git
#git archive --prefix="osc-0.140.1/" --format=tar 0.140.1| gzip > osc-0.140.1.tar.gz
Source:         osc-%{version}.tar.gz
Summary:        The openSUSE Build Service Commander
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  rpm-python
Requires:       rpm-python
Requires:       m2crypto
Requires:       python-lxml
Requires:       python-urlgrabber
Requires:       fuse-python

#Recommends:     osc-source_validator

%description
Commandline client for the openSUSE Build Service.

See http://en.opensuse.org/openSUSE:OSC , as well as
http://en.opensuse.org/openSUSE:Build_Service_Tutorial for a general
introduction.


%prep
%setup -q

#fixup encoding
iconv -f ISO8859-1 -t UTF-8 -o TODO.new TODO
mv TODO.new TODO

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__python} setup.py install -O1 --prefix=%{_prefix} --root %{buildroot}
%__ln_s osc-wrapper.py %{buildroot}/%{_bindir}/osc
%__mkdir_p %{buildroot}%{_localstatedir}/lib/osc-plugins
install -Dm0644 dist/complete.csh %{buildroot}%{_sysconfdir}/profile.d/osc.csh
install -Dm0644 dist/complete.sh %{buildroot}%{_sysconfdir}/profile.d/osc.sh
install -Dm0755 dist/osc.complete %{buildroot}/%{_prefix}/lib/osc/complete

%files
%doc AUTHORS README TODO NEWS
%{_bindir}/osc*
%{python_sitelib}/*
%config %{_sysconfdir}/profile.d/osc.csh
%config %{_sysconfdir}/profile.d/osc.sh
%dir %{_localstatedir}/lib/osc-plugins
%{_mandir}/man1/osc.*
%{_prefix}/lib/osc

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.132.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.132.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.132.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Jerome Soyer <saispo@gmail.com> - 0.132.4-1
- Update to 0.132.4

* Thu Jun  9 2011 Jerome Soyer <saispo@gmail.com> - 0.132.1-2
- Fix non-arch dependent shell script in /usr/lib for multilib

* Wed Jun  8 2011 Jerome Soyer <saispo@gmail.com> - 0.132.1-1
- Update to 0.132.1
- Fix tab/space in SPEC file
- Add comment and command for tarball creation
- Fix libdir-macro-in-noarch-package

* Wed Jun  8 2011 Jerome Soyer <saispo@gmail.com> - 0.132.0-1
- Initial build
