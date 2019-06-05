#
# Conditional build:
%bcond_without	apidocs		# Doxygen based API documentation
%bcond_without	gstreamer	# GStreamer module
#
Summary:	PipeWire - server and user space API to deal with multimedia pipelines
Summary(pl.UTF-8):	PipeWire - serwer i API przestrzeni użytkownika do obsługi potoków multimedialnych
Name:		pipewire
Version:	0.2.6
Release:	1
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://github.com/PipeWire/pipewire/releases
Source0:	https://github.com/PipeWire/pipewire/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	95c5a745b56b68065d528fcf0b1aca31
#Patch0:	%{name}-what.patch
URL:		https://pipewire.org/
# for tests only
#BuildRequires:	SDL2-devel >= 2
BuildRequires:	alsa-lib-devel
BuildRequires:	dbus-devel
%{?with_apidocs:BuildRequires:	doxygen}
# libavcodec libavformat libavfilter
BuildRequires:	ffmpeg-devel
BuildRequires:	gcc >= 5:3.2
%{?with_gstreamer:BuildRequires:	glib2-devel >= 1:2.32.0}
%{?with_apidocs:BuildRequires:	graphviz}
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%endif
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sbc-devel
BuildRequires:	systemd-devel
BuildRequires:	udev-devel
BuildRequires:	xmltoman
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PipeWire is a server and user space API to deal with multimedia
pipelines. This includes:
 - Making available sources of video (such as from a capture devices
   or application provided streams) and multiplexing this with
   clients.
 - Accessing sources of video for consumption.
 - Generating graphs for audio and video processing.

Nodes in the graph can be implemented as separate processes,
communicating with sockets and exchanging multimedia content using fd
passing.

%description -l pl.UTF-8
PipeWire to serwer i API przestrzeni użytkownika do obsługi potoków
multimedialnych. Obejmuje to:
 - udostępnianie źródeł obrazu (np. z urządzeń przechwytujących obraz
   lub strumieni udostępnianych przez aplikacje) oraz multipleksowanie
   ich do klientów
 - dostęp do źródeł obrazu do pobierania
 - generowanie grafów do przetwarzania dźwięku i obrazu

%package libs
Summary:	PipeWire shared library
Summary(pl.UTF-8):	Biblioteka współdzielona PipeWire
Group:		Libraries

%description libs
PipeWire shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona PipeWire.

%package devel
Summary:	Header files for PipeWire library and Simple Plugin API
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PipeWire oraz Simple Plugin API
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for PipeWire library and Simple Plugin API.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PipeWire oraz Simple Plugin API.

%package apidocs
Summary:	API documentation for PipeWire library
Summary(pl.UTF-8):	Dokumentacja API biblioteki PipeWire
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for PipeWire library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PipeWire.

%package spa-module-alsa
Summary:	PipeWire SPA plugin to play and record audio with ALSA API
Summary(pl.UTF-8):	Wtyczka PipeWire SPA do odtwarzania i nagrywania dźwięku przy użyciu API ALSA
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description spa-module-alsa
PipeWire SPA plugin to play and record audio with ALSA API.

%description spa-module-alsa -l pl.UTF-8
Wtyczka PipeWire SPA do odtwarzania i nagrywania dźwięku przy użyciu
API ALSA.

%package spa-module-bluez
Summary:	PipeWire SPA plugin to play audio with Bluetooth A2DP
Summary(pl.UTF-8):	Wtyczka PipeWire SPA do odtwarzania dźwięku przez Bluetooth A2DP
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description spa-module-bluez
PipeWire SPA plugin to play audio with Bluetooth A2DP.

%description spa-module-bluez -l pl.UTF-8
Wtyczka PipeWire SPA do odtwarzania dźwięku przez Bluetooth A2DP.

%package spa-module-ffmpeg
Summary:	PipeWire SPA plugin to decode/encode with FFmpeg library
Summary(pl.UTF-8):	Wtyczka PipeWire SPA do kodowania/dekodowania przy użyciu biblioteki FFmpeg
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description spa-module-ffmpeg
PipeWire SPA plugin to decode/encode with FFmpeg library.

%description spa-module-ffmpeg -l pl.UTF-8
Wtyczka PipeWire SPA do kodowania/dekodowania przy użyciu biblioteki
FFmpeg.

