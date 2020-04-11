%global commit  f9356df
%global forgeurl https://gitlab.com/edouardklein/falsisign
%forgemeta

Name:           falsisign
Version:        0
Release:        20200411.0%{?dist}
Summary:        Make it look like a PDF has been hand signed and scanned

License:        WTF
URL:            %{forgeurl}
Source0:        %{forgesource}
BuildArch:      noarch

#BuildRequires:  
Requires:       ImageMagick
Requires:       file
Requires:       grep
Requires:       coreutils

%description
A script to make a PDF look like it's printed, signed, and then scanned again.
Because digital signatures are still not accepted in many places while
a signed and scanned printout is.

%prep
%setup -n %{name}-master

%build


%install
install -d %{buildroot}%{_bindir}/
cp -a falsisign.sh signdiv.sh %{buildroot}%{_bindir}/

%files
%license LICENSE
%doc README.org document.pdf falsiscan.png Signature_example.pdf Signature_guide.pdf
%{_bindir}/*



%changelog
* Sat Apr 11 2020 Miroslav Suchý <msuchy@redhat.com>
- initial packaging
