Summary: Build system for Yocto and OpenEmbedded
Name: bitbake
Version: 1.48.1
Release: 0%{?dist}
# see LICENSE for details
License: GPLv2 and MIT and BSD and zlib and OFL
Source0: http://git.openembedded.org/bitbake/snapshot/%{name}-%{version}.tar.gz
URL: http://git.openembedded.org/bitbake/
Patch0: remove.path.insert.patch
Patch1: path.mangling.path
BuildArch: noarch

Requires: python3-beautifulsoup4
Requires: python3-ply
Requires: python3-progressbar2
Recommends: python3-pytz

BuildRequires: python3-devel
# documentation
BuildRequires: sphinx
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx_rtd_theme

%description
BitBake is a generic task execution engine that allows shell and Python tasks
to be run efficiently and in parallel while working within complex inter-task
dependency constraints. One of BitBake's main users, OpenEmbedded, takes this
core and builds embedded Linux software stacks using a task-oriented approach.

For information about Bitbake, see the OpenEmbedded website:
 http://www.openembedded.org/

Bitbake plain documentation can be found under the doc directory or its integrated
html version at the Yocto Project website:
  http://yoctoproject.org/documentation

%package doc
Summary: Documentation for BitBake

%description doc
Documentation for BitBake in HTML format.

%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
# this is symbolic link, recreate it later
rm -f bin/bitbake-dumpsig

# remove bundled modules
# beautifulsoup4
rm -rf lib/bs4
# ply
rm -rf lib/ply
# progressbar2
rm -rf progressbar
# FIXME - the following modules are bundled but not yet packaged
# simplediff



# this is not needed when we put modules on propper place
for i in bin/*; do
  sed -i '/sys.path.insert/d' "$i"
done
# bitbake has the insert on two lines
sed -i "/'lib'))/d" bin/bitbake

make -C doc html

#iconv -f iso-8859-1 -t utf-8 doc/manual/xhtml/docbook.css > docbook.css.tmp
#touch -r doc/manual/xhtml/docbook.css docbook.css.tmp
#mv docbook.css.tmp doc/manual/xhtml/docbook.css

%install
mkdir -p %{buildroot}%{_bindir}
cp -a bin/* %{buildroot}%{_bindir}
# recreate the symlink which we deleted in prep
ln -s bitbake-diffsigs %{buildroot}%{_bindir}/bitbake-dumpsig

mkdir -p %{buildroot}%{python3_sitelib}
cp -a lib/* %{buildroot}%{python3_sitelib}/

# Removing extra docs
rm -rf %{buildroot}%{_docdir}

mkdir -p %{buildroot}%{_pkgdocdir}
cp -a doc/_build/html/* %{buildroot}%{_pkgdocdir}/

mkdir -p %{buildroot}%{_sysconfdir}/bitbake
cp -a conf/bitbake.conf %{buildroot}%{_sysconfdir}/bitbake/

%files
%doc AUTHORS ChangeLog README
%license LICENSE LICENSE.GPL-2.0-only LICENSE.MIT
%dir %{_sysconfdir}/bitbake
%config(noreplace) %{_sysconfdir}/bitbake/bitbake.conf
%{_bindir}/*
%{python3_sitelib}/*

%files doc
%{_pkgdocdir}

%changelog
