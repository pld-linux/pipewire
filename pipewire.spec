# TODO: evl support (BR: libevl-devel, https://evlproject.org/)
# - enable bluez5-codec-lc3
#
# Conditional build:
%bcond_without	apidocs		# Doxygen based API documentation
%bcond_without	ffmpeg		# ffmpeg spa plugin integration
%bcond_without	gstreamer	# GStreamer module
%bcond_without	jack		# pipewire-jack and jack spa plugin integration
%bcond_with	libcamera	# libcamera plugin
%bcond_without	lv2		# LV2 plugins support
%bcond_without	roc		# ROC modules
%bcond_without	x11		# X11 bell support
#
Summary:	PipeWire - server and user space API to deal with multimedia pipelines
Summary(pl.UTF-8):	PipeWire - serwer i API przestrzeni użytkownika do obsługi potoków multimedialnych
Name:		pipewire
Version:	0.3.68
Release:	1
License:	MIT, LGPL v2+, GPL v2
Group:		Libraries
Source0:	https://gitlab.freedesktop.org/pipewire/pipewire/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	e0572cb5ff19411fb51c88b9b156acca
Patch0:		%{name}-gcc.patch
URL:		https://pipewire.org/
BuildRequires:	ModemManager-devel >= 1.10.0
%if %{with jack}
BuildRequires:	SDL2-devel >= 2
%endif
BuildRequires:	Vulkan-Loader-devel >= 1.1.69
BuildRequires:	alsa-lib-devel >= 1.1.7
BuildRequires:	avahi-devel
BuildRequires:	bluez-libs-devel >= 4.101
BuildRequires:	dbus-devel
# rst2man
BuildRequires:	docutils
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	fdk-aac-devel
# libavcodec libavformat libavfilter
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel}
BuildRequires:	gcc >= 6:4.9
BuildRequires:	gettext-tools
%if %{with gstreamer}
BuildRequires:	glib2-devel >= 1:2.32.0
%endif
%{?with_apidocs:BuildRequires:	graphviz}
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= 1.10
BuildRequires:	gstreamer-plugins-base-devel >= 1.10
%endif
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel >= 1.9.17}
BuildRequires:	ldacBT-devel
%ifarch i386 i486 %{armv4} %{armv5} %{armv6}
# possibly more 32-bit archs (where 8-byte __atomic_store_n require libatomic)
BuildRequires:	libatomic-devel
%endif
%{?with_libcamera:BuildRequires:	libcamera-devel}
%{?with_x11:BuildRequires:	libcanberra-devel}
BuildRequires:	libcap-devel
%{?with_libcamera:BuildRequires:	libdrm-devel >= 2.4.98}
BuildRequires:	libfreeaptx-devel
BuildRequires:	libsndfile-devel >= 1.0.20
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libusb-devel >= 1.0
%{?with_lv2:BuildRequires:	lilv-devel}
BuildRequires:	meson >= 0.61.1
BuildRequires:	ncurses-devel
BuildRequires:	ninja >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	opus-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	readline-devel >= 8.1.1-2
%{?with_roc:BuildRequires:	roc-toolkit-devel >= 0.2.0}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRequires:	sbc-devel
BuildRequires:	systemd-devel
BuildRequires:	udev-devel
BuildRequires:	webrtc-audio-processing-devel >= 0.2
BuildRequires:	webrtc-audio-processing-devel < 1.0
%if %{with x11}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel >= 6
%endif
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libsndfile >= 1.0.20
Requires:	pipewire-session-manager
Requires:	systemd-units >= 1:250.1
Suggests:	rtkit
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
BuildArch:	noarch

%description apidocs
API documentation for PipeWire library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PipeWire.

%package spa-module-alsa
Summary:	PipeWire SPA plugin to play and record audio with ALSA API
Summary(pl.UTF-8):	Wtyczka PipeWire SPA do odtwarzania i nagrywania dźwięku przy użyciu API ALSA
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	alsa-lib >= 1.1.7

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
Requires:	bluez-libs >= 4.101

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

%package spa-module-jack
Summary:	PipeWire SPA plugin to play and record audio with JACK API
Summary(pl.UTF-8):	Wtyczka PipeWire SPA do odtwarzania i nagrywania dźwięku przy użyciu API JACK
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	jack-audio-connection-kit >= 1.9.17

%description spa-module-jack
PipeWire SPA plugin to play and record audio with JACK API.

