Summary:	External bounce-message translator/formatter for qmail
Name:		qmail-superbounce
Version:	0.9
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	%{name}-%{version}.tar.gz
Requires:	qmail >= 1.03-38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an external bouncer for qmail. It can pack the bounced message
int MIME attachment, tranlsate it to recipient's language, and change
the Date: field to localtime. All of these are configuration options.

%prep
%setup -q

%build
%configure \
	--with-qmail-queue=%{_libdir}/qmail/qmail-queue \
	--with-controldir=%{_sysconfdir}/qmail/control

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR="$RPM_BUILD_ROOT"

echo "superbounce" > $RPM_BUILD_ROOT%{_sysconfdir}/qmail/control/extbouncer
install -d $RPM_BUILD_ROOT%{_sysconfdir}/qmail/alias/
echo "|%{_sbindir}/qmail-superbounce" > $RPM_BUILD_ROOT%{_sysconfdir}/qmail/alias/.qmail-superbounce

gzip -9nf README NEWS ChangeLog

%find_lang %{name}

%post
if [ -f /var/lock/subsys/qmail ]; then
	/etc/rc.d/init.d/qmail restart
fi

%postun
if [ -f /var/lock/subsys/qmail ]; then
	/etc/rc.d/init.d/qmail restart
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/qmail/control/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/qmail/alias/.qmail-superbounce
