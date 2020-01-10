Summary:        Tar file manipulation API
Name:           libtar
Version:        1.2.11
Release:        28%{?dist}
License:        MIT
Group:          System Environment/Libraries
URL:            http://www.feep.net/libtar/
Source0:        ftp://ftp.feep.net/pub/software/libtar/libtar-%{version}.tar.gz
Patch0:         http://ftp.debian.org/debian/pool/main/libt/libtar/libtar_1.2.11-4.diff.gz
Patch1:         libtar-1.2.11-missing-protos.patch
Patch2:         libtar-macro.patch
Patch3:         libtar-1.2.11-tar_header.patch
Patch4:         libtar-1.2.11-mem-deref.patch
Patch5:         libtar-1.2.11-fix-memleak.patch
Patch6:         libtar-1.2.11-bz729009.patch
Patch7:         libtar-1.2.11-CVE-2013-4397.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  zlib-devel libtool

%description
libtar is a C library for manipulating tar archives. It supports both
the strict POSIX tar format and many of the commonly-used GNU
extensions.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -z .deb
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .tar_header
%patch4 -p1 -b .deref
%patch5 -p1 -b .fixmem
%patch6 -p1
%patch7 -p1

# set correct version for .so build
%global ltversion %(echo %{version} | tr '.' ':')
sed -i 's/-rpath $(libdir)/-rpath $(libdir) -version-number %{ltversion}/' \
  lib/Makefile.in
# sanitize the macro definitions so that aclocal can find them:
cd autoconf
sed '/^m4_include/d;s/ m4_include/ m4][_include/g' aclocal.m4 >psg.m4
rm acsite.m4 aclocal.m4
cd ..


%build
cp -p /usr/share/libtool/config/config.sub autoconf
# config.guess is not needed, macro %%configure specifies --build
libtoolize --copy
aclocal -I autoconf
autoconf
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
# Without this we get no debuginfo and stripping
chmod +x $RPM_BUILD_ROOT%{_libdir}/libtar.so.%{version}
rm $RPM_BUILD_ROOT%{_libdir}/*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc COPYRIGHT TODO README ChangeLog*
%{_bindir}/%{name}
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/libtar.h
%{_includedir}/libtar_listhash.h
%{_libdir}/lib*.so
%{_mandir}/man3/*.3*


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.2.11-28
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2.11-27
- Mass rebuild 2013-12-27

* Fri Oct 04 2013 Kamil Dudka <kdudka@redhat.com> - 1.2.11-26
- fix CVE-2013-4397: buffer overflows by expanding a specially-crafted archive

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 1.2.11-24
- fix specfile issues reported by the fedora-review script

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 09 2011 Kamil Dudka <kdudka@redhat.com> - 1.2.11-21
- Allow to extract debug-info from /usr/bin/libtar (#729009)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 27 2010 Kamil Dudka <kdudka@redhat.com> - 1.2.11-19
- Completed review of memory leaks related patches (#589056)

* Mon May 3 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.2.11-18
- Fix more memory leaks

* Mon May 3 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.2.11-17
- Fix lot of memory leaks

* Thu Dec 31 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.2.11-16
- Fix invalid memory de-reference issue in BZ #551415

* Fri Nov 20 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.2.11-15
- Fix buffer overflow in BZ #538770

* Tue Sep 22 2009 Stepan Kasal <skasal@redhat.com> - 1.2.11-14
- fix up so that it builds again (#511566)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.11-11
- Fix missing prototype compiler warnings

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.11-10
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.11-9
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.11-8
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.11-7
- Taking over as maintainer since Anvil has other priorities
- Add a bunch of patches from Debian, which build a .so instead of a .a
  and fix a bunch of memory leaks.
- Reinstate a proper devel package as we now build a .so

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.2.11-6.fc5
- Modified URL and added one in Source0

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.2.11-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 0:1.2.11-0.fdr.3
- Merged devel and main packages
- Package provide now libtar-devel

* Tue Jul  8 2003 Dams <anvil[AT]livna.org>
- Initial build.
