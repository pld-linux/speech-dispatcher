# TODO: think about default configuration (DefaultModule is espeak, which is not loaded by default)
#
# Conditional build:
%bcond_with	ibmtts		# IBM TTS synthesizer support (commercial, proprietary)
%bcond_without	espeak		# eSpeak synthesizer support
%bcond_without	flite		# Flite synthesizer support
%bcond_without	ivona		# Ivona synthesizer support
%bcond_without	svox		# SVOX Pico synthesizer support
%bcond_without	alsa		# ALSA audio output supprot
%bcond_without	libao		# libao audio output supprot
%bcond_without	nas		# NAS audio output support
%bcond_without	pulseaudio	# pulse audio output support
%bcond_without	python		# Python 3 binding (python 2.x no longer supported)
%bcond_without	static_libs	# don't build static libraries
#
Summary:	A device independent layer for speech synthesis
Summary(pl.UTF-8):	Niezależna od urządzenia warstwa obsługująca syntezę mowy
Name:		speech-dispatcher
Version:	0.8.3
Release:	3
License:	LGPL v2.1+ (library and audio drivers), GPL v2+ (programs and speech modules)
Group:		Applications/Sound
Source0:	http://www.freebsoft.org/pub/projects/speechd/%{name}-%{version}.tar.gz
# Source0-md5:	d17b041fa3c87cb1b73ac6e95b80d276
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
Patch0:		%{name}-info.patch
URL:		http://www.freebsoft.org/
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	autoconf >= 2.63
# for __pycache__ support (python 3.2+)
BuildRequires:	automake >= 1:1.13
BuildRequires:	dotconf-devel >= 1.3
%{?with_espeak:BuildRequires:	espeak-devel}
BuildRequires:	glib2-devel >= 1:2.28
%{?with_flite:BuildRequires:	flite-devel}
%{?with_ibmtts:BuildRequires:	ibmtts-devel}
BuildRequires:	intltool >= 0.40.0
%{?with_libao:BuildRequires:	libao-devel}
%{?with_ivona:BuildRequires:	libdumbtts-devel}
BuildRequires:	libsndfile-devel >= 1.0.2
BuildRequires:	libtool >= 2:2.2
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
%{?with_python:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.527
%{?with_svox:BuildRequires:	svox-devel}
BuildRequires:	texinfo
%{?with_nas:BuildRequires:	xorg-lib-libXau-devel}
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dotconf >= 1.3
Requires:	libsndfile >= 1.0.2
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

%package audio-libao
Summary:	libao audio output module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł wyjścia dźwięku libao dla Speech Dispatchera
License:	LGPL v2.1+
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description audio-libao
libao audio output module for Speech Dispatcher.

%description audio-libao -l pl.UTF-8
Moduł wyjścia dźwięku libao dla Speech Dispatchera.

%package audio-nas
Summary:	NAS audio output module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł wyjścia dźwięku NAS dla Speech Dispatchera
License:	LGPL v2.1+
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description audio-nas
NAS audio output module for Speech Dispatcher.

%description audio-nas -l pl.UTF-8
Moduł wyjścia dźwięku NAS dla Speech Dispatchera.

%package audio-pulse
Summary:	PulseAudio audio output module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł wyjścia dźwięku PulseAudio dla Speech Dispatchera
License:	LGPL v2.1+
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description audio-pulse
PulseAudio audio output module for Speech Dispatcher.

%description audio-pulse -l pl.UTF-8
Moduł wyjścia dźwięku PulseAudio dla Speech Dispatchera.

%package module-espeak
Summary:	eSpeak synthesizer module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł syntezatora eSpeak dla Speech Dispatchera
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description module-espeak
eSpeak synthesizer module for Speech Dispatcher.

%description module-espeak -l pl.UTF-8
Moduł syntezatora eSpeak dla Speech Dispatchera.

%package module-flite
Summary:	Flite synthesizer module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł syntezatora Flite dla Speech Dispatchera
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description module-flite
Flite synthesizer module for Speech Dispatcher.

%description module-flite -l pl.UTF-8
Moduł syntezatora Flite dla Speech Dispatchera.

%package module-ibmtts
Summary:	IBM TTS synthesizer module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł syntezatora IBM TTS dla Speech Dispatchera
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description module-ibmtts
IBM TTS synthesizer module for Speech Dispatcher.

%description module-ibmtts -l pl.UTF-8
Moduł syntezatora IBM TTS dla Speech Dispatchera.

%package module-ivona
Summary:	Ivona synthesizer module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł syntezatora Ivona dla Speech Dispatchera
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description module-ivona
Ivona synthesizer module for Speech Dispatcher.

%description module-ivona -l pl.UTF-8
Moduł syntezatora Ivona dla Speech Dispatchera.

%package module-pico
Summary:	SVOX Pico synthesizer module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł syntezatora SVOX Pico dla Speech Dispatchera
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description module-pico
SVOX Pico synthesizer module for Speech Dispatcher.

%description module-pico -l pl.UTF-8
Moduł syntezatora SVOX Pico dla Speech Dispatchera.

%package libs
Summary:	Speech Dispatcher client library
Summary(pl.UTF-8):	Biblioteka kliencka Speech Dispatchera
License:	LGPL v2.1+
Group:		Libraries
Requires:	glib2 >= 1:2.28

%description libs
Speech Dispatcher provides a device independent layer for speech
synthesis. This package contains client library.

%description libs -l pl.UTF-8
Speech Dispatcher zapewnia niezależną od urządzenia warstwę
obsługującą syntezę mowy. Ten pakiet zawiera biblitotekę kliencką.

%package devel
Summary:	Header files for speech-dispatcher library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki speech-dispatcher
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.28

%description devel
Header files for speech-dispatcher library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki speech-dispatcher.

%package static
Summary:	Static speech-dispatcher library
Summary(pl.UTF-8):	Statyczna biblioteka speech-dispatcher
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static speech-dispatcher library.

%description static -l pl.UTF-8
Statyczna biblioteka speech-dispatcher.

%package -n python3-%{name}
Summary:	Python 3 library for communication with Speech Dispatcher
Summary(pl.UTF-8):	Biblioteka Pythona 3 do komunikacji ze Speech Dispatcherem
License:	LGPL v2.1+
Group:		Libraries/Python
Requires:	python3-modules
Obsoletes:	python-speech-dispatcher

%description -n python3-%{name}
Speech Dispatcher provides a device independent layer for speech
synthesis. This package contains a Python 3 library for communication
with Speech Dispatcher.

%description -n python3-%{name} -l pl.UTF-8
Speech Dispatcher zapewnia niezależną od urządzenia warstwę
obsługującą syntezę mowy. Ten pakiet zawiera bibliotekę Pythona 3 do
komunikacji ze Speech Dispatcherem.

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
	%{__disable python} \
	%{__enable_disable static_libs static} \
	%{__with_without alsa} \
	--with-default-audio-method=%{?with_alsa:alsa}%{!?with_alsa:oss} \
	%{__with_without espeak} \
	%{__with_without flite} \
	%{__with_without ibmtts} \
	%{__with_without ivona} \
	%{__with_without libao} \
	%{__with_without nas} \
	%{__with_without pulseaudio pulse} \
	%{__with_without svox pico}

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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/speech-dispatcher/spd_*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/speech-dispatcher/spd_*.a
%endif
%if %{without ibmtts}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/speech-dispatcher/modules/ibmtts.conf
%endif

%find_lang %{name}

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/spd-conf
%attr(755,root,root) %{_bindir}/spd-say
%attr(755,root,root) %{_bindir}/spdsend
%attr(755,root,root) %{_bindir}/speech-dispatcher
%dir %{_libdir}/speech-dispatcher
%{?with_alsa:%attr(755,root,root) %{_libdir}/speech-dispatcher/spd_alsa.so}
%{_libdir}/speech-dispatcher/spd_oss.so
%dir %{_libdir}/speech-dispatcher-modules
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_cicero
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_dummy
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_festival
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_generic
%{_datadir}/speech-dispatcher
%{_datadir}/sounds/speech-dispatcher
%dir %{_sysconfdir}/speech-dispatcher
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/speechd.conf
%dir %{_sysconfdir}/speech-dispatcher/clients
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/clients/emacs.conf
%dir %{_sysconfdir}/speech-dispatcher/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/cicero.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/dtk-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/epos-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/espeak-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/espeak-mbrola-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/festival.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/llia_phon-generic.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/swift-generic.conf
%dir %attr(755,%{name},%{name}) /var/run/speech-dispatcher
%dir %attr(755,%{name},%{name}) /var/log/speech-dispatcher
/usr/lib/tmpfiles.d/%{name}.conf
%{_infodir}/spd-say.info*
%{_infodir}/speech-dispatcher.info*
%lang(cs) %{_infodir}/speech-dispatcher-cs.info*
%{_infodir}/ssip.info*

%if %{with libao}
%files audio-libao
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher/spd_libao.so
%endif

%if %{with nas}
%files audio-nas
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher/spd_nas.so
%endif

%if %{with pulseaudio}
%files audio-pulse
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher/spd_pulse.so
%endif

%if %{with espeak}
%files module-espeak
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_espeak
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/espeak.conf
%endif

%if %{with flite}
%files module-flite
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_flite
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/flite.conf
%endif

%if %{with ibmtts}
%files module-ibmtts
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_ibmtts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/ibmtts.conf
%endif

%if %{with ivona}
%files module-ivona
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_ivona
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/ivona.conf
%endif

%if %{with svox}
%files module-pico
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_pico
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/pico.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/pico-generic.conf
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspeechd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspeechd.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspeechd.so
%{_libdir}/libspeechd.la
%{_includedir}/speech-dispatcher
%{_pkgconfigdir}/speech-dispatcher.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libspeechd.a
%endif

%if %{with python}
%files -n python3-%{name}
%defattr(644,root,root,755)
%dir %{py3_sitedir}/speechd
%{py3_sitedir}/speechd/*.py
%{py3_sitedir}/speechd/__pycache__
%dir %{py3_sitedir}/speechd_config
%{py3_sitedir}/speechd_config/*.py
%{py3_sitedir}/speechd_config/__pycache__
%endif
