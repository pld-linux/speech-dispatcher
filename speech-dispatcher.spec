# Conditional build:
%bcond_with	flite
%bcond_with	ibmtts
%bcond_without	espeak
%bcond_without	nas
%bcond_without	alsa
%bcond_without	pulse
#
Summary:	A device independent layer for speech synthesis
#Summary(pl.UTF-8):	-
Name:		speech-dispatcher
Version:	0.6.5
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://www.freebsoft.org/pub/projects/speechd/%{name}-%{version}.tar.gz
# Source0-md5:	ad8cf47918207872ba976f2b2e47c02b
Patch0:		%{name}-python-install.patch
URL:		http://www.freebsoft.org/
Buildrequires:	libatomic_ops
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_flite:Buildrequires:	flite-devel}
%{?with_ibmtts:Buildrequires:	ibmtts-devel}
%{?with_espeak:Buildrequires:	espeak-devel}
%{?with_nas:Buildrequires:	nas-devel}
%{?with_alsa:Buildrequires:	alsa-lib-devel}
%{?with_pulse:Buildrequires:	pulseaudio-devel}
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
	%{?with_pulse:--with-pulse}%{!?with_pulse:--without-pulse}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

# unpackaged:
/etc/speech-dispatcher/clients/emacs.conf
/etc/speech-dispatcher/clients/gnome-speech.conf
/etc/speech-dispatcher/modules/apollo.conf
/etc/speech-dispatcher/modules/cicero.conf
/etc/speech-dispatcher/modules/dtk-generic.conf
/etc/speech-dispatcher/modules/epos-generic.conf
/etc/speech-dispatcher/modules/espeak-generic.conf
/etc/speech-dispatcher/modules/espeak.conf
/etc/speech-dispatcher/modules/festival.conf
/etc/speech-dispatcher/modules/flite.conf
/etc/speech-dispatcher/modules/ibmtts.conf
/etc/speech-dispatcher/modules/llia_phon-generic.conf
/etc/speech-dispatcher/speechd.conf
/usr/lib/libspeechd.so.2
/usr/lib/speech-dispatcher-modules/sd_cicero
/usr/lib/speech-dispatcher-modules/sd_espeak
/usr/lib/speech-dispatcher-modules/sd_festival
/usr/lib/speech-dispatcher-modules/sd_generic
/usr/lib/speech-dispatcher/libsdaudio.a
/usr/lib/speech-dispatcher/libsdaudio.la
/usr/lib/speech-dispatcher/libsdaudio.so
/usr/lib/speech-dispatcher/libsdaudio.so.2
/usr/lib/speech-dispatcher/libsdaudio.so.2.0.2
/usr/share/info/spd-say.info.gz
/usr/share/info/speech-dispatcher-cs.info.gz
/usr/share/info/speech-dispatcher.info.gz
/usr/share/info/ssip.info.gz
/usr/share/python2.5/site-packages/speechd-0.3-py2.5.egg-info
/usr/share/python2.5/site-packages/speechd/__init__.py
/usr/share/python2.5/site-packages/speechd/__init__.pyc
/usr/share/python2.5/site-packages/speechd/_test.py
/usr/share/python2.5/site-packages/speechd/_test.pyc
/usr/share/python2.5/site-packages/speechd/client.py
/usr/share/python2.5/site-packages/speechd/client.pyc
