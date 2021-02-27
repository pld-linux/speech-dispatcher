# TODO:
# - think about default configuration (DefaultModule is espeak, which is not loaded by default)
# - common-lisp and guile bindings (src/api/{cl,guile})
#
# Conditional build:
%bcond_with	baratinoo	# Voxygen Baratinoo synthesizer support (proprietary)
%bcond_without	espeak		# eSpeak synthesizer support
%bcond_without	espeak_ng	# eSpeak-NG synthesizer support
%bcond_without	flite		# Flite synthesizer support
%bcond_with	ibmtts		# IBM TTS synthesizer support (proprietary)
%bcond_without	ivona		# Ivona synthesizer support
%bcond_with	kali		# Kali synthesizer support (proprietary?)
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
Version:	0.10.1
Release:	2
License:	LGPL v2.1+ (library and audio drivers), GPL v2+ (programs and speech modules)
Group:		Applications/Sound
#Source0Download: https://github.com/brailcom/speechd/releases
Source0:	https://github.com/brailcom/speechd/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	49bc64d8517762d9c9818f5ef3d3bc42
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
Patch0:		%{name}-info.patch
URL:		https://freebsoft.org/speechd
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	autoconf >= 2.63
# for __pycache__ support (python 3.2+)
BuildRequires:	automake >= 1:1.13
BuildRequires:	dotconf-devel >= 1.3
%{?with_espeak:BuildRequires:	espeak-devel}
%{?with_espeak_ng:BuildRequires:	espeak-ng-devel}
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	help2man
%{?with_flite:BuildRequires:	flite-devel}
%{?with_ibmtts:BuildRequires:	ibmtts-devel}
BuildRequires:	intltool >= 0.40.0
%{?with_libao:BuildRequires:	libao-devel}
%{?with_ivona:BuildRequires:	libdumbtts-devel}
BuildRequires:	libltdl-devel
BuildRequires:	libsndfile-devel >= 1.0.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
%{?with_python:BuildRequires:	python3-devel >= 1:3.2}
%{?with_python:BuildRequires:	python3-pyxdg}
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
# for spd-conf
Requires:	python3-%{name} = %{version}-%{release}
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

%package module-baratinoo
Summary:	Baratinoo synthesizer module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł syntezatora Baratinoo dla Speech Dispatchera
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description module-baratinoo
Baratinoo synthesizer module for Speech Dispatcher.

%description module-baratinoo -l pl.UTF-8
Moduł syntezatora Baratinoo dla Speech Dispatchera.

%package module-espeak
Summary:	eSpeak synthesizer module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł syntezatora eSpeak dla Speech Dispatchera
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description module-espeak
eSpeak synthesizer module for Speech Dispatcher.

%description module-espeak -l pl.UTF-8
Moduł syntezatora eSpeak dla Speech Dispatchera.

%package module-espeak-ng
Summary:	eSpeak NG synthesizer module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł syntezatora eSpeak NG dla Speech Dispatchera
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description module-espeak-ng
eSpeak NG synthesizer module for Speech Dispatcher.

%description module-espeak-ng -l pl.UTF-8
Moduł syntezatora eSpeak NG dla Speech Dispatchera.

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

%package module-kali
Summary:	Kali synthesizer module for Speech Dispatcher
Summary(pl.UTF-8):	Moduł syntezatora Kali dla Speech Dispatchera
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description module-kali
Kali synthesizer module for Speech Dispatcher.

%description module-kali -l pl.UTF-8
Moduł syntezatora Kali dla Speech Dispatchera.

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
Requires:	glib2 >= 1:2.36

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
Requires:	glib2-devel >= 1:2.36

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

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' src/api/python/speechd_config/spd-conf

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__disable python} \
	--disable-silent-rules \
	%{__enable_disable static_libs static} \
	%{__with_without alsa} \
	%{__with_without baratinoo} \
	--with-default-audio-method=%{?with_alsa:alsa}%{!?with_alsa:oss} \
	%{__with_without espeak} \
	%{__with_without flite} \
	%{__with_without ibmtts} \
	%{__with_without ivona} \
	%{__with_without kali} \
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
%doc ANNOUNCE AUTHORS BUGS FAQ NEWS README.md README.overview.md TODO
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/mary-generic-disabled.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/swift-generic.conf
%dir %attr(755,%{name},%{name}) /var/run/speech-dispatcher
%dir %attr(755,%{name},%{name}) /var/log/speech-dispatcher
%{systemdunitdir}/speech-dispatcherd.service
%{systemdtmpfilesdir}/%{name}.conf
%{_mandir}/man1/spd-conf.1*
%{_mandir}/man1/spd-say.1*
%{_mandir}/man1/speech-dispatcher.1*
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

%if %{with baratinoo}
%files module-baratinoo
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_baratinoo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/baratinoo.conf
%endif

%if %{with espeak}
%files module-espeak
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_espeak
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/espeak.conf
%endif

%if %{with espeak_ng}
%files module-espeak-ng
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_espeak-ng
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/espeak-ng.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/espeak-ng-mbrola-generic.conf
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

%if %{with kali}
%files module-kali
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/speech-dispatcher-modules/sd_kali
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/speech-dispatcher/modules/kali.conf
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
