# TODO:
# - how is it excpected to cooperate with git-daemon?
# - add dedicated system user
%include	/usr/lib/rpm/macros.perl
Summary:	Software for hosting git repositories
Summary(pl.UTF-8):	Narzędzie do hostowania repozytoriów git
Name:		gitolite
Version:	2.3.1
Release:	1
License:	GPL v2
Group:		Development/Tools
Source0:	http://github.com/sitaramc/gitolite/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	096e80901404832445040aef7d733550
Patch0:		%{name}-mkdir.patch
Patch1:		%{name}-env.patch
Patch2:		%{name}-BIG_INFO_CAP.patch
Patch3:		%{name}-broken_links.patch
Patch4:		%{name}-gl_setup.patch
Patch5:		%{name}-wildcard_repos.patch
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

%package contrib
Summary:	Miscellaneous scripts for gitolite
Group:		Development/Tools
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description contrib
Miscellaneous scripts for gitolite

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

rm src/gl-system-install

echo v%{version} > conf/VERSION
sed -i 's,^$GL_PACKAGE_CONF =.*,$GL_PACKAGE_CONF = "%{_sysconfdir}/gitolite";,g' conf/example.gitolite.rc
sed -i 's,^$GL_PACKAGE_HOOKS =.*,$GL_PACKAGE_HOOKS = "%{_datadir}/gitolite/hooks";,g' conf/example.gitolite.rc

# Some ugly hacks. Life without ugly hacks would be so booring.
sed -i 's,^GL_PACKAGE_CONF=.*,GL_PACKAGE_CONF=%{_sysconfdir}/gitolite,g' src/gl-setup

%build
# Copy documentation from contrib
find contrib -name \*.mkd -exec cp '{}' doc \;
# Format documentation
for F in doc/*.mkd; do
	perl -MText::Markdown > $(echo $F | sed s/.mkd/.html/) < $F \
		-e '$text=join("",<>); $text=~s#(\[\w+\]: )http://sitaramc.github.com/gitolite/doc/#$1#g;
                    print Text::Markdown::markdown ($text);'
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/gitolite,%{_datadir}/gitolite/{hooks,contrib},%{perl_vendorlib}}
cp -a src/gl-* src/sshkeys-lint $RPM_BUILD_ROOT%{_bindir}
cp -p src/*.pm $RPM_BUILD_ROOT%{perl_vendorlib}
cp -p conf/{example.gitolite.rc,VERSION} $RPM_BUILD_ROOT%{_sysconfdir}/gitolite
cp -a hooks/* $RPM_BUILD_ROOT%{_datadir}/gitolite/hooks
cp -a contrib/* $RPM_BUILD_ROOT%{_datadir}/gitolite/contrib
find  $RPM_BUILD_ROOT%{_datadir}/gitolite/contrib -name \*.mkd | xargs rm

%{__rm} $RPM_BUILD_ROOT%{_datadir}/gitolite/hooks/common/{gl-pre-git.hub-sample,post-receive.mirrorpush}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.mkd conf/example.conf hooks/common/{gl-pre-git.hub-sample,post-receive.mirrorpush}

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

%files contrib
%defattr(644,root,root,755)
%dir %{_datadir}/gitolite/contrib/
%dir %{_datadir}/gitolite/contrib/adc
%dir %{_datadir}/gitolite/contrib/partial-copy
%dir %{_datadir}/gitolite/contrib/real-users
%dir %{_datadir}/gitolite/contrib/VREF
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/able
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/delete-branch
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/fork
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/get-rights-and-owner.in-perl
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/git
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/git-annex-shell
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/gl-reflog
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/help
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/hub
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/list-trash
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/lock
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/perms
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/restore
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/restrict-admin
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/rm
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/rmrepo
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/rsync
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/sskm
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/sudo
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/su-expand
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/su-getperms
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/symbolic-ref
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/trash
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/unlock
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/watch
%attr(755,root,root) %{_datadir}/gitolite/contrib/adc/who-pushed
%attr(755,root,root) %{_datadir}/gitolite/contrib/mirrorconf-helper.sh
%attr(755,root,root) %{_datadir}/gitolite/contrib/partial-copy/gl-pre-git
%attr(755,root,root) %{_datadir}/gitolite/contrib/partial-copy/t.sh
%attr(755,root,root) %{_datadir}/gitolite/contrib/partial-copy/update.secondary
%attr(755,root,root) %{_datadir}/gitolite/contrib/real-users/gl-shell
%attr(755,root,root) %{_datadir}/gitolite/contrib/real-users/gl-shell-setup
%attr(755,root,root) %{_datadir}/gitolite/contrib/VREF/gl-VREF-COUNT
%attr(755,root,root) %{_datadir}/gitolite/contrib/VREF/gl-VREF-DUPKEYS
%attr(755,root,root) %{_datadir}/gitolite/contrib/VREF/gl-VREF-EMAIL_CHECK
%attr(755,root,root) %{_datadir}/gitolite/contrib/VREF/gl-VREF-FILETYPE
%{_datadir}/gitolite/contrib/VREF/gl-VREF-MERGE_CHECK
%{_datadir}/gitolite/contrib/adc/adc.common-functions
%{_datadir}/gitolite/contrib/adc/getdesc
%{_datadir}/gitolite/contrib/adc/htpasswd
%{_datadir}/gitolite/contrib/adc/pygitolite.py
%{_datadir}/gitolite/contrib/adc/s3backup
%{_datadir}/gitolite/contrib/adc/setdesc
%{_datadir}/gitolite/contrib/adc/su-setperms
%{_datadir}/gitolite/contrib/adc/svnserve
%{_datadir}/gitolite/contrib/gitweb
%{_datadir}/gitolite/contrib/ldap

%files doc
%defattr(644,root,root,755)
%doc doc/*
