# This package contains macros that provide functionality relating to
# Software Collections. These macros are not used in default
# Fedora builds, and should not be blindly copied or enabled.
# Specifically, the "scl" macro must not be defined in official Fedora
# builds. For more information, see:
# http://docs.fedoraproject.org/en-US/Fedora_Contributor_Documentation
# /1/html/Software_Collections_Guide/index.html
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name single_test
%global git_hash 64657b2

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.6.0
Release: 1%{?dist}
Summary: Rake tasks to invoke single tests/specs with rakish syntax
Group: Development/Languages
License: Public Domain
URL: http://github.com/grosser/single_test
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fedora} > 18
Requires: %{?scl_prefix}ruby(release)
%else
Requires: %{?scl_prefix}ruby(abi) = 1.9.1
%endif
Requires: %{?scl_prefix}ruby(rubygems) 
Requires: %{?scl_prefix}rubygem(rake) > 0.9
BuildRequires: %{?scl_prefix}rubygems-devel 
BuildRequires: %{?scl_prefix}rubygems
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
#tests
BuildRequires: rubygem-rspec

%description
Runs a single test/spec via rake.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} "}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:"}

%build
mkdir -p .%{gem_dir}

# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} "}
gem build %{gem_name}.gemspec
%{?scl:"}

%{?scl:scl enable %{scl} - << \EOF}
%if 0%{?fedora} > 18
%{gem_install}
%else
mkdir -p ./%{gem_dir}
gem install --local --install-dir ./%{gem_dir} --force %{gem_name}-%{version}.gem
%endif
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Fri Aug 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.6.0-1
- rebase to 0.6.0

* Fri Aug 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.5.2-3
- initial package

* Thu Jun 13 2013 Lukas Zapletal <lzap+git@redhat.com> 0.5.2-2
- post gem2rpm changes (lzap+git@redhat.com)

* Thu Jun 13 2013 Lukas Zapletal <lzap+git@redhat.com> 0.5.2-1
- new package built with tito

