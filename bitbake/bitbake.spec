Summary: Build system for Yocto and OpenEmbedded
Name: bitbake
Version: 1.48.1
Release: 0%{?dist}
# see LICENSE for details
License: GPLv2 and MIT and BSD and zlib and OFL
Source0: http://git.openembedded.org/bitbake/snapshot/%{name}-%{version}.tar.gz
URL: http://git.openembedded.org/bitbake/
#BuildRequires: python-devel, xmlto-tex, lynx
BuildArch: noarch

# documentation
BuildRequires: sphinx

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

%build
#CFLAGS="$RPM_OPT_FLAGS" python3 setup.py build

# Generating docs
make -C doc/manual all

iconv -f iso-8859-1 -t utf-8 doc/manual/xhtml/docbook.css > docbook.css.tmp
touch -r doc/manual/xhtml/docbook.css docbook.css.tmp
mv docbook.css.tmp doc/manual/xhtml/docbook.css

%install
#python3 setup.py install -O1 --skip-build --root %{buildroot}

# We strip bad shebangs (/usr/bin/env) instead of fixing them
# since these files are not executable anyways
find %{buildroot}/%{python3_sitelib} -name '*.py' \
  -exec grep -q '^#!' '{}' \; -print | while read F
do
  awk '/^#!/ {if (FNR == 1) next;} {print}' $F >chopped
  touch -r $F chopped
  mv chopped $F
done

# Removing extra docs
rm -rf %{buildroot}%{_docdir}

make -C doc html
make html
mkdir -p %{buildroot}%{_pkgdocdir}
cp -a html/_build/html/* %{buildroot}%{_pkgdocdir}/


%files
#%doc doc/COPYING.GPL doc/manual/xhtml/ doc/manual/txt/usermanual.txt doc/manual/pdf/usermanual.pdf
#%{_bindir}/bbimage
#%{_bindir}/bitbake
#%{_datadir}/bitbake/
#%{python333_sitelib}/*

%files doc
%{_pkgdocdir}

%changelog
