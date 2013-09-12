%global gem_name xmlhash

Name: rubygem-%{gem_name}
Version: 1.3.6
Release: 0%{?dist}
Summary: A small C module to parse a XML string into a ruby hash
Group: Development/Languages
License: MIT
URL: https://github.com/coolo/xmlhash
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(pkg-config)
Requires: libxml2
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby-devel 
BuildRequires: libxml2 libxml2-devel
BuildRequires: rubygem(pkg-config)
Provides: rubygem(%{gem_name}) = %{version}
#tests
BuildRequires: rubygem(json)
BuildRequires: rubygem(minitest)

%description
A small C module that wraps libxml2's xmlreader to parse a XML
string into a ruby hash.


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

mkdir -p %{buildroot}%{gem_extdir_mri}/lib/xmlhash
mv %{buildroot}%{gem_instdir}/lib/xmlhash/xmlhash.so %{buildroot}%{gem_extdir_mri}/lib/xmlhash/

# Remove the binary extension sources and build leftovers.
rm -rf ext
rm -rf %{buildroot}%{gem_instdir}/ext
rm -f %{buildroot}%{gem_instdir}/{.gemtest,.autotest,.travis.yml}

%check
pushd .%{gem_instdir}
testrb -Ilib test/test_xmlhash.rb
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/ext
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.txt

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/Manifest.txt
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Mon Aug 05 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.5-5
- 988818 - actually run the test suite
- 988818 - move README.txt to main package
- 988818 - summary-too-long
- 988818 - escape macro in comment

* Fri Jul 26 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.5-4
- BR minitest

* Fri Jul 26 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.5-3
- run test
- fix files section
- Remove the binary extension sources and build leftovers.
- add BuildRequires rubygem(pkg-config)
- require libxml2 and BR libxml2, libxml2-devel

* Fri Jul 26 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.5-2
- initial package

