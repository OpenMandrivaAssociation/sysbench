Summary:       System performance benchmark
Name:          sysbench
Version:       1.0.17
Release:       1
Group:         System/Kernel and hardware
License:       GPLv2+
Source0:       https://github.com/akopytov/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
URL:           https://github.com/akopytov/sysbench/

BuildRequires: automake
BuildRequires: pkgconfig(ck)
BuildRequires: docbook-style-xsl
BuildRequires: libaio-devel
BuildRequires: libtool
BuildRequires: xsltproc
BuildRequires: luajit-devel
BuildRequires: mariadb-devel
#BuildRequires: mariadb-connector-c-devel
#BuildRequires: libpq-devel
BuildRequires: postgresql-devel
BuildRequires: python-cram

%description
SysBench is a modular, cross-platform and multi-threaded benchmark
tool for evaluating OS parameters that are important for a system
running a database under intensive load.

The idea of this benchmark suite is to quickly get an impression about
system performance without setting up complex database benchmarks or
even without installing a database at all. Current features allow to
test the following system parameters:
- file I/O performance
- scheduler performance
- memory allocation and transfer speed
- POSIX threads implementation performance
- database server performance (OLTP benchmark)

Primarily written for MySQL server benchmarking, SysBench will be
further extended to support multiple database backends, distributed
benchmarks and third-party plug-in modules.


%prep
%setup -q
rm -r third_party/luajit/luajit/
rm -r third_party/concurrency_kit/ck/
rm -r third_party/cram/

%build
export CFLAGS="%{optflags}"
autoreconf -vif
%configure --with-mysql \
           --with-pgsql \
           --with-system-ck \
           --with-system-luajit \
           --without-gcc-arch

%make

%install
%makeinstall_std
mv %{buildroot}%{_docdir}/sysbench/manual.html .

%check
cd tests
./test_run.sh

%files
%doc ChangeLog README.md manual.html
%doc COPYING
%{_bindir}/*
%{_datadir}/%{name}