%description spa-module-jack -l pl.UTF-8
Wtyczka PipeWire SPA do odtwarzania i nagrywania dźwięku przy użyciu
API JACK.

%package spa-module-libcamera
Summary:	PipeWire SPA plugin to access cameras through libcamera
Summary(pl.UTF-8):	Wtyczka PipeWire SPA do dostępu do kamer przez libcamera
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description spa-module-libcamera
PipeWire SPA plugin to access cameras through libcamera.

%description spa-module-libcamera -l pl.UTF-8
Wtyczka PipeWire SPA do dostępu do kamer przez libcamera.

%package spa-module-vulkan
Summary:	PipeWire SPA plugin to generate video frames using Vulkan
Summary(pl.UTF-8):	Wtyczka PipeWire SPA do generowania ramek obrazu przy użyciu Vulkana
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	Vulkan-Loader >= 1.1.69

%description spa-module-vulkan
PipeWire SPA plugin to generate video frames using Vulkan.

%description spa-module-vulkan -l pl.UTF-8
Wtyczka PipeWire SPA do generowania ramek obrazu przy użyciu Vulkana.

%package jack
Summary:	PipeWire JACK sound system integration
Summary(pl.UTF-8):	Integracja PipeWire z systemem dźwięku JACK
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	jack-audio-connection-kit >= 1.9.17

%description jack
PipeWire JACK sound system integration.

%description jack -l pl.UTF-8
Integracja PipeWire z systemem dźwięku JACK.

%package pulseaudio
Summary:	PipeWire PulseAudio sound system integration
Summary(pl.UTF-8):	Integracja PipeWire z systemem dźwięku PulseAudio
Group:		Libraries
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	%{name} = %{version}-%{release}
Requires:	systemd-units >= 1:250.1
Suggests:	pulseaudio-tools

%description pulseaudio
PipeWire PulseAudio sound system integration.

%description pulseaudio -l pl.UTF-8
Integracja PipeWire z systemem dźwięku PulseAudio.

%package roc
Summary:	PipeWire ROC streaming integration
Summary(pl.UTF-8):	Integracja PipeWire ze strumieniami ROC
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description roc
PipeWire ROC streaming integration.

%description roc -l pl.UTF-8
Integracja PipeWire ze strumieniami ROC.

%package x11-bell
Summary:	PipeWire module for X11 bell support
Summary(pl.UTF-8):	Moduł PipeWire do obsługi dzwonka X11
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	xorg-lib-libXfixes >= 6

%description x11-bell
PipeWire module for X11 bell support.

%description x11-bell -l pl.UTF-8
Moduł PipeWire do obsługi dzwonka X11.

%package -n alsa-plugin-pipewire
Summary:	PipeWire integration plugin for ALSA sound system
Summary(pl.UTF-8):	Wtyczka systemu dźwięku ALSA integrująca z PipeWire
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	alsa-lib >= 1.1.7

%description -n alsa-plugin-pipewire
PipeWire integration plugin for ALSA sound system.

%description -n alsa-plugin-pipewire -l pl.UTF-8
Wtyczka systemu dźwięku ALSA integrująca z PipeWire.

%package -n gstreamer-pipewire
Summary:	PipeWire video sink and source plugin for GStreamer
Summary(pl.UTF-8):	Wtyczka udostępniająca źródło i cel obrazu PipeWire dla GStreamera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2 >= 1:2.32.0
Requires:	gstreamer >= 1.10
Requires:	gstreamer-plugins-base >= 1.10

%description -n gstreamer-pipewire
PipeWire video sink and source plugin for GStreamer.

%description -n gstreamer-pipewire -l pl.UTF-8
Wtyczka udostępniająca źródło i cel obrazu PipeWire dla GStreamera.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	-Daudiotestsrc=enabled \
	-Dbluez5-backend-hsphfpd=enabled \
	-Dbluez5-backend-native-mm=enabled \
	-Dcompress-offload=enabled \
	%{?with_apidocs:-Ddocs=enabled} \
	%{?with_ffmpeg:-Dffmpeg=enabled} \
	%{!?with_gstreamer:-Dgstreamer=disabled} \
	%{!?with_jack:-Djack=disabled} \
	-Dlibcamera=%{__enabled_disabled libcamera} \
	%{!?with_lv2:-Dlv2=disabled} \
	-Dman=enabled \
	%{!?with_jack:-Dpipewire-jack=disabled} \
	%{!?with_roc:-Droc=disabled} \
	-Dsession-managers='[]' \
	-Dvideotestsrc=enabled \
	-Dvolume=enabled \
	-Dvulkan=enabled \
	-Dx11=%{__enabled_disabled x11}
