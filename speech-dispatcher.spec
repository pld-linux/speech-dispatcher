#
# Conditional build:
%bcond_with	ibmtts		# commercial, proprietary IBM TTS synthesizer support
%bcond_without	flite		# flite synthetizer support
%bcond_without	espeak		# espeak synthetizer support
%bcond_without	nas		# NAS audio output support
%bcond_without	alsa		# ALSA audio output supprot
%bcond_without	pulse		# pulse audio output support
%bcond_without	static_libs	# don't build static libraries
#
Summary:	A device independent layer for speech synthesis
Summary(pl.UTF-8):	Niezależna od urządzenia warstwa obsługująca syntezę mowy
Name:		speech-dispatcher
Version:	0.6.7
Release:	1
License:	GPL v2
Group:		Applications/Sound
Source0:	http://www.freebsoft.org/pub/projects/speechd/%{name}-%{version}.tar.gz
# Source0-md5:	67432ad655b50fd7c1f1f79e012cfe3f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-python-install.patch
Patch1:		%{name}-info.patch
URL:		http://www.freebsoft.org/
%{?with_alsa:Buildrequires:	alsa-lib-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dotconf-devel
%{?with_espeak:Buildrequires:	espeak-devel}
%{?with_flite:Buildrequires:	flite-devel}
%{?with_ibmtts:Buildrequires:	ibmtts-devel}
Buildrequires:	libatomic_ops
BuildRequires:	libtool
%{?with_nas:Buildrequires:	nas-devel}
%{?with_pulse:Buildrequires:	pulseaudio-devel}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	texinfo
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
Provides:	group(%{name})
Provides:	user(%{name})
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Speech Dispatcher provides a device independent layer for speech
synthesis.

%description -l pl.UTF-8
Speech Dispatcher zapewnia niezależną od urządzenia warstwę
obsługującą syntezę mowy.

%package libs
Summary:	Speech Dispatcher client library
Summary(pl.UTF-8):	Biblioteka kliencka Speech Dispatchera
Group:		Libraries

%description libs
Speech Dispatcher provides a device independent layer for speech
synthesis. This package contains client library.

%description libs -l pl.UTF-8
Speech Dispatcher zapewnia niezależną od urządzenia warstwę
obsługującą syntezę mowy. Ten pakiet zawiera biblitotekę kliencką.

%package devel
Summary:	Header files for speech-dispatcher library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki speech-dispatcher
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for speech-dispatcher library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki speech-dispatcher.

%package static
Summary:	Static speech-dispatcher library
Summary(pl.UTF-8):	Statyczna biblioteka speech-dispatcher
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static speech-dispatcher library.

%description static -l pl.UTF-8
Statyczna biblioteka speech-dispatcher.

%package -n python-%{name}
Summary:	Python library for communication with Speech Dispatcher
Summary(pl_PL.UTF-8):	Biblioteka Pythona do komunikacji ze Speech Dispatcherem
Group:		Libraries/Python
%pyrequires_eq	python-modules

%description -n python-%{name}
Speech Dispatcher provides a device independent layer for speech
synthesis. This package contains a Python library for communication
with Speech Dispatcher.

%description -n python-%{name} -l pl_PL.UTF-8
Speech Dispatcher zapewnia niezależną od urządzenia warstwę
obsługującą syntezę mowy. Ten pakiet zawiera bibliotekę Pythona do
komunikacji ze Speech Dispatcherem.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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

install -d $RPM_BUILD_ROOT/var/{log,run}/speech-dispatcher

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE2}	$RPM_BUILD_ROOT/etc/sysconfig/%{name}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}/speechd
%py_postclean
# library for engines output, API not included in -devel
rm $RPM_BUILD_ROOT%{_libdir}/speech-dispatcher/libsdaudio.{so,la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 224 %{name}
%useradd -u 224 -g 224 -G audio -d /usr/share/empty -s /bin/false -c "%{name} user" %{name}

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/speech-dispatcher
%attr(755,root,root) %{_libdir}/speech-dispatcher/libsdaudio.so.*
%dir %{_sysconfdir}/speech-dispatcher
%dir %{_sysconfdir}/speech-dispatcher/clients
%dir %{_sysconfdir}/speech-dispatcher/modules
%dir %{_libdir}/speech-dispatcher-modules
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/clients/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/*.conf
%dir %attr(755,%{name},%{name}) /var/run/speech-dispatcher
%dir %attr(755,%{name},%{name}) /var/log/speech-dispatcher
%{_infodir}/spd-say.info*
%lang(cs) %{_infodir}/speech-dispatcher-cs.info*
%{_infodir}/speech-dispatcher.info*
%{_infodir}/ssip.info*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspeechd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspeechd.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspeechd.so
%{_libdir}/libspeechd.la
%{_includedir}/libspeechd.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libspeechd.a
%endif

%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/speechd
%{py_sitescriptdir}/speechd/*.py[co]
%{py_sitescriptdir}/speechd-*.egg-info
