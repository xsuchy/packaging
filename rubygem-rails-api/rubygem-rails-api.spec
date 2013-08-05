%global gem_name rails-api

Name: rubygem-%{gem_name}
Version: 0.1.0
Release: 5%{?dist}
Summary: Rails for API only Applications
Group: Development/Languages
License: MIT
URL: https://github.com/rails-api/rails-api
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://github.com/rails-api/rails-api/issues/99
Source1: LICENSE
Requires: ruby(release)
Requires: ruby(rubygems) >= 1.3.6
Requires: rubygem(actionpack) >= 3.2.11
Requires: rubygem(railties) >= 3.2.11
Requires: rubygem(tzinfo) => 0.3.31
Requires: rubygem(tzinfo) < 0.4
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}
#test
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rails)

%description
Rails::API is a subset of a normal Rails application,
created for applications that don't require all
functionality that a complete Rails application provides.


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

cp -a %{SOURCE1} ./
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
sed -i '/require.*bundler/d' test/test_helper.rb
#generators are omited because it generate application which use bundler
testrb -v -Ilib -Itest test/api_application/*_test.rb test/api_controller/*_test.rb
popd

%files
%dir %{gem_instdir}
%{_bindir}/rails-api
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.md
%doc LICENSE

%files doc
%doc %{gem_docdir}
%{gem_instdir}/test

%changelog
* Mon Jul 29 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.0-5
- BR rails

* Mon Jul 29 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.0-4
- BR minitest

* Mon Jul 29 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.0-3
- add tests

* Mon Jul 29 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.0-2
- initial package

