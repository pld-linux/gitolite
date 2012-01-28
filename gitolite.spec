# TODO:
# - how is it excpected to cooperate with git-daemon?
# - add dedicated system user
%include	/usr/lib/rpm/macros.perl
Summary:	Software for hosting git repositories
Summary(pl.UTF-8):	Narzędzie do hostowania repozytoriów git
Name:		gitolite
Version:	2.2.1
Release:	2
License:	GPL v2
Group:		Development/Tools
Source0:	http://github.com/sitaramc/gitolite/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9ad2611deab29f65d1c033d17b5fda38
Patch0:		%{name}-mkdir.patch
Patch1:		%{name}-env.patch
Patch2:		%{name}-BIG_INFO_CAP.patch
Patch3:		%{name}-broken_links.patch
Patch4:		%{name}-gl_setup.patch
Patch5:		%{name}-wildcard_repos.patch
Patch6:         %{name}-nogitweb.patch
URL:		http://github.com/sitaramc/gitolite
BuildRequires:	perl-Text-Markdown
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	git-core
Requires:	openssh-server
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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

rm src/gl-system-install

echo v%{version} > conf/VERSION
sed -i 's,^# $GL_PACKAGE_CONF =.*,$GL_PACKAGE_CONF = "%{_sysconfdir}/gitolite";,g' conf/example.gitolite.rc
sed -i 's,^# $GL_PACKAGE_HOOKS =.*,$GL_PACKAGE_HOOKS = "%{_datadir}/gitolite/hooks";,g' conf/example.gitolite.rc

# Some ugly hacks. Life without ugly hacks would be so booring.
sed -i 's,^GL_PACKAGE_CONF=.*,GL_PACKAGE_CONF=%{_sysconfdir}/gitolite,g' src/gl-setup
sed -i '2a\GL_ADMIN=$HOME/.gitolite\nGL_BINDIR=%{_bindir}\n' hooks/gitolite-admin/post-update

%build
# Format documentation
for F in doc/*.mkd; do
	perl -MText::Markdown > $(echo $F | sed s/.mkd/.html/) < $F \
		-e '$text=join("",<>); $text=~s#(\[\w+\]: )http://sitaramc.github.com/gitolite/doc/#$1#g;
                    print Text::Markdown::markdown ($text);'
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/gitolite,%{_datadir}/gitolite/hooks,%{perl_vendorlib}}
cp -a src/gl-* src/sshkeys-lint $RPM_BUILD_ROOT%{_bindir}
cp -p src/*.pm $RPM_BUILD_ROOT%{perl_vendorlib}
cp -p conf/{example.gitolite.rc,VERSION} $RPM_BUILD_ROOT%{_sysconfdir}/gitolite
cp -a hooks/* $RPM_BUILD_ROOT%{_datadir}/gitolite/hooks

%{__rm} $RPM_BUILD_ROOT%{_datadir}/gitolite/hooks/common/{gl-pre-git.hub-sample,update.secondary.sample,post-receive.mirrorpush}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.mkd conf/example.conf hooks/common/{gl-pre-git.hub-sample,update.secondary.sample,post-receive.mirrorpush}

%dir %{_sysconfdir}/gitolite
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gitolite/example.gitolite.rc
%{_sysconfdir}/gitolite/VERSION
%attr(755,root,root) %{_bindir}/gl-*
%attr(755,root,root) %{_bindir}/sshkeys-lint
%dir %{_datadir}/gitolite
%{perl_vendorlib}/gitolite*.pm
%dir %{_datadir}/gitolite/hooks
%dir %{_datadir}/gitolite/hooks/common
%dir %{_datadir}/gitolite/hooks/gitolite-admin
%attr(755,root,root) %{_datadir}/gitolite/hooks/common/gitolite-hooked
%attr(755,root,root) %{_datadir}/gitolite/hooks/common/update
%attr(755,root,root) %{_datadir}/gitolite/hooks/gitolite-admin/post-update

%files doc
%defattr(644,root,root,755)
%doc doc/*
