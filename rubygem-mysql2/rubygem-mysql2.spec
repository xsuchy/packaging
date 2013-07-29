%global gem_name mysql2

Name: rubygem-%{gem_name}
Version: 0.3.13
Release: 2%{?dist}
Summary: A simple, fast Mysql library for Ruby, binding to libmysql
Group: Development/Languages
License: MIT
URL: http://github.com/brianmario/mysql2
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: mysql
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby ruby-devel
BuildRequires: mysql mysql-devel
Provides: rubygem(%{gem_name}) = %{version}

%description
The Mysql2 gem is meant to serve the extremely common use-case of connecting,
querying and iterating on results. Some database libraries out there serve as
direct 1:1 mappings of the already complex C API's available. This one is not.

It also forces the use of UTF-8 [or binary] for the connection [and all strings
in 1.9, unless Encoding.default_internal is set then it'll convert from UTF-8
to that encoding] and uses encoding-aware MySQL API calls where it can.

The API consists of two classes:

Mysql2::Client - your connection to the database

Mysql2::Result - returned from issuing a #query on the connection. It includes
Enumerable.

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

mkdir -p %{buildroot}%{gem_extdir_mri}/lib/mysql2
mv %{buildroot}%{gem_instdir}/lib/mysql2/mysql2.so %{buildroot}%{gem_extdir_mri}/lib/mysql2/

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{geminstdir}/ext


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/ext
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/support/
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/MIT-LICENSE


%files doc
%doc %{gem_docdir}
%{gem_instdir}/spec/
%{gem_instdir}/examples/

%changelog
* Fri Jul 26 2013 Miroslav Suchý <msuchy@redhat.com> 0.3.13-2
- initial package

