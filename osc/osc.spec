%if (0%{?fedora} > 12 || 0%{?rhel} > 6)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           osc
Version:        0.132.4
Release:        4%{?dist}
Group:          Development/Tools
License:        GPLv2+
Url:            http://www.gitorious.org/opensuse/osc
#the tarball come from gitourious.
#i check out the latest version, same as openSUSE version.
#git clone git://gitorious.org/opensuse/osc.git
#git archive --prefix="osc-0.132.4/" --format=tar 0.132.4| gzip > osc-0.132.4.tar.gz
Source:         osc-%{version}.tar.gz
Summary:        The openSUSE Build Service Commander
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel
Requires:       rpm-python m2crypto python-lxml python-urlgrabber fuse-python

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
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --prefix=%{_prefix} --root %{buildroot}
%__ln_s osc-wrapper.py %{buildroot}/%{_bindir}/osc
%__mkdir_p %{buildroot}/var/lib/osc-plugins
%__mkdir_p %{buildroot}%{_datadir}/%{name}/complete
%__install -m 0644 dist/complete.csh %{buildroot}%{_datadir}/%{name}/complete/osc.csh
%__install -m 0644 dist/complete.sh %{buildroot}%{_datadir}/%{name}/complete/osc.sh
%__mkdir_p %{buildroot}/%{_prefix}/lib/osc
%__install -m 0755 dist/osc.complete %{buildroot}/%{_prefix}/lib/osc/complete

%clean
%{__rm} -rf %{buildroot}

%files

%defattr(-,root,root,-)
%doc AUTHORS README TODO NEWS
%{_bindir}/osc*
%{python_sitelib}/*
%{_prefix}/lib/osc/complete
%dir /var/lib/osc-plugins
%{_mandir}/man1/osc.*
%{_datadir}/%{name}/*

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
