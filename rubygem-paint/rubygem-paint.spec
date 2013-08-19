%global gem_name paint

Name: rubygem-%{gem_name}
Version: 0.8.6
Release: 1%{?dist}
Summary: Terminal painter
Group: Development/Languages
License: MIT
URL: https://github.com/janlelis/paint
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby >= 1.8.7
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}
#tests
BuildRequires: rubygem-rspec

%description
Paint manages terminal colors and effects for you. It combines the strengths
of term-ansicolor, rainbow and other similar projects into a simple to use,
however still flexible terminal colorization gem with no core extensions by
default.


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
cp -pr spec/ ./%{gem_instdir}
pushd ./%{gem_instdir}
rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%exclude %{gem_instdir}/.gemtest

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/CHANGELOG.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec

%changelog
* Mon Aug 19 2013 Miroslav Suchý <msuchy@redhat.com> 0.8.6-1
- initial package

