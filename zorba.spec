%define _disable_lto 1

# these are required by libsimplestore.so.0.9.21 and/or libzorba.so.0.9.21 but has no soname(!)
%define _provides_exceptions devel(libzorbaerrors\\|libzorbaerrors.so\\|devel(libzorbatypes\\|libzorbatypes.so\\|devel(libzorbautils\\|libzorbautils.so
%define _requires_exceptions devel(libzorbaerrors\\|libzorbaerrors.so\\|devel(libzorbatypes\\|libzorbatypes.so\\|devel(libzorbautils\\|libzorbautils.so

%define major %{version}.0

Summary:	A general purpose XQuery processor implementing in C++
Name:		zorba
Version:	3.1
Release:	1
Group:		System/Libraries
License:	Apache License
URL:		https://www.zorba-xquery.com/
Source0:	https://github.com/28msec/zorba/archive/refs/tags/%{version}.tar.gz
Patch0:		zorba-3.1-cmake-fixes.patch
Patch1:		https://src.fedoraproject.org/rpms/zorba/raw/f29/f/zorba-icu-namespace.patch
Patch2:		https://src.fedoraproject.org/rpms/zorba/raw/f29/f/zorba-check-dll_path.patch
Patch3:		https://src.fedoraproject.org/rpms/zorba/raw/f29/f/zorba-missing-includes.patch
Patch4:		zorba-3.1-icu-fixes.patch
BuildRequires:	boost-devel >= 1.32
BuildRequires:	cmake >= 2.4 
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(libxml-2.0) >= 2.2.16
BuildRequires:	pkgconfig(xerces-c)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	ninja
BuildRequires:	bison
BuildRequires:	flex

%description
Zorba is a general purpose XQuery processor implementing in C++ the W3C family
of specifications. It is not an XML database. The query processor has been
designed to be embeddable in a variety of environments such as other
programming languages extended with XML processing capabilities, browsers,
database servers, XML message dispatchers, or smartphones. Its architecture
employes a modular design, which allows customizing the Zorba query processor
to the environment's needs. In particular the architecture of the query
processor allows a pluggable XML store (e.g. main memory, DOM stores,
persistent disk-based large stores, S3 stores). Zorba runs on most platforms
and is available under the Apache license v2.

%prep
%autosetup -p1
%cmake -DCMAKE_INSTALL_DO_STRIP=0 -DCMAKE_SKIP_BUILD_RPATH=1  --debug-output .. -G Ninja

%build
%ninja_build -C build

%install
#touch build/doc/python/examples/python_test.py
#makeinstall_std INSTALL="install -p"  -C build
%ninja_install -C build

%libpackages

cat >>%{specpartsdir}/%{mklibname -d zorba_simplestore}.specpart <<EOF
%doc %{_docdir}/%{name}-%{major}
%{_includedir}/zorba
%{_includedir}/*.h
%{_includedir}/util/*.h
%{_datadir}/cmake/zorba-%{major}
EOF

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/testdriver
%{_datadir}/zorba
%{_datadir}/zorba-%{major}
%{_prefix}/lib/zorba
