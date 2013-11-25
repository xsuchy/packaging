%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name unicode-display_width

Summary: Support for east_asian_width string widths
Name: %{?scl_prefix}rubygem-%{gem_name}

Version: 0.1.1
Release: 8%{dist}
Group: Development/Languages
License: MIT
URL: https://github.com/janlelis/unicode-display_width
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fedora} > 18
Requires: %{?scl_prefix}ruby(release)
%else
Requires: %{?scl_prefix}ruby(abi) = 1.9.1
%endif
BuildRequires: %{?scl_prefix}rubygems-devel
BuildRequires: %{?scl_prefix}rubygems
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%global gembuilddir %{buildroot}%{gem_dir}

%description
This gem adds String#display_size to get the display size of a string using
EastAsianWidth.txt.

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}
%setup -n %{gem_name}-%{version} -T -D -q
%{?scl:scl enable %{scl} "}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:"}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} "}
gem build %{gem_name}.gemspec
%{?scl:"}

%{?scl:scl enable %{scl} "}
%gem_install
%{?scl:"}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
rm -rf %{buildroot}%{gem_instdir}/.yardoc

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/data
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/.gemspec

%changelog
* Fri Sep 13 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.1-8
- generate gem again during buildtime

* Mon Aug 19 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.1-7
- change group
- summary should not end with dot

* Thu Jul 04 2013 Dominic Cleal <dcleal@redhat.com> 0.1.1-6
- change ruby(abi) to ruby(release) for F19+ (dcleal@redhat.com)
- delete all zero sized tito.props (msuchy@redhat.com)
- with recent tito you do not need SCL meta package (msuchy@redhat.com)

* Thu Mar 14 2013 Miroslav Suchý <msuchy@redhat.com> 0.1.1-4
- new package built with tito

* Mon Sep 10 2012 Miroslav Suchý <msuchy@redhat.com> 0.1.1-3
- remove yardoc (msuchy@redhat.com)

* Mon Sep 10 2012 Miroslav Suchý <msuchy@redhat.com> 0.1.1-2
- new package built with tito

