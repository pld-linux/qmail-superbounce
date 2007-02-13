Summary:	External bounce-message translator/formatter for qmail
Summary(pl.UTF-8):	Zewnętrzny translator/formater odbitych wiadomości dla qmaila
Name:		qmail-superbounce
Version:	0.95
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://duch.mimuw.edu.pl/~hunter/%{name}-%{version}.tar.gz
# Source0-md5:	e9ae74a7f31c4cbd24c3f6f8cadfb9d1
Requires:	qmail >= 1.03-38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an external bouncer for qmail. It can pack the bounced message
int MIME attachment, tranlasate it to recipient's language, and change
the Date: field to localtime. All of these are configuration options.

%description -l pl.UTF-8
To jest zewnętrzny bouncer dla qmaila. Może zapakować odbitą wiadomość
w załącznik MIME, przetłumaczyć ją na język odbiorcy, zmienić pole
Date: na czas lokalny. Wszystko to ustawia się w konfiguracji.

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qmail/control/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qmail/alias/.qmail-superbounce
