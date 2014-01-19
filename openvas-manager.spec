
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Open Vulnerability Assessment System manager
Name:		openvas-manager
Version:	4.0.4
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://wald.intevation.org/frs/download.php/1434/%{name}-%{version}.tar.gz
# Source0-md5:	782238496faa2c55ea505ffdae4b41b1
URL:		http://www.openvas.org/
BuildRequires:	cmake
BuildRequires:	glib2-devel >= 2.16
BuildRequires:	gnutls-devel > 2.8
BuildRequires:	libuuid-devel
BuildRequires:	openvas-libraries-devel >= 6.0.0
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel
%if %{with apidocs}
BuildRequires:	doxygen
#BuildRequires:	sqlfairy
#BuildRequires:	xmltoman
%endif
BuildConflicts:	openvas-libraries-devel >= 7.0
Requires:	openvas-common >= 6.0.0
Suggests:	/usr/bin/makensis
Suggests:	/usr/bin/pdflatex
Suggests:	/usr/bin/xsltproc
Suggests:	alien
Suggests:	fakeroot
Suggests:	gnupg
Suggests:	rpm
Suggests:	wget
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the manager module for the Open Vulnerability Assessment
System (OpenVAS).

The Open Vulnerability Assessment System (OpenVAS) is a framework of
several services and tools offering a comprehensive and powerful
vulnerability scanning and vulnerability management solution.

%package apidocs
Summary:	OpenVAS manager API documentation
Summary(pl.UTF-8):	Dokumentacja API zarządcy OpenVAS
Group:		Documentation

%description apidocs
OpenVAS manager API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API zarządcy OpenVAS.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DLOCALSTATEDIR=/var \
	..
%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# included via %doc
rm $RPM_BUILD_ROOT%{_docdir}/%{name}/html/omp.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES ChangeLog README TODO INSTALL
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openvas/openvasmd_log.conf
%doc doc/{*.sql,*.html,*HOWTO,about-cert-feed.txt,*.png,*.rnc}
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*.8*
%{_datadir}/openvas/cert
%{_datadir}/openvas/openvasmd
%{_datadir}/openvas/scap
/var/lib/openvas/openvasmd
