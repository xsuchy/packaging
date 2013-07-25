%global gem_name hoptoad_notifier

Name: rubygem-%{gem_name}
Version: 2.4.11
Release: 1%{?dist}
Summary: Send your application errors to our hosted service and reclaim your inbox
Group: Development/Languages
License: MIT 
URL: http://www.hoptoadapp.com
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(builder) 
Requires: rubygem(activesupport) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description



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

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/generators/
%{gem_instdir}/script/
%{gem_instdir}/rails/
%doc %{gem_instdir}/INSTALL
%doc %{gem_instdir}/README.md

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README_FOR_HEROKU_ADDON.md
%doc %{gem_instdir}/TESTING.rdoc
%doc %{gem_instdir}/SUPPORTED_RAILS_VERSIONS
%{gem_instdir}/test/
%{gem_instdir}/spec/
%{gem_instdir}/Rakefile

%changelog
* Thu Jul 25 2013 msuchy@redhat.com - 2.4.11-1
- Initial package
