%global gem_name scoped_search

Summary: Easily search your ActiveRecord models
Name: rubygem-%{gem_name}

Version: 2.6.1
Release: 0%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/wvanbergen/scoped_search/wiki
Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: rubygems
Requires: rubygem-activerecord >= 2.1.0
BuildRequires: ruby 
BuildRequires: rubygems
%if 0%{?rhel} == 6
Requires: ruby(abi) = %{rubyabi}
%else
Requires: ruby(release)
%endif
BuildRequires: rubygems-devel
BuildArch: noarch
Provides: rubygem(scoped_search) = %{version}

# for check section
%if 0%{?fedora} > 17
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(sqlite3)
%endif

%description
Scoped search makes it easy to search your ActiveRecord-based models. It will
create a named scope :search_for that can be called with a query string. It
will build an SQL query using the provided query string and a definition that
specifies on what fields to search. Because the functionality is built on
named_scope, the result of the search_for call can be used like any other
named_scope, so it can be chained with another scope or combined with
will_paginate. Because it uses standard SQL, it does not require any setup,
indexers or daemons. This makes scoped_search suitable to quickly add basic
search functionality to your application with little hassle. On the other hand,
it may not be the best choice if it is going to be used on very large data sets
or by a large user base.

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

%build

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
rm -rf %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/{.yardoc,.gitignore,.infinity_test,.travis.yml}
mv %{buildroot}%{gem_instdir}/{LICENSE,README.rdoc} ./

# https://github.com/wvanbergen/scoped_search/issues/26
chmod a-x %{buildroot}%{gem_instdir}/lib/scoped_search.rb

rm %{buildroot}%{gem_cache}

%check
pushd .%{gem_instdir}
# Get rid of Bundler, not needed on Fedora.
sed -i "/require 'bundler\/setup'/ d" spec/spec_helper.rb
# sqlite3-ruby and sqlite3 are identical rubygems, where the former is
# older name for the gem. Would be nice if upstream support both
# reincarnations.
# do not test on postgresql and ruby
sed '5,15d' -i spec/database.ruby.yml
#test does not work right now
#https://github.com/wvanbergen/scoped_search/issues/34
#or more precisly works only on F18+
%if 0%{?fedora} > 17
rspec spec
%endif
popd

%files
%doc LICENSE
%dir %{gem_instdir}
%{gem_instdir}/lib
%{gem_instdir}/init.rb
%{gem_instdir}/app
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile*
%{gem_instdir}/spec
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Miroslav Suchý <msuchy@redhat.com> 2.6.0-1
- rebase to 2.6.0 release (msuchy@redhat.com)

* Wed Apr 03 2013 Miroslav Suchý <msuchy@redhat.com> 2.5.1-1
- rebase to 2.5.1

* Tue Apr 02 2013 Miroslav Suchý <msuchy@redhat.com> 2.5.0-1
- rebase to 2.5.0

* Wed Mar 13 2013 Miroslav Suchý <msuchy@redhat.com> - 2.4.1-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Mar 11 2013 Miroslav Suchý <msuchy@redhat.com> 2.4.1-1
- rebase to 2.4.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Miroslav Suchý <msuchy@redhat.com> 2.4.0-5
- run test only on F18+ (msuchy@redhat.com)
- enable tests (msuchy@redhat.com)

* Tue Oct 30 2012 Miroslav Suchý <msuchy@redhat.com> 2.4.0-4
- do not run test on rhel6 at all due missing rspec (msuchy@redhat.com)

* Tue Oct 30 2012 Miroslav Suchý <msuchy@redhat.com> 2.4.0-3
- remove .travis.yml, add Gemfile.activerecord* (msuchy@redhat.com)

* Mon Oct 29 2012 Miroslav Suchý <msuchy@redhat.com> 2.4.0-2
- do not run test, because it is not working (msuchy@redhat.com)
- disable testing on other backend but sqllite (msuchy@redhat.com)
- update to recent scoped_search-2.4.0.gem (msuchy@redhat.com)

* Tue Oct 16 2012 Miroslav Suchý <msuchy@redhat.com> 2.4.0-1
- update to recent scoped_search-2.4.0.gem (msuchy@redhat.com)

* Wed Aug 15 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-10
- 847504 - move gemspec to -doc subpackage (msuchy@redhat.com)

* Wed Aug 15 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-9
- test suite is failing on F17 a lot - disable for now (msuchy@redhat.com)
- 847504 - use test suite (msuchy@redhat.com)
- 847504 - remove dot files in %%install section (msuchy@redhat.com)
- 847504 - use macro in SOURCE0 (msuchy@redhat.com)

* Tue Aug 14 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-8
- 847504 - put in front of chmod link to github issue (msuchy@redhat.com)
- 847504 - fix typo in summary (msuchy@redhat.com)

* Tue Aug 14 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-7
- 847504 - remove cached gem (msuchy@redhat.com)
- 847504 - correctly use dist tag (msuchy@redhat.com)
- 847504 - rewrap description (msuchy@redhat.com)

* Sun Aug 12 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-6
- fix spelling error (msuchy@redhat.com)
- module scoped_search.rb should not be executable (msuchy@redhat.com)

* Sun Aug 12 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-5
- buildroot is not needed (msuchy@redhat.com)
- change Group to valid item (msuchy@redhat.com)

* Fri Aug 10 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-4
- there is no need to require rubygems in some version (msuchy@redhat.com)

* Fri Aug 10 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-3
- there is no need to require rubygems in some version (msuchy@redhat.com)

* Thu Aug 09 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-2
- fix filelist (msuchy@redhat.com)
- create doc subpackage (msuchy@redhat.com)
- fix requirements (msuchy@redhat.com)

* Thu Aug 09 2012 Miroslav Suchý <msuchy@redhat.com> 2.3.7-1
- edit rubygem-scoped_search.spec according guidelines (msuchy@redhat.com)
- import rubygem-scoped_search.spec from foreman-rpms (msuchy@redhat.com)

