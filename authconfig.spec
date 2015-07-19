%define _disable_ld_no_undefined 1

Summary:	Command line tool for setting up authentication from network services
Name:		authconfig
Version:	6.2.10
Release:	2
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		https://fedorahosted.org/authconfig
Source0:	https://fedorahosted.org/releases/a/u/%{name}/%{name}-%{version}.tar.bz2
Patch1:		authconfig-6.2.6-gdm-nolastlog.patch
Requires:	newt
Requires:	pam >= 0.99.10.0
Requires:	python
Requires:	pwquality > 0.9
Conflicts:	pam_krb5 < 1.49
Conflicts:	samba-common < 3.0
Conflicts:	samba-client < 3.0
Conflicts:	nss_ldap < 254
Conflicts:	sssd < 0.99.1
Conflicts:	freeipa-client < 2.2.0
Conflicts:	ipa-client < 2.2.0
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(python)
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	perl-XML-Parser
Requires:	/usr/bin/openssl

%description 
Authconfig is a command line utility which can configure a workstation
to use shadow (more secure) passwords.  Authconfig can also configure a
system to be a client for certain networked user information and
authentication schemes.

%package gtk
Summary:	Graphical tool for setting up authentication from network services
Group:		System/Configuration/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	pygtk2.0-libglade >= 2.14.0

%description gtk
Authconfig-gtk is a GUI program which can configure a workstation
to use shadow (more secure) passwords.  Authconfig-gtk can also configure
a system to be a client for certain networked user information and
authentication schemes.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .gdm

%build
%configure --with-python-rev=3
%make

%install
%makeinstall_std
rm %{buildroot}%{_datadir}/%{name}/authconfig-tui.py
ln -s authconfig.py %{buildroot}%{_datadir}/%{name}/authconfig-tui.py

%find_lang %{name}
find %{buildroot}%{_datadir} -name "*.mo" | xargs ./utf8ify-mo


%triggerin -- authconfig <= 5.4.9
authconfig --update --nostart >/dev/null 2>&1 || :

%files -f %{name}.lang
%doc COPYING NOTES TODO README.samba3
%ghost %config(noreplace) %{_sysconfdir}/sysconfig/authconfig
%ghost %config(noreplace) %{_sysconfdir}/pam.d/system-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/password-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/fingerprint-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/smartcard-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/postlogin-ac
%{_sbindir}/cacertdir_rehash
%{_sbindir}/authconfig
%{_sbindir}/authconfig-tui
%exclude %{_mandir}/man8/system-config-authentication.*
%exclude %{_mandir}/man8/authconfig-gtk.*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_libdir}/python*/site-packages/acutilmodule.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/authconfig.py*
%{_datadir}/%{name}/authconfig-tui.py*
%{_datadir}/%{name}/authinfo.py*
%{_datadir}/%{name}/shvfile.py*
%{_datadir}/%{name}/dnsclient.py*
%{_datadir}/%{name}/msgarea.py*
%attr(700,root,root) %dir %{_localstatedir}/lib/%{name}

%files gtk
%{_bindir}/authconfig
%{_bindir}/authconfig-tui
%{_bindir}/authconfig-gtk
%{_bindir}/system-config-authentication
%{_sbindir}/authconfig-gtk
%{_sbindir}/system-config-authentication
%{_mandir}/man8/system-config-authentication.*
%{_mandir}/man8/authconfig-gtk.*
%{_datadir}/%{name}/authconfig.glade
%{_datadir}/%{name}/authconfig-gtk.py*
%config(noreplace) %{_sysconfdir}/pam.d/authconfig-gtk
%config(noreplace) %{_sysconfdir}/pam.d/system-config-authentication
%config(noreplace) %{_sysconfdir}/security/console.apps/authconfig-gtk
%config(noreplace) %{_sysconfdir}/security/console.apps/system-config-authentication
%config(noreplace) %{_sysconfdir}/pam.d/authconfig
%config(noreplace) %{_sysconfdir}/pam.d/authconfig-tui
%config(noreplace) %{_sysconfdir}/security/console.apps/authconfig
%config(noreplace) %{_sysconfdir}/security/console.apps/authconfig-tui
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/16x16/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/22x22/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/24x24/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/32x32/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/48x48/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/256x256/apps/system-config-authentication.*

