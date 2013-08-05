%global gem_name mobileesp_converted

Name: rubygem-%{gem_name}
Version: 0.2.1
Release: 4%{?dist}
Summary: Provides device type detection based on HTTP request headers
Group: Development/Languages
License: ASL 2.0 
URL: http://github.com/jistr/mobileesp_converted
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
#tests
BuildRequires: rubygem(rake)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(bundler)

BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Autoconverted version (from Java to Ruby) of MobileESP library.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

sed -i '1{/#\!\/usr\/bin\/env rake/d}' %{buildroot}%{gem_instdir}/Rakefile
rm %{buildroot}%{gem_instdir}/.gitignore

%check
pushd .%{gem_instdir}
rake test
popd


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%exclude %{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/README.md

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/convert_to_ruby.vim
%{gem_instdir}/java_source/
%{gem_instdir}/spec/

%changelog
* Thu Jul 25 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.1-4
- add BR rubygem(bundler)

* Thu Jul 25 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.1-3
- include gemspec (msuchy@redhat.com)
- use rake instead of rspec (msuchy@redhat.com)
- BR rubygem(minitest) (msuchy@redhat.com)
- enable tests (msuchy@redhat.com)

* Tue Jul 23 2013 Miroslav Suchý <msuchy@redhat.com> 0.2.1-2
- initial package

