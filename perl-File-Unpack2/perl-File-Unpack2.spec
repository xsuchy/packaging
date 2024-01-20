%global commit 4bcdc19ca9a2a5b9817e3e501d0018b58bf577d0
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           perl-File-Unpack2
Version:        1.0
Release:        %autorelease
Summary:        Strong archive file unpacker, based on mime-types

# contrib/stringsx.c: MIT OR GPL-1.0-or-later
# contrib/stringsx.pl: MIT OR GPL-1.0-or-later
# file_unpack2.pl: GPL-1.0-or-later OR Artistic-1.0-Perl
# Makefile.PL: GPL-1.0-or-later OR Artistic-1.0-Perl
# LICENSES/MIT.txt: MIT
# README: GPL-1.0-or-later OR Artistic-1.0-Perl
# Unpack2.pm: GPL-1.0-or-later OR Artistic-1.0-Perl
License:        (MIT OR GPL-1.0-or-later) AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
# wget https://github.com/openSUSE/perl-File-Unpack2/archive/%%{commit}/%%{name}-%%{shortcommit}.tar.gz
# tar axf %%{name}-%%{shortcommit}.tar.gz
# rm -rf perl-File-Unpack2-%%{commit}/t
# tar caf %%{name}-%%{shortcommit}-repackaged.tar.gz perl-File-Unpack2-%%{commit}
Source:         %{name}-%{shortcommit}-repackaged.tar.gz
URL:            https://github.com/openSUSE/perl-File-Unpack2

BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  coreutils
BuildRequires:  perl-podlators

#BuildRequires:  perl(Test::CheckManifest)
#BuildRequires:  perl(Test::More)
#BuildRequires:  perl(Test::Pod)
#BuildRequires:  perl(Test::Pod::Coverage)

BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::LibMagic)
BuildRequires:  perl(File::MimeInfo::Magic)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Temp)

BuildRequires:  perl(Compress::Raw::Lzma)
# (provider perl-Compress-Raw-Zlib is obsoleted by installed perl)
BuildRequires:  perl(BSD::Resource)
BuildRequires:  perl(Compress::Raw::Bzip2)
BuildRequires:  perl(Compress::Raw::Zlib) >= 2.024
BuildRequires:  perl(Filesys::Statvfs)
BuildRequires:  perl(IPC::Run)
BuildRequires:  perl(JSON)
BuildRequires:  perl(String::ShellQuote)
BuildRequires:  perl(Text::Sprintf::Named)
# shared-mime-info is a dependency of perl-File-MimeInfo
# file is a dependency of perl-File-LibMagic
BuildRequires:  fdupes
BuildRequires:  file >= 5.03
BuildRequires:  shared-mime-info >= 0.60

Requires:       perl(File::LibMagic)
Requires:       perl(File::MimeInfo::Magic)

Requires:       perl(Compress::Raw::Lzma)
Requires:       perl(Compress::Raw::Bzip2)
Requires:       file >= 5.03
Requires:       shared-mime-info >= 0.60
Requires:       perl(BSD::Resource)
Requires:       perl(Compress::Raw::Zlib) >= 2.024
Requires:       perl(Filesys::Statvfs)

## refer to Unpack.pm:@builtin_mime_handlers and to the helper subdirectory
## to see what we might need:
# grep '# Requires: ' Unpack.pm helper/*

BuildRequires:  xz
Requires:       xz

BuildRequires:  lzip
Requires:       lzip

BuildRequires:  poppler-utils
Requires:       poppler-utils

## The following BuildRequires is for testing existance only.
## If you cannot provide a package, you may remove it from both BuildRequires 
## and Requires, and move it over to Recommends.
#BuildRequires:  binutils
#BuildRequires:  bzip2
#BuildRequires:  cabextract
#BuildRequires:  cpio
#BuildRequires:  genisoimage
#BuildRequires:  gzip
#BuildRequires:  p7zip
#BuildRequires:  rpm
#BuildRequires:  sharutils
#BuildRequires:  tar
#BuildRequires:  unzip
Requires:       binutils
Requires:       bzip2
Requires:       cabextract
Requires:       cpio
Requires:       genisoimage
Requires:       gzip
Requires:       p7zip-plugins
Requires:       rpm
Requires:       sharutils
Requires:       tar
Requires:       unzip
Recommends:     unrar poppler-utils xz upx antiword

