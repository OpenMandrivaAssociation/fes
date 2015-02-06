# http://trac.sagemath.org/sage_trac/ticket/13162

Name:		fes
Version:	0.1
Release:	2
License:	GPLv3+
Group:		Sciences/Mathematics
Summary:	Fast Exhaustive Search
URL:		http://www.lifl.fr/~bouillag
Source0:	http://www.lifl.fr/~bouillag/download/fes-0.1.spkg
Source1:	%{name}.rpmlintrc
ExclusiveArch:	x86_64
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{py_requires -d}
BuildRequires:	texlive
BuildRequires:	texlive-collection-science
Patch0:		%{name}-dynamic.patch

%description
This external library implements an efficient implement of exhaustive
search to solve systems of low-degree boolean equations. Exhaustive
search is asymptotically faster than computing a Groebner basis,
except in special cases. This particular implementation is
particularly efficient (in the good cases it tests 3 candidate
solutions per CPU cycle on each core).

%package	devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{version}-%{release}

%description	devel
This package contains the header files and development documentation
for %{name}.

%prep
%setup -q
%patch0 -p1

pushd src
    autoreconf -ifs
popd

%build
pushd src
    export CCASFLAGS="%{optflags} -Wa,--noexecstack"
    %configure --disable-static --enable-dynamic
    make %{?_smp_mflags}
    pushd doc
	pdflatex doc.tex
    popd
popd

%install
make install DESTDIR=%{buildroot} -C src
rm %{buildroot}%{_libdir}/libfes.la

%check
pushd src
    chmod +x test/test_suite.py
    make check
    cat test/test_suite.py.log
popd

%files
%doc src/AUTHORS
%doc src/COPYING
%{_libdir}/libfes.so.*

%files		devel
%doc src/TODO
%doc src/doc/doc.pdf
%{_includedir}/fes_interface.h
%{_libdir}/libfes.so
