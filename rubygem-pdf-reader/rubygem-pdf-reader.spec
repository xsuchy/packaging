%global gem_name pdf-reader
%if 0%{?rhel} == 6
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%endif

Summary: Ruby library to parse PDF files
Name: rubygem-%{gem_name}
Version: 1.3.3
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/yob/pdf-reader
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
# git clone git://github.com/yob/pdf-reader.git && cd pdf-reader/
# git archive --format=tar --prefix=spec/ eee24b0:spec | gzip > pdf-reader-spec.tar-1.3.3.tar.gz
Source1: pdf-reader-spec-%{version}.tar.gz
%if 0%{?rhel} == 6
Requires: ruby(abi) = 1.8
%else
Requires: ruby(release)
%endif
%if 0%{?fedora}
BuildRequires: rubygems-devel
%endif
BuildRequires: rubygems
%if 0%{?fedora} > 16
BuildRequires: rubygem-rspec
%endif
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}
Requires: rubygem(Ascii85) >= 1.0.0
Requires: rubygem(Ascii85) < 1.1.0
BuildRequires: rubygem(Ascii85) >= 1.0.0
BuildRequires: rubygem(Ascii85) < 1.1.0
Requires: rubygem(ruby-rc4)
BuildRequires: rubygem(ruby-rc4)
BuildRequires: rubygem(minitest)
Requires: rubygem(afm) >= 0.2.0
Requires: rubygem(afm) < 0.3.0
Requires: rubygem(hashery) >= 2.0
Requires: rubygem(hashery) < 3.0

%description
The PDF::Reader library implements a PDF parser conforming as much as possible
to the PDF specification from Adobe.

%package doc
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
tar -xzf %{SOURCE1}

%build

gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

mv %{buildroot}%{gem_instdir}/{TODO,README.rdoc,MIT-LICENSE,CHANGELOG} ./
rm -rf %{buildroot}%{gem_instdir}/.yardoc

chmod a+x %{buildroot}%{gem_instdir}/examples/*.rb

%check
%if 0%{?fedora} > 16
cp -pr spec/ ./%{gem_instdir}
pushd ./%{gem_instdir}
sed -i '/require.*bundler/d' spec/spec_helper.rb
sed -i '/Bundler.setup/d' spec/spec_helper.rb
rspec spec
rm -rf spec
popd
%endif

%files
%{_bindir}/pdf_*
%doc MIT-LICENSE
%dir %{gem_instdir}
%{gem_instdir}/lib
%{gem_instdir}/bin
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc README.rdoc TODO CHANGELOG
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/examples

%changelog
* Mon Aug 05 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.3-1
- rebase to 1.3.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Miroslav Suchý <msuchy@redhat.com> - 1.1.1-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 05 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-6
- 850679 - add rubygem(minitest) to BR (msuchy@redhat.com)
- 850679 - include version in file name with spec tests (msuchy@redhat.com)

* Mon Sep 03 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-5
- 850679 - run test suite (msuchy@redhat.com)
- 850679 - flag examples as executables (msuchy@redhat.com)

* Thu Aug 23 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-4
- 850679 - add rubygems to BR (msuchy@redhat.com)
- 850679 - fix BR and do not remove %%{gem_instdir}/bin (msuchy@redhat.com)

* Wed Aug 22 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-3
- add runtime dependencies (msuchy@redhat.com)

* Wed Aug 22 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-2
- new package built with tito

* Tue Aug 21 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-1
- new package built with tito

