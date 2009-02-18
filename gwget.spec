%define epiphany_ver %(rpm -q --whatprovides epiphany-devel --queryformat "%{VERSION}")
%define epiphany_minor %(echo %epiphany_ver | awk -F. '{print $2}')
%define epiphany_major 2.%epiphany_minor
%define epiphany_next_major %(echo 2.$((%epiphany_minor+1)))

Summary: 	GUI Download manager using wget
Name: 		gwget
Version: 	1.0.1
Release: 	%mkrel 1
License: 	GPLv2+
Group: 		Networking/File transfer
Source: 	http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
Patch0:		gwget-1.00-fix-str-fmt.patch
Patch1:     	gwget-1.0.1-new-epiphany.patch
Patch2:		gwget-0.99-fix-dbus-name.patch
Patch3:		gwget-1.00-linkage.patch
Patch4:		gwget-1.0.1-desktop-entry.patch
URL: 		http://gwget.sourceforge.net/
Buildroot: 	%{_tmppath}/%{name}-%{version}-buildroot
Buildrequires:	libgnomeui2-devel
Buildrequires:	libglade2.0-devel
BuildRequires:	gtk+2-devel >= 2.6.0
BuildRequires:  epiphany-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	intltool
BuildRequires:	automake gnome-common
Requires: 	wget >= 1.10

%description
Gwget is a download manager for GNOME 2. It uses wget as a backend.
Currently, very basic wget options are available, supporting multiple
downloads, drag&drop and display the errors from wget process.

%package -n epiphany-gwget
Summary:	Epiphany extension, using gwget as downloader
Group: 		Networking/File transfer
Requires:	gwget = %{version}
Requires:	epiphany >= %epiphany_major
Requires:	epiphany < %epiphany_next_major

%description -n epiphany-gwget
Gwget is a download manager for GNOME 2. It uses wget as a backend.
Currently, very basic wget options are available, supporting multiple
downloads, drag&drop and display the errors from wget process.

This package contains an extension for epiphany, the GNOME web browser,
which allows the browser to use gwget as an external file downloader.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
autoreconf -fi

%build
%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
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
 
%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%update_icon_cache hicolor
%post_install_gconf_schemas %name
%endif

%preun
%preun_install_gconf_schemas %name

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%clean_icon_cache hicolor
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr (-,root,root)
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

%files -n epiphany-gwget
%defattr (-,root,root)
%doc COPYING
%{_libdir}/epiphany/*/extensions/*
