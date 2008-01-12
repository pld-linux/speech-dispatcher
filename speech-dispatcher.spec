# Conditional build:
%bcond_with	flite
%bcond_with	ibmtts
%bcond_without	espeak
%bcond_without	nas
%bcond_without	alsa
%bcond_without	pulse
%bcond_without	static_libs # don't build static librarie
#
Summary:	A device independent layer for speech synthesis
#Summary(pl.UTF-8):	-
Name:		speech-dispatcher
Version:	0.6.5
Release:	0.3
License:	GPL v2
Group:		Applications
Source0:	http://www.freebsoft.org/pub/projects/speechd/%{name}-%{version}.tar.gz
# Source0-md5:	ad8cf47918207872ba976f2b2e47c02b
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-python-install.patch
URL:		http://www.freebsoft.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dotconf-devel
Buildrequires:	libatomic_ops
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
%{?with_flite:Buildrequires:	flite-devel}
%{?with_ibmtts:Buildrequires:	ibmtts-devel}
%{?with_espeak:Buildrequires:	espeak-devel}
%{?with_nas:Buildrequires:	nas-devel}
%{?with_alsa:Buildrequires:	alsa-lib-devel}
%{?with_pulse:Buildrequires:	pulseaudio-devel}
Provides:	group(%{name})
Provides:	user(%{name})
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Speech Dispatcher provides a device independent layer for speech
synthesis.

#description -l pl.UTF-8

%package devel
Summary:	Header files for speed-dispatcher library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki speed-dispatcher
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for speed-dispatcher library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki speed-dispatcher.

%package static
Summary:	Static speed-dispatcher library
Summary(pl.UTF-8):	Statyczna biblioteka speed-dispatcher
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static speed-dispatcher library.

%description static -l pl.UTF-8
Statyczna biblioteka speed-dispatcher.

%package -n python-%{name}
Summary:	Python library for communication with Speech Dispatcher
#Summary(pl_PL.UTF-8):
Group:		Libraries/Python
%pyrequires_eq	python-modules

%description -n python-%{name}
Speech Dispatcher provides a device independent layer for speech
synthesis. This package contains a Python library for communication
with Speech Dispatcher.

#description -n python-%{name} -l pl_PL.UTF-8

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_flite:--with-flite}%{!?with_flite:--without-flite} \
	%{?with_ibmtts:--with-ibmtts}%{!?with_ibmtts:--without-ibmtts} \
	%{?with_espeak:--with-espeak}%{!?with_espeak:--without-espeak} \
	%{?with_nas:--with-nas}%{!?with_nas:--without-nas} \
	%{?with_alsa:--with-alsa}%{!?with_alsa:--without-alsa} \
	%{?with_pulse:--with-pulse}%{!?with_pulse:--without-pulse} \
	--enable-static=%{?with_static_libs:yes}%{!?with_static_libs:no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/run/speech-dispatcher

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE2}	$RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 223 %{name}
%useradd -u 223 -g 223 -d /usr/share/empty -s /bin/false -c "%{name} user" %{name}

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_libdir}/speech-dispatcher
%attr(755,root,root) %{_libdir}/speech-dispatcher/lib*.so.*.*.*
# XXX: ? below
%attr(755,root,root) %{_libdir}/speech-dispatcher/lib*.so.[^.]
%dir %{_sysconfdir}/speech-dispatcher
%dir %{_sysconfdir}/speech-dispatcher/clients
%dir %{_sysconfdir}/speech-dispatcher/modules
%dir %{_libdir}/speech-dispatcher-modules
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_cicero
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_espeak
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_festival
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_generic
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/clients/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/*.conf
%dir %attr(755,%{name},%{name}) /var/run/speech-dispatcher
%{_infodir}/spd-say.info.gz
%lang(cs) %{_infodir}/speech-dispatcher-cs.info.gz
%{_infodir}/speech-dispatcher.info.gz
%{_infodir}/ssip.info.gz

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/speech-dispatcher/lib*.so
%{_libdir}/speech-dispatcher/lib*.la
%{_includedir}/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_libdir}/speech-dispatcher/lib*.a
%endif

%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/speechd
%{py_sitescriptdir}/speechd/*.py[c]
