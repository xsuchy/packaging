%global targetdir %{_prefix}/lib/%{name}
%global githash 0ebeb69

Name:		slimmerjs
Version:	0.9.6
Release:	1%{?dist}
Summary:	A scriptable browser like PhantomJS, based on Firefox

License:	MPLv2.0
URL:		https://github.com/laurentj/slimerjs/
#git archive --format=tar --prefix=slimerjs/ 0ebeb69 | gzip > slimerjs-0ebeb69.tar.gz
Source0:	slimerjs-0ebeb69.tar.gz
BuildArch:	noarch

BuildRequires:	xulrunner
BuildRequires:	zip
BuildRequires:	sed
BuildRequires:	xorg-x11-server-Xvfb
Requires:	xulrunner
Recommends: xorg-x11-server-Xvfb

%description
SlimerJS is a scriptable browser. It allows you to manipulate a web page with
an external Javascript script: opening a webpage, clicking on links, modifying
the content... It is useful to do functional tests, page automation, network
monitoring, screen capture etc.

It is a tool like PhantomJs, except that it runs Gecko instead of Webkit, and
it is not (yet) natively headless. However, it can be headless with the use of
xvfb under Linux or MacOS.

%prep
%setup -q -n slimerjs


%build
pushd src
mkdir -p xulrunner
ln -s /usr/bin/xulrunner xulrunner/xulrunner
BUILDDATE=`date +%Y%m%d`
sed -i -e "s/BuildID=.*/BuildID=$BUILDDATE/g" application.ini
# zip chrome files into omni.ja
zip -r ./omni.ja chrome/ components/ defaults/ modules/ chrome.manifest --exclude @package_exclude.lst
popd

%install
mkdir -p %{buildroot}%{targetdir}/xulrunner
mkdir -p %{buildroot}%{_bindir}
ln -s %{targetdir}/slimerjs %{buildroot}%{_bindir}/slimerjs

pushd src
cp -a application.ini xulrunner omni.ja vendors slimerjs %{buildroot}%{targetdir}/

mkdir -p %{buildroot}%{targetdir}/chrome/
cp -a chrome/icons %{buildroot}%{targetdir}/chrome/

# zip chrome files into omni.ja
zip -r %{buildroot}%{targetdir}/omni.ja chrome/ components/ defaults/ modules/ chrome.manifest --exclude @package_exclude.lst

%check
xvfb-run src/slimerjs  test/launch-main-tests.js | grep ' 3 failures'
#xvfb-run src/slimerjs  test/launch-rendering-tests.js

%files
%doc README.md docs API_COMPAT.md BUILD.md CONTRIBUTING.md CREDITS.md examples/
%license LICENSE
%{_bindir}/slimerjs
%{targetdir}


%changelog
* Thu Oct 22 2015 Miroslav Suchý <msuchy@redhat.com> 0.9.6-1
- initial packaging


