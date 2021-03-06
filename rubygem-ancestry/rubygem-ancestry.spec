%global gem_name ancestry
%global githash bfcbb57

Name: rubygem-%{gem_name}
Version: 2.1.0
Release: 1%{?dist}
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

#for tests, which are not present in gem file
# git clone git@github.com:stefankroes/ancestry.git && cd ancestry
# git archive --format=tar %{githash} test | gzip > %{name}-%{version}-test.tar.gz
Source1: %{name}-%{version}-test.tar.gz
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(test-unit)
BuildRequires: rubygems
BuildRequires: sqlite
BuildRequires: rubygem(sqlite3)
 
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
pushd ./%{gem_instdir}
tar zxf %{SOURCE1}
sed -i '/require.*bundler/d' test/environment.rb
mkdir log
touch log/test.log
cat <<EOF > test/database.yml
sqlite3:
  adapter: sqlite3
  database: ":memory:"
EOF
testrb -v -Ilib -Itest test/*_test.rb
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README.rdoc
%exclude %{gem_instdir}/init.rb
%exclude %{gem_instdir}/install.rb

%files doc
%doc %{gem_docdir}
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Mon May 26 2014 Miroslav Suchý <msuchy@redhat.com> 2.1.0-1
- rebase to ancestry-2.1.0

* Mon Aug 26 2013 Miroslav Suchý <msuchy@redhat.com> 2.0.0-5
- enable test
- mark README and LICENSE as doc

* Tue Aug 13 2013 Miroslav Suchý <msuchy@redhat.com> 2.0.0-4
- fix typos 

* Tue Aug 13 2013 msuchy@redhat.com - 2.0.0-1
- Initial package
