# TODO:
# - what to do with .pm file installed in %{_bindir}?
# - how is it excpected to cooperate with git-daemon?
Summary:	Software for hosting git repositories
Summary(pl.UTF-8):	Narzędzie do hostowania repozytoriów git
Name:		gitolite
Version:	1.5.1
Release:	0.1
License:	GPL v2
Group:		Development/Tools
# git://eagain.net/gitosis.git
Source0:	http://github.com/sitaramc/gitolite/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bb5f1ed88cbf96ca5d4fbda2adf5ed3f
Patch0:		%{name}-setup.patch
URL:		http://github.com/sitaramc/gitolite
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	git-core
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gitolite allows a server to host many git repositories and provide
access to many developers, without having to give them real userids on
the server. The essential magic in doing this is ssh's pubkey access
and the authorized_keys file, and the inspiration was an older program
called gitosis.

Gitolite can restrict who can read from (clone/fetch) or write to
(push) a repository. It can also restrict who can push to what branch
or tag, which is very important in a corporate environment. Gitolite
can be installed without requiring root permissions, and with no
additional software than git itself and perl. It also has several
other neat features described below and elsewhere in the doc/
directory.

%prep
%setup -qc

mv sitaramc-gitolite-*/* .
rm -rf sitaramc-gitolite-*

rm src/gl-system-install

echo %{version} > conf/VERSION
sed 's,^# $GL_PACKAGE_CONF =.*, $GL_PACKAGE_CONF = %{_sysconfdir}/gitolite,g' conf/example.gitolite.rc
sed 's,^# $GL_PACKAGE_HOOKS =.*, $GL_PACKAGE_HOOKS = %{_datadir}/gitolite/hooks,g' conf/example.gitolite.rc

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/gitolite,%{_datadir}/gitolite/hooks}
cp src/* $RPM_BUILD_ROOT%{_bindir}
cp -a conf/* $RPM_BUILD_ROOT%{_sysconfdir}/gitolite
cp -a hooks/* $RPM_BUILD_ROOT%{_datadir}/gitolite/hooks

rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/gitosis/test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.mkd doc

%dir %{_sysconfdir}/gitolite
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_datadir}/gitolite
%attr(755,root,root) %{_bindir}/*