# TODO: -Devl=enabled

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/pipewire,%{_datadir}/alsa/alsa.conf.d}
cp -p pipewire-alsa/conf/*.conf $RPM_BUILD_ROOT%{_datadir}/alsa/alsa.conf.d

# packaged as %doc in -apidocs
%{?with_apidocs:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/pipewire/html}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_user_post filter-chain.service pipewire.service pipewire.socket

%preun
%systemd_user_preun filter-chain.service pipewire.service pipewire.socket

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post pulseaudio
%systemd_user_post pipewire-pulse.service pipewire-pulse.socket

%preun pulseaudio
%systemd_user_preun pipewire-pulse.service pipewire-pulse.socket

%files -f %{name}.lang
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/security/limits.d/25-pw-rlimits.conf
%attr(755,root,root) %{_bindir}/pipewire
%attr(755,root,root) %{_bindir}/pipewire-aes67
%attr(755,root,root) %{_bindir}/pipewire-avb
%attr(755,root,root) %{_bindir}/pw-cat
%attr(755,root,root) %{_bindir}/pw-cli
%attr(755,root,root) %{_bindir}/pw-dot
%attr(755,root,root) %{_bindir}/pw-dsdplay
%attr(755,root,root) %{_bindir}/pw-dump
%attr(755,root,root) %{_bindir}/pw-encplay
%attr(755,root,root) %{_bindir}/pw-link
%attr(755,root,root) %{_bindir}/pw-loopback
%attr(755,root,root) %{_bindir}/pw-metadata
%attr(755,root,root) %{_bindir}/pw-mididump
%attr(755,root,root) %{_bindir}/pw-midiplay
%attr(755,root,root) %{_bindir}/pw-midirecord
%attr(755,root,root) %{_bindir}/pw-mon
%attr(755,root,root) %{_bindir}/pw-play
%attr(755,root,root) %{_bindir}/pw-profiler
%attr(755,root,root) %{_bindir}/pw-record
%attr(755,root,root) %{_bindir}/pw-reserve
%attr(755,root,root) %{_bindir}/pw-top
%attr(755,root,root) %{_bindir}/pw-v4l2
%attr(755,root,root) %{_bindir}/spa-inspect
%attr(755,root,root) %{_bindir}/spa-json-dump
%attr(755,root,root) %{_bindir}/spa-monitor
# R: libsndfile
%attr(755,root,root) %{_bindir}/spa-resample
%dir %{_sysconfdir}/pipewire
%dir %{_datadir}/pipewire
%{_datadir}/pipewire/client.conf
%{_datadir}/pipewire/client-rt.conf
%{_datadir}/pipewire/filter-chain.conf
%{_datadir}/pipewire/minimal.conf
%{_datadir}/pipewire/pipewire.conf
%{_datadir}/pipewire/pipewire-aes67.conf
%{_datadir}/pipewire/pipewire-avb.conf
%dir %{_datadir}/pipewire/client-rt.conf.avail
%{_datadir}/pipewire/client-rt.conf.avail/20-upmix.conf
%dir %{_datadir}/pipewire/client.conf.avail
%{_datadir}/pipewire/client.conf.avail/20-upmix.conf
%dir %{_datadir}/pipewire/filter-chain
%{_datadir}/pipewire/filter-chain/demonic.conf
%{_datadir}/pipewire/filter-chain/sink-dolby-surround.conf
%{_datadir}/pipewire/filter-chain/sink-eq6.conf
%{_datadir}/pipewire/filter-chain/sink-make-LFE.conf
%{_datadir}/pipewire/filter-chain/sink-matrix-spatialiser.conf
%{_datadir}/pipewire/filter-chain/sink-mix-FL-FR.conf
%{_datadir}/pipewire/filter-chain/sink-virtual-surround-5.1-kemar.conf
%{_datadir}/pipewire/filter-chain/sink-virtual-surround-7.1-hesuvi.conf
%{_datadir}/pipewire/filter-chain/source-duplicate-FL.conf
%{_datadir}/pipewire/filter-chain/source-rnnoise.conf
%dir %{_datadir}/pipewire/pipewire-pulse.conf.avail
%{_datadir}/pipewire/pipewire-pulse.conf.avail/20-upmix.conf
%dir %{_datadir}/pipewire/pipewire.conf.avail
%{_datadir}/pipewire/pipewire.conf.avail/10-rates.conf
%{_datadir}/pipewire/pipewire.conf.avail/20-upmix.conf
%{systemduserunitdir}/filter-chain.service
%{systemduserunitdir}/pipewire.service
%{systemduserunitdir}/pipewire.socket
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-access.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-adapter.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-avb.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-client-device.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-client-node.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-combine-stream.so
# R: webrtc-audio-processing >= 0.2
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-echo-cancel.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-fallback-sink.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-filter-chain.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-link-factory.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-loopback.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-metadata.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-pipe-tunnel.so
# R: dbus-libs
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-portal.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-profiler.so
# R: systemd-libs
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-protocol-native.so
# R: dbus-libs systemd-libs
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-protocol-pulse.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-protocol-simple.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-raop-discover.so
# R: openssl
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-raop-sink.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-rt.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-rtp-sap.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-rtp-session.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-rtp-sink.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-rtp-source.so
# R: dbus-libs
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-rtkit.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-session-manager.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-spa-device.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-spa-device-factory.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-spa-node.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-spa-node-factory.so
# R: avahi-libs
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-zeroconf-discover.so
%attr(755,root,root) %{_libdir}/pipewire-0.3/v4l2/libpw-v4l2.so
%dir %{_libdir}/spa-0.2/aec
%attr(755,root,root) %{_libdir}/spa-0.2/aec/libspa-aec-null.so
# R: webrtc-audio-processing >= 0.2
%attr(755,root,root) %{_libdir}/spa-0.2/aec/libspa-aec-webrtc.so
%dir %{_libdir}/spa-0.2/audioconvert
%attr(755,root,root) %{_libdir}/spa-0.2/audioconvert/libspa-audioconvert.so
%dir %{_libdir}/spa-0.2/audiomixer
%attr(755,root,root) %{_libdir}/spa-0.2/audiomixer/libspa-audiomixer.so
%dir %{_libdir}/spa-0.2/audiotestsrc
%attr(755,root,root) %{_libdir}/spa-0.2/audiotestsrc/libspa-audiotestsrc.so
%dir %{_libdir}/spa-0.2/avb
%attr(755,root,root) %{_libdir}/spa-0.2/avb/libspa-avb.so
%dir %{_libdir}/spa-0.2/control
%attr(755,root,root) %{_libdir}/spa-0.2/control/libspa-control.so
%dir %{_libdir}/spa-0.2/support
# R: dbus-libs
%attr(755,root,root) %{_libdir}/spa-0.2/support/libspa-dbus.so
# R: systemd-libs
%attr(755,root,root) %{_libdir}/spa-0.2/support/libspa-journal.so
%attr(755,root,root) %{_libdir}/spa-0.2/support/libspa-support.so
%dir %{_libdir}/spa-0.2/v4l2
# R: udev-libs
%attr(755,root,root) %{_libdir}/spa-0.2/v4l2/libspa-v4l2.so
%dir %{_libdir}/spa-0.2/videoconvert
%attr(755,root,root) %{_libdir}/spa-0.2/videoconvert/libspa-videoconvert.so
%dir %{_libdir}/spa-0.2/videotestsrc
%attr(755,root,root) %{_libdir}/spa-0.2/videotestsrc/libspa-videotestsrc.so
%dir %{_libdir}/spa-0.2/volume
%attr(755,root,root) %{_libdir}/spa-0.2/volume/libspa-volume.so
%{_mandir}/man1/pipewire.1*
%{_mandir}/man1/pw-cat.1*
%{_mandir}/man1/pw-cli.1*
%{_mandir}/man1/pw-dot.1*
%{_mandir}/man1/pw-link.1*
%{_mandir}/man1/pw-metadata.1*
%{_mandir}/man1/pw-mididump.1*
%{_mandir}/man1/pw-mon.1*
%{_mandir}/man1/pw-profiler.1*
%{_mandir}/man1/pw-top.1*
%{_mandir}/man5/pipewire.conf.5*

%files libs
%defattr(644,root,root,755)
%doc COPYING LICENSE NEWS README.md
%attr(755,root,root) %{_libdir}/libpipewire-0.3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpipewire-0.3.so.0
%dir %{_libdir}/pipewire-0.3
%dir %{_libdir}/pipewire-0.3/v4l2
%dir %{_libdir}/spa-0.2
%dir %{_datadir}/spa-0.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpipewire-0.3.so
%{_includedir}/pipewire-0.3
%{_includedir}/spa-0.2
%{_pkgconfigdir}/libpipewire-0.3.pc
%{_pkgconfigdir}/libspa-0.2.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif

%files spa-module-alsa
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/spa-acp-tool
%dir %{_libdir}/spa-0.2/alsa
# R: alsa-lib udev-libs
%attr(755,root,root) %{_libdir}/spa-0.2/alsa/libspa-alsa.so
%{_datadir}/alsa-card-profile

%files spa-module-bluez
%defattr(644,root,root,755)
%dir %{_libdir}/spa-0.2/bluez5
# R: bluez-libs >= 4.101 dbus-libs libusb >= 1.0 sbc
%attr(755,root,root) %{_libdir}/spa-0.2/bluez5/libspa-bluez5.so
# R: fdk-aac
%attr(755,root,root) %{_libdir}/spa-0.2/bluez5/libspa-codec-bluez5-aac.so
# R: libfreeaptx sbc
%attr(755,root,root) %{_libdir}/spa-0.2/bluez5/libspa-codec-bluez5-aptx.so
# R: sbc
%attr(755,root,root) %{_libdir}/spa-0.2/bluez5/libspa-codec-bluez5-faststream.so
# R: ldacBT
%attr(755,root,root) %{_libdir}/spa-0.2/bluez5/libspa-codec-bluez5-ldac.so
# R: opus
%attr(755,root,root) %{_libdir}/spa-0.2/bluez5/libspa-codec-bluez5-opus.so
# R: sbc
%attr(755,root,root) %{_libdir}/spa-0.2/bluez5/libspa-codec-bluez5-sbc.so
%dir %{_datadir}/spa-0.2/bluez5
%{_datadir}/spa-0.2/bluez5/bluez-hardware.conf

%files spa-module-ffmpeg
%defattr(644,root,root,755)
%dir %{_libdir}/spa-0.2/ffmpeg
# R: ffmpeg-libs
%attr(755,root,root) %{_libdir}/spa-0.2/ffmpeg/libspa-ffmpeg.so

%if %{with jack}
%files spa-module-jack
%defattr(644,root,root,755)
%dir %{_libdir}/spa-0.2/jack
# R: jack-audio-connection-kit-libs
%attr(755,root,root) %{_libdir}/spa-0.2/jack/libspa-jack.so
%endif

%if %{with libcamera}
%files spa-module-libcamera
%defattr(644,root,root,755)
%dir %{_libdir}/spa-0.2/libcamera
# R: libcamera
%attr(755,root,root) %{_libdir}/spa-0.2/libcamera/libspa-libcamera.so
%endif

%files spa-module-vulkan
%defattr(644,root,root,755)
%dir %{_libdir}/spa-0.2/vulkan
# R: Vulkan-Loader
%attr(755,root,root) %{_libdir}/spa-0.2/vulkan/libspa-vulkan.so

%if %{with jack}
%files jack
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pw-jack
%dir %{_libdir}/pipewire-0.3/jack
%attr(755,root,root) %{_libdir}/pipewire-0.3/jack/libjack.so*
%attr(755,root,root) %{_libdir}/pipewire-0.3/jack/libjacknet.so*
%attr(755,root,root) %{_libdir}/pipewire-0.3/jack/libjackserver.so*
%{_datadir}/pipewire/jack.conf
%{_mandir}/man1/pw-jack.1*
%endif

%files pulseaudio
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pipewire-pulse
# R: pulseaudio-libs
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-pulse-tunnel.so
%{_datadir}/pipewire/pipewire-pulse.conf
%{systemduserunitdir}/pipewire-pulse.service
%{systemduserunitdir}/pipewire-pulse.socket
%{_mandir}/man1/pipewire-pulse.1*

%if %{with roc}
%files roc
%defattr(644,root,root,755)
# R: roc-toolkit
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-roc-sink.so
# R: roc-toolkit
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-roc-source.so
%endif

%if %{with x11}
%files x11-bell
%defattr(644,root,root,755)
# R: libX11 libXfixes libcanberra
%attr(755,root,root) %{_libdir}/pipewire-0.3/libpipewire-module-x11-bell.so
%endif

%files -n alsa-plugin-pipewire
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so
%attr(755,root,root) %{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
/lib/udev/rules.d/90-pipewire-alsa.rules

%if %{with gstreamer}
%files -n gstreamer-pipewire
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstpipewire.so
%endif