Recommends:     file-unpack == %version

#tests
#BuildRequires:  perl(FindBin)

%description
File::Unpack2 is an unpacker for archives and files
(bz2/gz/zip/tar/cpio/iso/rpm/deb/cab/lzma/7z/rar/...).  We call
it strong, because it is not fooled by file suffixes, or multiply wrapped packages.
It reliably detects mime-types and recursivly descends into each archive found
until it finally exposes all unpackable payload contents. 
A precise logfile can be written, describing mimetypes and unpack actions.
Most of the known archive file formats are supported. Shell-script-style
plugins can be added to support additinal formats.

%package -n file-unpack
Summary:        Command line tool to unpack anything
Requires:       %{name}%{?_isa} == %{version}-%{release}
License:        MIT OR GPL-1.0-or-later OR (GPL-1.0-or-later OR Artistic-1.0-Perl)

%description -n file-unpack
/usr/bin/file-unpack is a trivial command line frontend that
ships with the File::Unpack perl module.

%prep
%autosetup -n %{name}-%{commit}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

(cd contrib && %{make_build} stringsx)

%install
%{make_install}
mv %{buildroot}/usr/bin/{file_unpack,file-unpack} || :
install -d       %{buildroot}/usr/share/File-Unpack/helper/
install helper/* %{buildroot}/usr/share/File-Unpack/helper/

%fdupes %{buildroot}/usr/share/File-Unpack/

ln -s file-unpack %{buildroot}/%{_bindir}/file_unpack
ln -s file-unpack %{buildroot}/%{_bindir}/unpack-file
ln -s file-unpack %{buildroot}/%{_bindir}/unpack-file-deep
ln -s file-unpack %{buildroot}/%{_bindir}/unpack-deep
ln -s file-unpack %{buildroot}/%{_bindir}/file-unpack-deep

## CAUTION: a line beginning with . is a macro-expanded by nroff.
# echo .nf > file-unpack.1
# perl -Iblib/lib file-unpack.pl --help >> file-unpack.1 && true
# rm -rf file-unpack.1

cat <<EOF> file-unpack.pod
=pod

=head1 SYNOPSIS
EOF

perl file-unpack2.pl --help >> file-unpack2.pod && true

cat <<EOF1>> file-unpack2.pod
=head1 REFERENCES

See also C<perldoc File::Unpack>
EOF1

pod2man file-unpack2.pod > file-unpack2.1
rm file-unpack2.pod

echo <<EOF2>> MANIFEST
file-unpack2.1
EOF2

install -m0644 -D file-unpack2.1 %{buildroot}/%_mandir/man1/file-unpack2.1
ln -s file-unpack.1 %{buildroot}/%_mandir/man1/unpack_file2.1
install -m0755 -D contrib/stringsx %{buildroot}/%_bindir/stringsx
rm contrib/stringsx # so that the Manifest in make check is not confused.


%{_fixperms} %{buildroot}/*

%check
#export RELEASE_TESTING=1
#%{__make} test

%files
%doc README Changes
%{perl_vendorlib}/File
%dir /usr/share/File-Unpack
/usr/share/File-Unpack
%doc %_mandir/man3/File::Unpack2.3pm*

%files -n file-unpack
%{_bindir}/file-unpack-deep
%{_bindir}/file_unpack
%{_bindir}/file_unpack2
%{_bindir}/stringsx
%{_bindir}/unpack-deep
%{_bindir}/unpack-file
%{_bindir}/unpack-file-deep
%_mandir/man1/file-unpack.1*
%_mandir/man1/file_unpack2.1*
%_mandir/man1/unpack_file.1*
%license LICENSES/MIT.txt

%changelog
%autochangelog
