Summary:	External bounce-message translator/formatter for qmail
Summary(pl):	Zewnêtrzny translator/formater odbitych wiadomo¶ci dla qmaila
Name:		qmail-superbounce
Version:	0.95
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	%{name}-%{version}.tar.gz
Requires:	qmail >= 1.03-38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an external bouncer for qmail. It can pack the bounced message
int MIME attachment, tranlasate it to recipient's language, and change
the Date: field to localtime. All of these are configuration options.

%description -l pl
To jest zewnêtrzny bouncer dla qmaila. Mo¿e zapakowaæ odbit± wiadomo¶æ
w za³±cznik MIME, przet³umaczyæ j± na jêzyk odbiorcy, zmieniæ pole
Date: na czas lokalny. Wszystko to ustawia siê w konfiguracji.

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


%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/qmail ]; then
	/etc/rc.d/init.d/qmail restart
fi

%postun
if [ -f /var/lock/subsys/qmail ]; then
	/etc/rc.d/init.d/qmail restart
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README NEWS ChangeLog
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/qmail/control/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/qmail/alias/.qmail-superbounce
