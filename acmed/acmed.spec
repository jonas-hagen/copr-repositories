#
# spec file for package acmed

%global debug_package %{nil}
#%%undefine _disable_source_fetch

Name:           acmed
Summary:        A client for the ACME (RFC 8555) protocol.
Version:        0.18.0
Release:        1%{?dist}
License:        MIT or ASL 2.0
Url:            https://github.com/breard-r/acmed
Source0:        https://github.com/breard-r/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define source0sha256 ad8b44fa7efb2e7d72c69f3e20cbbb2119a1346e27a343e6471ea7f45d9fe5c8
ExclusiveArch:  %{rust_arches}
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  rust-packaging
BuildRequires:  systemd-units
BuildRequires:  systemd-rpm-macros

%description
The Automatic Certificate Management Environment (ACME), is an
internet standard (RFC 8555) which allows to automate X.509
certificates signing by a Certification Authority (CA).
ACMEd is one of the many clients for this protocol.

%prep
echo "%{source0sha256}  %{SOURCE0}" | sha256sum -c --
%autosetup -n %{name}-%{version}

%build
make

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 0644 contrib/systemd/acmed.service %{buildroot}%{_unitdir}/acmed.service
install -p -D -m 0644 contrib/systemd/acmed.tmpfiles %{buildroot}%{_tmpfilesdir}/acmed.tmpfiles
install -p -D -m 0644 contrib/systemd/acmed.sysusers %{buildroot}%{_sysusersdir}/acmed.conf
sed -i "s:/usr/bin/acmed:%{_bindir}/acmed:" %{buildroot}%{_unitdir}/acmed.service
sed -i "s:/run/acmed/acmed.pid:%{_rundir}/acmed/acmed.pid:" %{buildroot}%{_unitdir}/acmed.service
sed -i "s:/etc/acmed:%{_sysconfdir}/acmed:" %{buildroot}%{_unitdir}/acmed.service
install -p -D -m 0644 contrib/polkit/10-acmed.rules %{buildroot}%{_datadir}/polkit-1/rules.d/acmed.rules

# Docs
mkdir -p %{buildroot}%{_defaultdocdir}/acmed
install -m644 CHANGELOG.md %{buildroot}%{_defaultdocdir}/acmed/CHANGELOG.md
install -m644 CONTRIBUTING.md %{buildroot}%{_defaultdocdir}/acmed/CONTRIBUTING.md
install -m644 LICENSE-APACHE-2.0.txt %{buildroot}%{_defaultdocdir}/acmed/LICENSE-APACHE-2.0.txt
install -m644 LICENSE-MIT.txt %{buildroot}%{_defaultdocdir}/acmed/LICENSE-MIT.txt
install -m644 README.md %{buildroot}%{_defaultdocdir}/acmed/README.md

install -d -m755 %{buildroot}/run/%{name}/
install -d -m755 %{buildroot}/var/lib/%{name}/
install -d -m755 %{buildroot}/var/lib/%{name}/accounts/
install -d -m755 %{buildroot}/var/lib/%{name}/certs/

%pre
%sysusers_create_compat contrib/systemd/acmed.sysusers

%files
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/acmed
%attr(755, root, root) %{_bindir}/tacd
%attr(644, root, root) %{_mandir}/man5/acmed.toml.5.gz
%attr(644, root, root) %{_mandir}/man8/acmed.8.gz
%attr(644, root, root) %{_mandir}/man8/tacd.8.gz
%attr(-, root, root) %{_defaultdocdir}/acmed/
%config(noreplace) %{_sysconfdir}/acmed/acmed.toml
%config(noreplace) %{_sysconfdir}/acmed/default_hooks.toml
%config(noreplace) %{_sysconfdir}/acmed/letsencrypt.toml
%{_datadir}/polkit-1/rules.d/acmed.rules
%{_unitdir}/acmed.service
%{_tmpfilesdir}/acmed.tmpfiles
%{_sysusersdir}/acmed.conf
%dir /run/%{name}/
%dir /var/lib/%{name}/

%if %{with check}
%check
%cargo_test
%endif

%changelog
* Wed Sep 15 2021 Jonas Hagen <jhca_fedora@qrst.ch> 0.18.0-1
- Run acmed rootless and constrained (please add .well-known path to ReadWritePaths in drop-in service file if using HTTP01 method)
 - Include systemd tempfiles and sysusers
 - Include polkit rule

* Fri Apr 23 2021 Marco Bignami <m.bignami@unknown-domain.no-ip.net> 0.16.0-2
 - Removed group tag.

* Thu Feb 11 2021 Marco Bignami <m.bignami@unknown-domain.no-ip.net> 0.16.0-1
 - Initial build.
