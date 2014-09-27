Name: nanoblogger
Version: 3.4.2
Release: 3%{?dist}

Summary: Small weblog engine for the UNIX command line
License: GPLv2+
Group: Applications/Internet

Url: http://nanoblogger.sourceforge.net/
BuildArch: noarch

Source: http://nanoblogger.sourceforge.net/downloads/%name-%version.tar.gz
Source1: nb.1

%description
NanoBlogger is a small weblog engine written in Bash for the command line. It
uses common UNIX tools such as cat, grep, and sed to create static HTML
content.

pros:

    * highly configurable and extensible
    * intuitive command line interface
    * easy drafting, editing, and management of entries
    * configurable amount of archiving by category, year, month, day, and entry
    * pagination
    * permanent and navigational links
    * templates and CSS style sheets for full control over layout
    * placeholders for easy template manipulation
    * support for multiple weblogs
    * support for multiple tags (categories)
    * support for both relative and absolute links
    * support for date manipulation of entries
    * Atom syndication (comes with 1.0 format)
    * RSS syndication (comes with RSS 1.0 and 2.0 formats)
    * plugins for calendar, recent entries, weblog status, etc.
    * plugins for text formatting (e.g. line breaks translate to HTML)
    * global (nb.conf) and per-weblog (blog.conf) configuration
    * intelligent build system that only rebuilds what's necessary
    * simple cache system for extra boost in speed
    * independent from java-script and server-side scripting (e.g. PHP)
    * independent from external database (stores data in flat-files)
    * includes user manual
    * multilingual support
    * multi-platform portability (just add bash and the required commands)
    * modular code base

cons:

    * slow (written in bash)
    * no comments (only available as add-on)
    * comes with a user manual
    * not easily upgradable

%prep
%setup -q

%build
sed -i 's/%%version/%{version}/g' nb
sed -i 's/^NB_BASE_DIR=/NB_BASE_DIR="/usr/share/nanoblogger"/g' nb
sed -i 's/^NB_DOC_DIR=/NB_DOC_DIR="/usr/share/doc/nanoblogger"/g' nb
sed -i 's/^NB_CFG_DIR/NB_CFG_DIR="/etc/nanoblogger"/g' nb

%install
mkdir -p %{buildroot}/%{_bindir}
cp nb %{buildroot}/%{_bindir}

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
cp nb.conf %{buildroot}/%{_sysconfdir}/%{name}

mkdir -p %{buildroot}/%{_datadir}/%{name}
cp -a default/ lang/ lib/ moods/ plugins/ welcome-to-nb.txt %{buildroot}/%{_datadir}/%{name}


install -D -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/nb.1

%files
%{_bindir}/nb
%config(noreplace) %{_sysconfdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/nb.1*

%doc ChangeLog README copyright docs/nanoblogger.html TODO

%changelog
* Sat Sep 27 2014 Miroslav Suchý <miroslav@suchy.cz> 3.4.2-3
- remove url_handler requires

* Sat Sep 27 2014 Miroslav Suchý <miroslav@suchy.cz> 3.4.2-2
- fix rpmlint issues

* Sat Sep 27 2014 Miroslav Suchý <miroslav@suchy.cz> 3.4.2-1
- repackage for 3.4.2

* Sat Jun 06 2009 Kirill Maslinsky <kirill@altlinux.org> 3.4-alt1.rc2
- Initial build for Sisyphus

