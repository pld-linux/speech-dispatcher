#
# Conditional build:
%bcond_with	ibmtts		# commercial, proprietary IBM TTS synthesizer support
%bcond_without	flite		# flite synthetizer support
%bcond_without	espeak		# espeak synthetizer support
%bcond_without	nas		# NAS audio output support
%bcond_without	alsa		# ALSA audio output supprot
%bcond_without	pulseaudio	# pulse audio output support
%bcond_without	static_libs	# don't build static libraries
%bcond_without	ivona		# don't build ivona support
#
Summary:	A device independent layer for speech synthesis
Summary(pl.UTF-8):	Niezależna od urządzenia warstwa obsługująca syntezę mowy
Name:		speech-dispatcher
Version:	0.7.1
Release:	2
License:	GPL v2
Group:		Applications/Sound
Source0:	http://www.freebsoft.org/pub/projects/speechd/%{name}-%{version}.tar.gz
# Source0-md5:	ccfc30ac006673d36b4223eb760ed696
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
Patch0:		%{name}-info.patch
Patch1:		pulse.patch
URL:		http://www.freebsoft.org/
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dotconf-devel
%{?with_espeak:BuildRequires:	espeak-devel}
%{?with_flite:BuildRequires:	flite-devel}
%{?with_ibmtts:BuildRequires:	ibmtts-devel}
BuildRequires:	libatomic_ops
%{?with_ivona:BuildRequires:	libdumbtts-devel}
BuildRequires:	libtool
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	texinfo
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
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
Summary(pl.UTF-8):	Biblioteka Pythona do komunikacji ze Speech Dispatcherem
Group:		Libraries/Python
%pyrequires_eq	python-modules

%description -n python-%{name}
Speech Dispatcher provides a device independent layer for speech
synthesis. This package contains a Python library for communication
with Speech Dispatcher.

%description -n python-%{name} -l pl.UTF-8
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
	%{__with_without flite} \
	%{__with_without ibmtts} \
	%{__with_without espeak} \
	%{__with_without nas} \
	%{__with_without alsa} \
	%{__with_without pulseaudio pulse} \
	%{__with_without ivona} \
	%{__enable_disable static_libs static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/{log,run}/speech-dispatcher \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE2}	$RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}/speechd
%py_postclean
# library for engines output, API not included in -devel
%{__rm} $RPM_BUILD_ROOT%{_libdir}/speech-dispatcher/libsdaudio.{so,la,a}

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
%attr(755,root,root) %{_bindir}/clibrary
%attr(755,root,root) %{_bindir}/clibrary2
%attr(755,root,root) %{_bindir}/connection_recovery
%attr(755,root,root) %{_bindir}/long_message
%attr(755,root,root) %{_bindir}/run_test
%attr(755,root,root) %{_bindir}/spd-conf
%attr(755,root,root) %{_bindir}/spd-say
%attr(755,root,root) %{_bindir}/spdsend
%attr(755,root,root) %{_bindir}/speech-dispatcher
%dir %{_libdir}/speech-dispatcher
%attr(755,root,root) %{_libdir}/speech-dispatcher/libsdaudio.so.*
%dir %{_sysconfdir}/speech-dispatcher
%dir %{_sysconfdir}/speech-dispatcher/clients
%dir %{_sysconfdir}/speech-dispatcher/modules
%dir %{_libdir}/speech-dispatcher-modules
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_cicero
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_dummy
%if %{with espeak}
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_espeak
%endif
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_festival
%if %{with flite}
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_flite
%endif
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_generic
%if %{with ibmtts}
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_ibmtts
%endif
%if %{with ivona}
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_ivona
%endif
%{_datadir}/speech-dispatcher
%{_datadir}/sounds/speech-dispatcher
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/speechd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/clients/emacs.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/clients/gnome-speech.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/cicero.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/dtk-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/epos-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/espeak-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/espeak-mbrola-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/espeak.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/festival.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/flite.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/ibmtts.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/ivona.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/llia_phon-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/swift-generic.conf
%dir %attr(755,%{name},%{name}) /var/run/speech-dispatcher
%dir %attr(755,%{name},%{name}) /var/log/speech-dispatcher
/usr/lib/tmpfiles.d/%{name}.conf
%{_infodir}/spd-say.info*
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
%dir %{py_sitedir}/speechd
%dir %{py_sitedir}/speechd_config
%{py_sitedir}/speechd/*.py[co]
%{py_sitedir}/speechd_config/*.py[co]
