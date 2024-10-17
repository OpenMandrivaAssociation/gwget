%define build_epiphany 0

Summary:	GUI Download manager using wget
Name:		gwget
Version:	1.0.4
Release:	5
License:	GPLv2+
Group:		Networking/File transfer
URL:		https://gwget.sourceforge.net/
Source:		http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
Patch0:		gwget-1.0.2-format-strings.patch
Patch1:		gwget-1.0.4-glib.patch
Patch2:		gwget-0.99-fix-dbus-name.patch
Patch3:		gwget-1.00-linkage.patch
Patch4:		gwget-1.0.4-epiphany-230.patch
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	intltool
BuildRequires:	automake
BuildRequires:	gnome-common
%if %{build_epiphany}
BuildRequires:	pkgconfig(epiphany-3.4)
%else
Obsoletes:	epiphany-gwget < %{version}-%{release}
%endif
Requires:	wget

%description
Gwget is a download manager for GNOME 2. It uses wget as a backend.
Currently, very basic wget options are available, supporting multiple
downloads, drag&drop and display the errors from wget process.

%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_datadir}/dbus-1/services/*.service
%{_datadir}/gwget/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png

#---------------------------------------------------------------------------

%if %{build_epiphany}
%package -n epiphany-gwget
Summary:	Epiphany extension, using gwget as downloader
Group: 		Networking/File transfer
Requires:	gwget = %{version}
Requires:	epiphany

%description -n epiphany-gwget
Gwget is a download manager for GNOME 2. It uses wget as a backend.
Currently, very basic wget options are available, supporting multiple
downloads, drag&drop and display the errors from wget process.

This package contains an extension for epiphany, the GNOME web browser,
which allows the browser to use gwget as an external file downloader.

%files -n epiphany-gwget
%doc COPYING
%{_libdir}/epiphany/*/extensions/*
%endif

#---------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1 -b .format
%patch1 -p1 -b .glib
%patch2 -p1
%patch3 -p1
%patch4 -p0 -b .ep

%build
autoreconf -fi
%configure2_5x --disable-static
%make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall_std

install -D -m 0644 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 0644 %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png
install -D -m 0644 %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png
install -D -m 0644 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -D -m 0644 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -D -m 0644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# remove files not bundled
rm -rf %{buildroot}%{_prefix}/doc/ %{buildroot}%{_includedir}

%find_lang %{name} --with-gnome

