%define __autobuild__ 0
%define use_scl 0
%if %{use_scl}
%global scl %{use_scl}
%endif

%if %{__autobuild__}
%define version PKG_VERSION
%else
%define version 0.01
%endif
%define release %(/bin/date +"%Y%m%d.%H%M")
%define centos %(awk '/CentOS release [0-9]/ {print substr ($3,1,1)}' /etc/issue)

%define __module  XML-Hash-LX
%define __git     git://github.com/Mons/%{__module}
%define __dir     %{__module}

%{?scl:%scl_package package_name}
%{!?scl:%global pkg_name %{__module}}

Name:         %{?scl_prefix}perl-%{__module}
Version:      %{version}
Release:      %{release}
Summary:      Convert hash to xml and xml to hash using LibXML
Group:        Development/Libraries
License:      perl

BuildRequires: %{?scl_prefix}perl(XML::LibXML)
BuildRequires: %{?scl_prefix}perl(Module::Install)
BuildRequires: %{?scl_prefix}perl(Test::More)
BuildRequires: %{?scl_prefix}perl(Test::Pod::Coverage)
BuildRequires: %{?scl_prefix}perl(lib::abs)
BuildRequires: %{?scl_prefix}perl(Types::Serialiser)

Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%{?scl:Requires: %scl_runtime}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if %{__autobuild__}
Packager: BUILD_USER
Source0: %{__module}-GIT_TAG.tar.bz2
%else
Source0: %{__module}.tar.bz2
%endif

%description
Convert hash to xml and xml to hash using LibXML
%{lua:
if rpm.expand("%{__autobuild__}") == '1'
then
print("From tag: GIT_TAG\n")
print("Git hash: GITHASH\n")
print("Build by: BUILD_USER\n")
end}

%prep
rm -rf %{__module}
#%if %{__autobuild__}
%setup -q -n %{__module}
#%endif

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %buildroot
make pure_install PERL_INSTALL_ROOT=%buildroot
find %buildroot -type f -name .packlist -exec rm -f {} ';'
find %buildroot -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %buildroot/*

%check
make test

%clean

%files
%defattr(-,root,root,-)
%doc Changes README LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*.3pm*
