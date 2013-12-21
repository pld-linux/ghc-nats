#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	nats
Summary:	Haskell 98 natural numbers
Summary(pl.UTF-8):	Liczby naturalne dla Haskella 98
Name:		ghc-%{pkgname}
Version:	0.1.2
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/nats
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	86b609392a5272aa0eb4c66d3bbd4172
URL:		http://hackage.haskell.org/package/nats
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 2
BuildRequires:	ghc-base < 10
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 2
BuildRequires:	ghc-base-prof < 10
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 2
Requires:	ghc-base < 10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Haskell 98 natural numbers.

%description -l pl.UTF-8
Liczby naturalne dla Haskella 98.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 2
Requires:	ghc-base-prof < 10

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.markdown LICENSE README.markdown
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSnats-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSnats-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric/Natural.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric/Natural
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric/Natural/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSnats-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric/Natural.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Numeric/Natural/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
