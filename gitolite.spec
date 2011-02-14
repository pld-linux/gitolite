# TODO:
# - how is it excpected to cooperate with git-daemon?
# - add dedicated system user
%include	/usr/lib/rpm/macros.perl
Summary:	Software for hosting git repositories
Summary(pl.UTF-8):	Narzędzie do hostowania repozytoriów git
Name:		gitolite
Version:	1.5.9
Release:	1
License:	GPL v2
Group:		Development/Tools
Source0:	http://github.com/sitaramc/gitolite/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	195c3bb527d1873151ee12c46814ae2c
# Use the following script to update Patch0:
# for I in $(ack 'require gitolite' gitolite-1.5.8/ | cut -d: -f1 | sort | uniq ); do mv $I $I.old; sed < $I.old > $I '/require gitolite/iuse lib "/usr/share/gitolite/lib";'; done
# for I in $(ack 'require gitolite' gitolite-1.5.8/ | cut -d: -f1 | sort | uniq | grep -v old); do diff -u $I.old $I; done
Patch0:		lib.patch
URL:		http://github.com/sitaramc/gitolite
BuildRequires:	perl-Text-Markdown
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	git-core
Requires:	openssh-clients
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprov	perl(gitolite)
%define		_noautoreq	perl(gitolite)

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
additional software than git itself and Perl.

%package doc
Summary:	Manual for Gitolite
Summary(fr.UTF-8):	Documentation pour Gitolite
Summary(it.UTF-8):	Documentazione di Gitolite
Summary(pl.UTF-8):	Podręcznik dla Gitolite
Group:		Documentation

%description doc
Documentation for Gitolite.

%description doc -l fr.UTF-8
Documentation pour Gitolite.

%description doc -l it.UTF-8
Documentazione di Gitolite.

%description doc -l pl.UTF-8
Dokumentacja do Gitolite.

%prep
%setup -qc
mv sitaramc-gitolite-*/* .
rm -rf sitaramc-gitolite-*
%patch0 -p1

rm src/gl-system-install

echo %{version} > conf/VERSION
sed -i 's,^# $GL_PACKAGE_CONF =.*,$GL_PACKAGE_CONF = "%{_sysconfdir}/gitolite";,g' conf/example.gitolite.rc
sed -i 's,^# $GL_PACKAGE_HOOKS =.*,$GL_PACKAGE_HOOKS = "%{_datadir}/gitolite/hooks";,g' conf/example.gitolite.rc

# Some ugly hacks. Life without ugly hacks would be so booring.
sed -i 's,^GL_PACKAGE_CONF=.*,GL_PACKAGE_CONF=%{_sysconfdir}/gitolite,g' src/gl-setup
sed -i '2a\GL_ADMIN=$HOME/.gitolite\nGL_BINDIR=%{_bindir}\n' hooks/gitolite-admin/post-update

%build
# Format documentation
for F in doc/*.mkd; do
	perl -MText::Markdown > $(echo $F | sed s/.mkd/.html/) < $F \
		-e 'print Text::Markdown::markdown (join "", <>)'
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/gitolite,%{_datadir}/gitolite/{hooks,lib}}
cp -a src/gl-* src/sshkeys-lint $RPM_BUILD_ROOT%{_bindir}
cp -p src/gitolite.pm $RPM_BUILD_ROOT%{_datadir}/gitolite/lib
cp -p conf/example.gitolite.rc $RPM_BUILD_ROOT%{_sysconfdir}/gitolite
cp -a hooks/* $RPM_BUILD_ROOT%{_datadir}/gitolite/hooks

rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/gitosis/test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.mkd conf/example.conf
%dir %{_sysconfdir}/gitolite
%dir %{_sysconfdir}/gitolite
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gitolite/example.gitolite.rc
%attr(755,root,root) %{_bindir}/gl-*
%attr(755,root,root) %{_bindir}/sshkeys-lint
%dir %{_datadir}/gitolite
%{_datadir}/gitolite/lib
%dir %{_datadir}/gitolite/hooks
%dir %{_datadir}/gitolite/hooks/common
%dir %{_datadir}/gitolite/hooks/gitolite-admin
%attr(755,root,root) %{_datadir}/gitolite/hooks/common/gitolite-hooked
%attr(755,root,root) %{_datadir}/gitolite/hooks/common/post-receive.mirrorpush
%attr(755,root,root) %{_datadir}/gitolite/hooks/common/update
%attr(755,root,root) %{_datadir}/gitolite/hooks/gitolite-admin/post-update

%files doc
%defattr(644,root,root,755)
%doc doc/*