%package -n gstreamer-pipewire
Summary:	PipeWire video sink and source plugin for GStreamer
Summary(pl.UTF-8):	Wtyczka udostępniająca źródło i cel obrazu PipeWire dla GStreamera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer >= 1.0
Requires:	gstreamer-plugins-base >= 1.0

%description -n gstreamer-pipewire
PipeWire video sink and source plugin for GStreamer.

%description -n gstreamer-pipewire -l pl.UTF-8
Wtyczka udostępniająca źródło i cel obrazu PipeWire dla GStreamera.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Ddocs=true} \
	%{!?with_gstreamer:-Dgstreamer=false} \
	-Dman=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# packaged as %doc in -apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/pipewire/html

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pipewire
%attr(755,root,root) %{_bindir}/pipewire-cli
%attr(755,root,root) %{_bindir}/pipewire-monitor
%attr(755,root,root) %{_bindir}/spa-inspect
%attr(755,root,root) %{_bindir}/spa-monitor
%dir %{_sysconfdir}/pipewire
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pipewire/pipewire.conf
%{systemduserunitdir}/pipewire.service
%{systemduserunitdir}/pipewire.socket
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-audio-dsp.so
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-autolink.so
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-client-node.so
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-link-factory.so
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-mixer.so
# R: dbus-libs
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-portal.so
# R: systemd-libs
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-protocol-native.so
# R: dbus-libs
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-rtkit.so
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-spa-monitor.so
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-spa-node.so
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-spa-node-factory.so
%attr(755,root,root) %{_libdir}/pipewire-0.2/libpipewire-module-suspend-on-idle.so
%dir %{_libdir}/spa/audiomixer
%attr(755,root,root) %{_libdir}/spa/audiomixer/libspa-audiomixer.so
%dir %{_libdir}/spa/audiotestsrc
%attr(755,root,root) %{_libdir}/spa/audiotestsrc/libspa-audiotestsrc.so
%dir %{_libdir}/spa/support
# R: dbus-libs
%attr(755,root,root) %{_libdir}/spa/support/libspa-dbus.so
%attr(755,root,root) %{_libdir}/spa/support/libspa-support.so
%dir %{_libdir}/spa/test
%attr(755,root,root) %{_libdir}/spa/test/libspa-test.so
%dir %{_libdir}/spa/v4l2
# R: udev-libs
%attr(755,root,root) %{_libdir}/spa/v4l2/libspa-v4l2.so
%dir %{_libdir}/spa/videotestsrc
%attr(755,root,root) %{_libdir}/spa/videotestsrc/libspa-videotestsrc.so
%dir %{_libdir}/spa/volume
%attr(755,root,root) %{_libdir}/spa/volume/libspa-volume.so
%{_mandir}/man1/pipewire.1*
%{_mandir}/man1/pipewire-cli.1*
%{_mandir}/man1/pipewire-monitor.1*
%{_mandir}/man5/pipewire.conf.5*

%files libs
%defattr(644,root,root,755)
%doc LICENSE NEWS README
%attr(755,root,root) %{_libdir}/libpipewire-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpipewire-0.2.so.1
%dir %{_libdir}/pipewire-0.2
%dir %{_libdir}/spa

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpipewire-0.2.so
%{_includedir}/pipewire
%{_includedir}/spa
%{_pkgconfigdir}/libpipewire-0.2.pc
%{_pkgconfigdir}/libspa-0.1.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/design.txt build/doc/html/*
%endif

%files spa-module-alsa
%defattr(644,root,root,755)
%dir %{_libdir}/spa/alsa
# R: alsa-lib udev-libs
%attr(755,root,root) %{_libdir}/spa/alsa/libspa-alsa.so

%files spa-module-bluez
%defattr(644,root,root,755)
%dir %{_libdir}/spa/bluez5
# R: dbus-libs sbc
%attr(755,root,root) %{_libdir}/spa/bluez5/libspa-bluez5.so

%files spa-module-ffmpeg
%defattr(644,root,root,755)
%dir %{_libdir}/spa/ffmpeg
# R: ffmpeg-libs
%attr(755,root,root) %{_libdir}/spa/ffmpeg/libspa-ffmpeg.so

%if %{with gstreamer}
%files -n gstreamer-pipewire
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstpipewire.so
%endif
