#
# spec file for package acmed

#%global debug_package %{nil}

Name:           acmed
Summary:        A client for the ACME protocol.
Version:        0.17.0
Release:        1%{?dist}
License:        MIT
Url:            https://github.com/breard-r/acmed
Source0:        https://github.com/breard-r/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  systemd-units

%description
The Automatic Certificate Management Environment (ACME), is an 
internet standard (RFC 8555) which allows to automate X.509 
certificates signing by a Certification Authority (CA).
ACMEd is one of the many clients for this protocol.

%prep
%autosetup -n %{name}-%{version}


%build
make

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_unitdir}
install -m644 contrib/acmed.service.example %{buildroot}%{_unitdir}/acmed.service
sed -i "s:/usr/local/bin/acmed:%{_bindir}/acmed:" %{buildroot}%{_unitdir}/acmed.service
sed -i "s:/etc/acmed/acmed.pid:%{_localstatedir}/run/acmed.pid:" %{buildroot}%{_unitdir}/acmed.service
sed -i "s:/etc/acmed:%{_sysconfdir}/acmed:" %{buildroot}%{_unitdir}/acmed.service
# Docs
mkdir -p %{buildroot}%{_defaultdocdir}/acmed
install -m644 CHANGELOG.md %{buildroot}%{_defaultdocdir}/acmed/CHANGELOG.md
install -m644 CONTRIBUTING.md %{buildroot}%{_defaultdocdir}/acmed/CONTRIBUTING.md
install -m644 LICENSE-APACHE-2.0.txt %{buildroot}%{_defaultdocdir}/acmed/LICENSE-APACHE-2.0.txt
install -m644 LICENSE-MIT.txt %{buildroot}%{_defaultdocdir}/acmed/LICENSE-MIT.txt
install -m644 README.md %{buildroot}%{_defaultdocdir}/acmed/README.md

%clean
rm -rf %{buildroot}

%pre
getent group acmed >/dev/null || groupadd -r acmed
getent passwd acmed >/dev/null || \
    useradd -r -g acmed -d /etc/acmed -s /sbin/nologin \
    -c "ACMEd" acmed

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/acmed
%attr(755, root, root) %{_bindir}/tacd
%attr(644, root, root) %{_mandir}/man5/acmed.toml.5.gz
%attr(644, root, root) %{_mandir}/man8/acmed.8.gz
%attr(644, root, root) %{_mandir}/man8/tacd.8.gz
%attr(644, root, root) %{_sysconfdir}/acmed/certs
%attr(644, root, root) %{_sysconfdir}/acmed/accounts
%attr(644, root, root) %{_sysconfdir}/acmed/acmed.toml
%attr(644, root, root) %{_sysconfdir}/acmed/default_hooks.toml
%attr(755, root, root) %{_unitdir}/acmed.service
%attr(-, root, root) %{_defaultdocdir}/acmed/


%changelog
* Fri Apr 23 2021 Marco Bignami <m.bignami@unknown-domain.no-ip.net> 0.16.0-2
 - Removed group tag.

* Thu Feb 11 2021 Marco Bignami <m.bignami@unknown-domain.no-ip.net> 0.16.0-1
 - Initial build.
