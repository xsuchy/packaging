Name: nanoblogger-extra
Version: 3.4.2
Release: 2%{?dist}

Summary: Nanoblogger plugins
License: GPLv2+
Group: Applications/Internet

Url: http://nanoblogger.sourceforge.net/
BuildArch: noarch

Source: http://nanoblogger.sourceforge.net/downloads/%name-%version.tar.gz
Patch0: bash-completion-have.patch
Requires: nanoblogger

%description
NanoBlogger is a small weblog engine written in Bash for the command line. It
uses common UNIX tools such as cat, grep, and sed to create static HTML
content.

This package contains additional plugins and translations for this weblog
engine.

%prep
%setup -q -n nanoblogger-%{version}

%build

%install
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d/
cp -a docs/examples/nanoblogger.bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d/

mkdir -p %{buildroot}/%{_datadir}/%{name}
cp -a default/ lang/ plugins/ %{buildroot}/%{_datadir}/%{name}

%files
%doc ChangeLog README COPYING
%doc docs/nanoblogger_*.html
%{_sysconfdir}/bash_completion.d/nanoblogger.bash_completion
%{_datadir}/%{name}

%changelog
* Sat Sep 27 2014 Miroslav Suchý <miroslav@suchy.cz> 3.4.2-2
- fix name in setup phase

* Sat Sep 27 2014 Miroslav Suchý <miroslav@suchy.cz> 3.4.2-1
- initial package

