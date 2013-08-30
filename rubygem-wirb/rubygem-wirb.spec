%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name wirb
Summary: Wavy IRB: Colorizes irb results
Name: %{?scl_prefix}rubygem-%{gem_name}

Version: 1.0.1
Release: 4%{dist}
Group: Development/Languages
License: MIT
URL: https://github.com/janlelis/wirb
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fedora} > 18
Requires: %{?scl_prefix}ruby(release)
%else
Requires: %{?scl_prefix}ruby(abi) = 1.9.1
%endif
BuildRequires: %{?scl_prefix}rubygems-devel
BuildRequires: %{?scl_prefix}rubygems
Requires: %{?scl_prefix}rubygems
Requires: %{?scl_prefix}rubygem(paint)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(wirb) = %{version}
#tests
BuildRequires: rubygem(rspec)

%description
Wavy IRB: Colorizes irb results. It originated from Wirble, but only provides
result highlighting. Just call Wirb.start and enjoy the colors in your IRB ;).
You can use it with your favorite colorizer engine. See README.rdoc for more
details.

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}
%setup -q -D -T -n %{gem_name}-%{version}

%{?scl:scl enable %{scl} "}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:"}

%build
%{?scl:scl enable %{scl} "}
gem build %{gem_name}.gemspec
%{?scl:"}

%{?scl:scl enable %{scl} - << \EOF}
%if 0%{?fedora} >= 18
%{gem_install}
%else
mkdir -p ./%{gem_dir}
gem install --local --install-dir ./%{gem_dir} --force %{SOURCE0}
%endif
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

rm -rf %{buildroot}%{gem_instdir}/.yardoc
rm -f %{buildroot}%{gem_instdir}/.gemtest

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/data
%doc %{gem_instdir}/COPYING.txt
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.rdoc

%files doc
%{gem_instdir}/spec
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec

%check
pushd ./%{gem_instdir}
#requires rubygem-zucker which is not in Fedora
#rspec spec
popd

%changelog
* Tue Aug 20 2013 Miroslav Suchý <msuchy@redhat.com> 1.0.1-4
- populate ./%%{gem_dir} so we can cd there for tests

* Tue Aug 20 2013 Miroslav Suchý <msuchy@redhat.com> 1.0.1-3
- use standard group
- summary should not end with dot

* Tue Aug 20 2013 Miroslav Suchý <msuchy@redhat.com> 1.0.1-2
- add placeholder for tests

* Tue Aug 20 2013 Miroslav Suchý <msuchy@redhat.com> 1.0.1-1
- rebase to 1.0.1

* Thu Jul 04 2013 Dominic Cleal <dcleal@redhat.com> 0.4.2-6
- change ruby(abi) to ruby(release) for F19+ (dcleal@redhat.com)
- delete all zero sized tito.props (msuchy@redhat.com)
- with recent tito you do not need SCL meta package (msuchy@redhat.com)

* Wed Mar 27 2013 Miroslav Suchý <msuchy@redhat.com> 0.4.2-4
- put correct license in spec (msuchy@redhat.com)

* Thu Mar 14 2013 Miroslav Suchý <msuchy@redhat.com> 0.4.2-3
- new package built with tito

* Fri Sep 07 2012 Miroslav Suchý <msuchy@redhat.com> 0.4.2-2
- polish the spec (msuchy@redhat.com)

* Thu Sep 06 2012 Miroslav Suchý <msuchy@redhat.com> 0.4.2-1
- new package built with tito

