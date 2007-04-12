%define version	0.98.1
%define release %mkrel 1

Summary: 	GUI Download manager using wget
Name: 		gwget
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Networking/File transfer
Source: 	ftp://ftp.gnome.org/pub/gnome/sources/gwget/%{name}-%{version}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
URL: 		http://gwget.sourceforge.net/
Buildroot: 	%{_tmppath}/%{name}-%{version}-buildroot
Buildrequires:	libgnomeui2-devel
Buildrequires:	libglade2.0-devel
BuildRequires:	gtk+2-devel >= 2.6.0
BuildRequires:  epiphany-devel
BuildRequires:	perl-XML-Parser
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
%setup -q

%build
%configure2_5x --enable-epiphany-extension
%make CFLAGS="%optflags -Wall"

%install
rm -rf %{buildroot}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall_std

mkdir -p %{buildroot}/%{_menudir}
cat > %{buildroot}/%{_menudir}/%{name} <<EOF
?package(%{name}): \
 command="%{_bindir}/%{name}" \
 title="Gwget download manager" \
 longtitle="Download manager using wget as backend" \
 needs="x11" \
 icon="%{name}.png" \
 section="Internet/File Transfer"
EOF

install -D -m 0644 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 0644 %{SOURCE2} %{buildroot}%{_iconsdir}/%{name}.png
install -D -m 0644 %{SOURCE3} %{buildroot}%{_liconsdir}/%{name}.png

# remove files not bundled
rm -rf %{buildroot}%{_prefix}/doc/ %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/epiphany-1.*/extensions/*a

%find_lang %{name} --with-gnome
 
%post
%update_menus
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/%{name}.schemas &>/dev/null

%preun
if [ "$1" = "0" ]; then
 export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
 gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas >/dev/null
fi

%postun
%clean_menus 

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr (-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_datadir}/gwget/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_libdir}/bonobo/servers/GNOME_Gwget.server
%{_datadir}/idl/GNOME_Gwget.idl
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files -n epiphany-gwget
%defattr (-,root,root)
%doc COPYING
%{_libdir}/epiphany/*/extensions/*

