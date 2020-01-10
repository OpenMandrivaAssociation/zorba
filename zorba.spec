%define _disable_ld_as_needed 1
%define _disable_ld_no_undefined 1

# these are required by libsimplestore.so.0.9.21 and/or libzorba.so.0.9.21 but has no soname(!)
%define _provides_exceptions devel(libzorbaerrors\\|libzorbaerrors.so\\|devel(libzorbatypes\\|libzorbatypes.so\\|devel(libzorbautils\\|libzorbautils.so
%define _requires_exceptions devel(libzorbaerrors\\|libzorbaerrors.so\\|devel(libzorbatypes\\|libzorbatypes.so\\|devel(libzorbautils\\|libzorbautils.so

%define major 0.9.21
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	A general purpose XQuery processor implementing in C++
Name:		zorba
Version:	0.9.21
Release:	%mkrel 4
Group:		System/Libraries
License:	Apache License
URL:		http://www.zorba-xquery.com/
Source0:	http://downloads.sourceforge.net/zorba/%{name}-%{version}.tar.gz
Patch0:		zorba-missing-includes.patch
BuildRequires:	boost-devel >= 1.32
BuildRequires:	cmake >= 2.4 
BuildRequires:	icu-devel >= 2.6
BuildRequires:	libxml2-devel >= 2.2.16
BuildRequires:	python-devel
BuildRequires:	ruby-devel
BuildRequires:	swig
BuildRequires:	xerces-c28-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	%{libname}
Summary:	A general purpose XQuery processor implementing in C++
Group:		System/Libraries

%description -n	%{libname}
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

This package contains the shared Zorba libraries.

%package -n	%{develname}
Summary:	Development files for Zorba
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
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

This package contains the development files for Zorba.

%package -n	python-zorba
Summary:	Zorba Python module
Group:		Development/Python
Requires:	%{libname} = %{version}

%description -n	python-zorba
Provides Python module to use Zorba API

%package -n	ruby-zorba
Summary:	Zorba Ruby module
Group:		Development/Ruby
Requires:	%{libname} = %{version}

%description -n	ruby-zorba
Provides ruby module to use Zorba API

%prep

%setup -q
%autopatch -p1

%build
%cmake -DCMAKE_INSTALL_DO_STRIP=0 -DCMAKE_SKIP_BUILD_RPATH=1  --debug-output ..
%make

%install
rm -rf %{buildroot}

touch build/doc/python/examples/python_test.py
%makeinstall_std INSTALL="install -p"  -C build

%if "%{_lib}" == "lib64"
install -d %{buildroot}%{_libdir}
mv %{buildroot}%{_prefix}/lib/*.so.%{major} %{buildroot}%{_libdir}/
mv %{buildroot}%{_prefix}/lib/*.so %{buildroot}%{_libdir}/
%endif

# BORK!!!
install -m0755 build/src/zorbaerrors/libzorbaerrors.so %{buildroot}%{_libdir}/
install -m0755 build/src/zorbatypes/libzorbatypes.so %{buildroot}%{_libdir}/
install -m0755 build/src/zorbautils/libzorbautils.so %{buildroot}%{_libdir}/

# cleanup
rm -rf %{buildroot}%{_datadir}/doc/%{name}-%{version}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS.txt NOTICE.txt README.txt
%attr(0755,root,root) %{_libdir}/*.so.%{major}
%attr(0755,root,root) %{_libdir}/libzorbaerrors.so
%attr(0755,root,root) %{_libdir}/libzorbatypes.so
%attr(0755,root,root) %{_libdir}/libzorbautils.so

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}/%{name}
%dir %{_includedir}/%{name}/simplestore
%attr(0644,root,root) %{_includedir}/%{name}/%{name}/*.h
%attr(0644,root,root) %{_includedir}/%{name}/simplestore/*.h
%attr(0644,root,root) %{_libdir}/*.so
%exclude %{_libdir}/libzorbaerrors.so
%exclude %{_libdir}/libzorbatypes.so
%exclude %{_libdir}/libzorbautils.so

%files -n python-zorba
%defattr(-,root,root)
%attr(0755,root,root) %{python_sitelib}/_zorba_api.so
%attr(0644,root,root) %{python_sitelib}/zorba_api.*

%files -n ruby-zorba
%defattr(-,root,root)
%attr(0755,root,root) %{ruby_sitearchdir}/zorba_api.so

