%define version	0.99
%define svn	557
%define release %mkrel 4.%svn.1

Summary: 	GUI Download manager using wget
Name: 		gwget
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Networking/File transfer
Source: 	ftp://ftp.gnome.org/pub/gnome/sources/gwget/%{name}-r%{svn}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
#fwang: support epiphany >= 2.19 (from fedora)
Patch1:		gwget-0.99-epiphany219.patch
URL: 		http://gwget.sourceforge.net/
Buildroot: 	%{_tmppath}/%{name}-%{version}-buildroot
Buildrequires:	libgnomeui2-devel
Buildrequires:	libglade2.0-devel
BuildRequires:	gtk+2-devel >= 2.6.0
BuildRequires:  epiphany-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	automake1.7
Requires: 	wget >= 1.10

%description
Gwget is a download manager for GNOME 2. It uses wget as a backend.
Currently, very basic wget options are available, supporting multiple
downloads, drag&drop and display the errors from wget process.

%package -n epiphany-gwget
Summary:	Epiphany extension, using gwget as downloader
Group: 		Networking/File transfer
Requires:	gwget = %{version}
# (Abel) It is impossible to say: "Requires: epiphany = 1.6.x"
Requires:	epiphany

%description -n epiphany-gwget
Gwget is a download manager for GNOME 2. It uses wget as a backend.
Currently, very basic wget options are available, supporting multiple
downloads, drag&drop and display the errors from wget process.

This package contains an extension for epiphany, the GNOME web browser,
which allows the browser to use gwget as an external file downloader.

%prep
%setup -q -n %{name}
%patch1 -p1

%build
./autogen.sh
%configure2_5x --enable-epiphany-extension
%make CFLAGS="%optflags -Wall"

%install
rm -rf %{buildroot}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall_std

sed -i -e 's/^\(Icon=.*\).png$/\1/g' $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

desktop-file-install --vendor='' \
	--dir=%buildroot%_datadir/applications \
	--remove-category='Application' \
	--add-category='FileTransfer;GTK;GNOME' \
	%buildroot%_datadir/applications/*.desktop

install -D -m 0644 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 0644 %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png
install -D -m 0644 %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png
install -D -m 0644 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -D -m 0644 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -D -m 0644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# remove files not bundled
rm -rf %{buildroot}%{_prefix}/doc/ %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/epiphany-1.*/extensions/*a

%find_lang %{name} --with-gnome
 
%post
%update_menus
%update_desktop_database
%update_icon_cache hicolor
%post_install_gconf_schemas %name

%preun
%preun_install_gconf_schemas %name

%postun
%clean_menus
%clean_desktop_database
%clean_icon_cache hicolor

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
