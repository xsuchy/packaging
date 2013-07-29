%global gem_name yajl-ruby

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 1%{?dist}
Summary: Ruby C bindings to the excellent Yajl JSON stream-based parser library
Group: Development/Languages
License: MIT
URL: http://github.com/brianmario/yajl-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby-devel >= 1.8.6
Provides: rubygem(%{gem_name}) = %{version}

%description
This gem is a C binding to the excellent YAJL JSON parsing and generation
library.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

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

mkdir -p %{buildroot}%{gem_extdir_mri}/lib
# TODO: move the extensions
mv %{buildroot}%{gem_instdir}/lib/shared_object.so %{buildroot}%{gem_extdir_mri}/lib/



%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/ext
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Mon Jul 29 2013 msuchy@redhat.com - 1.1.0-1
- Initial package
