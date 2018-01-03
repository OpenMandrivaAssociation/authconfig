%define _disable_ld_no_undefined 1

Summary:	Command line tool for setting up authentication from network services
Name:		authconfig
Version:	7.0.1
Release:	1
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		https://pagure.io/authconfig
Source0:	https://releases.pagure.org/%{name}/%{name}-%{version}.tar.bz2
Patch1:		authconfig-6.2.6-gdm-nolastlog.patch
Patch2:		authconfig-7.0.1-nss-update.patch
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
BuildRequires:	pkgconfig(python3)
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	perl-XML-Parser
Requires:	/usr/bin/openssl
%rename %{name}-gtk

%description 
Authconfig is a command line utility which can configure a workstation
to use shadow (more secure) passwords.  Authconfig can also configure a
system to be a client for certain networked user information and
authentication schemes.

%prep
%setup -q -n %{name}-%{version}
%apply_patches

%build
%configure --with-python-rev=3
%make

%install
%makeinstall_std

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
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_libdir}/python*/site-packages/acutil.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/authconfig.py*
%{_datadir}/%{name}/authinfo.py*
%{_datadir}/%{name}/shvfile.py*
%{_datadir}/%{name}/dnsclient.py*
%attr(700,root,root) %dir %{_localstatedir}/lib/%{name}
