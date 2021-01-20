%global commit cc8cba9bec12d2fb4338f50412485f436b4c35b1
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Name:           email2domain
Summary:        Implements RFC 7929, section 3
Release:        1%{?dist}
Version:        0.1.%{shortcommit}

License:        FIXME
URL:            https://pagure.io/email2domain/
# git clone https://pagure.io/email2domain.git
# cd email2domain
# git archive %{shortcommit} -o email2domain-%{shortcommit}.tar.gz
Source0:  email2domain-%{shortcommit}.tar.gz


BuildRequires:  python3-devel
Requires:       python3

%description
Converts email to DNS record.

Implements RFC 7929, section 3
https://tools.ietf.org/html/rfc7929#section-3


%prep
%setup -c


%build
# nothing to do here

%install
mkdir -p %{buildroot}/%{_bindir}
cp -a email2domain.py %{buildroot}/%{_bindir}/email2domain

%check
python3 -m unittest email2domain.py

%files
#%license add-license-file-here
%{_bindir}/email2domain



%changelog
* Wed Jan 20 16:35:14 CET 2021 msuchy <msuchy@redhat.com>
- initial package
