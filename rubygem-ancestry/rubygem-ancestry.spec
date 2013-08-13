%global gem_name ancestry

Name: rubygem-%{gem_name}
Version: 2.0.0
Release: 3%{?dist}
Summary: Organize ActiveRecord model into a tree structure
Group: Development/Languages
License: MIT
URL: http://github.com/stefankroes/ancestry
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(activerecord) >= 3.0.0
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Ancestry allows the records of a ActiveRecord model to be organized in a tree
structure, using a single, intuitively formatted database column. It exposes
all the standard tree structure relations (ancestors, parent, root, children,
siblings, descendants) and all of them can be fetched in a single sql query.
Additional features are named_scopes, integrity checking, integrity restoration,
arrangement of (sub)tree into hashes and different strategies for dealing with
orphaned records.

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

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
sed -i '/require.*bundler/d' test/environment.rb
testrb -Ilib -Itest has_ancestry_test.rb
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/MIT-LICENSE
%{gem_instdir}/README.rdoc
%exclude %{gem_instdir}/init.rb
%exclude %{gem_instdir}/install.rb

%files doc
%doc %{gem_docdir}
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Tue Aug 13 2013 Miroslav Suchý <msuchy@redhat.com> 2.0.0-3
- run tests

* Tue Aug 13 2013 Miroslav Suchý <msuchy@redhat.com> 2.0.0-2
- initial package

* Tue Aug 13 2013 msuchy@redhat.com - 2.0.0-1
- Initial package
