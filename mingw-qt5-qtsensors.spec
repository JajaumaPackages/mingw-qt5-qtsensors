%?mingw_package_header

%global qt_module qtsensors
#%%global pre rc1

#%%global snapshot_date 20130510
#%%global snapshot_rev ceec1eda

%if 0%{?snapshot_date}
%global source_folder qt-%{qt_module}
%else
%global source_folder %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
%endif

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-qt5-%{qt_module}
Version:        5.6.0
Release:        2%{?pre:.%{pre}}%{?snapshot_date:.git%{snapshot_date}.%{snapshot_rev}}%{?dist}
Summary:        Qt5 for Windows - QtSensors component

License:        GPLv3 with exceptions or LGPLv2 with exceptions
Group:          Development/Libraries
URL:            http://qt-project.org/

%if 0%{?snapshot_date}
# To regenerate:
# wget http://qt.gitorious.org/qt/%{qt_module}/archive-tarball/%{snapshot_rev} -O qt5-%{qt_module}-%{snapshot_rev}.tar.gz
Source0:        qt5-%{qt_module}-%{snapshot_rev}.tar.gz
%else
%if "%{?pre}" != ""
Source0:        http://download.qt-project.org/development_releases/qt/%{release_version}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0:        http://download.qt-project.org/official_releases/qt/%{release_version}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 96
BuildRequires:  mingw32-qt5-qtbase >= 5.6.0
BuildRequires:  mingw32-qt5-qtdeclarative >= 5.6.0

BuildRequires:  mingw64-filesystem >= 96
BuildRequires:  mingw64-qt5-qtbase >= 5.6.0
BuildRequires:  mingw64-qt5-qtdeclarative >= 5.6.0


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtSensors component

%description -n mingw32-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win64
%package -n mingw64-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtSensors component

%description -n mingw64-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%?mingw_debug_package


%prep
%setup -q -n %{source_folder}


%build
%mingw_qmake_qt5 ../%{qt_module}.pro
%mingw_make %{?_smp_mflags}


%install
%mingw_make install INSTALL_ROOT=$RPM_BUILD_ROOT

# .prl files aren't interesting for us
find $RPM_BUILD_ROOT -name "*.prl" -delete

# Create a list of .dll.debug files which need to be excluded from the main packages
# We do this to keep the %%files section as clean/readable as possible (otherwise every
# single file and directory would have to be mentioned individually in the %%files section)
# Note: the .dll.debug files aren't created yet at this point (as it happens after
# the %%install section). Therefore we have to assume that all .dll files will
# eventually get a .dll.debug counterpart
find $RPM_BUILD_ROOT%{mingw32_prefix} | grep .dll | grep -v .dll.a | sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw32-qt5-%{qt_module}.excludes
find $RPM_BUILD_ROOT%{mingw64_prefix} | grep .dll | grep -v .dll.a | sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw64-qt5-%{qt_module}.excludes


# Win32
%files -n mingw32-qt5-%{qt_module} -f mingw32-qt5-%{qt_module}.excludes
%{mingw32_bindir}/Qt5Sensors.dll
%{mingw32_includedir}/qt5/QtSensors/
%{mingw32_libdir}/libQt5Sensors.dll.a
%{mingw32_libdir}/cmake/Qt5Sensors/
%{mingw32_libdir}/pkgconfig/Qt5Sensors.pc
%{mingw32_libdir}/qt5/plugins/sensorgestures/
%{mingw32_libdir}/qt5/plugins/sensors/
%{mingw32_datadir}/qt5/qml/QtSensors/
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_sensors.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_sensors_private.pri

# Win64
%files -n mingw64-qt5-%{qt_module} -f mingw64-qt5-%{qt_module}.excludes
%{mingw64_bindir}/Qt5Sensors.dll
%{mingw64_includedir}/qt5/QtSensors/
%{mingw64_libdir}/libQt5Sensors.dll.a
%{mingw64_libdir}/cmake/Qt5Sensors/
%{mingw64_libdir}/pkgconfig/Qt5Sensors.pc
%{mingw64_libdir}/qt5/plugins/sensorgestures/
%{mingw64_libdir}/qt5/plugins/sensors/
%{mingw64_datadir}/qt5/qml/QtSensors/
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_sensors.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_sensors_private.pri


%changelog
* Fri Feb 03 2017 Jajauma's Packages <jajauma@yandex.ru> - 5.6.0-2
- Rebuild with GCC 5.4.0

* Thu Apr  7 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-1
- Update to 5.6.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-1
- Update to 5.5.1

* Fri Aug  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 22 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-1
- Update to 5.4.1

* Tue Dec 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-1
- Update to 5.4.0

* Sat Sep 20 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.2-1
- Update to 5.3.2

* Tue Jul  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.1-1
- Update to 5.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.0-1
- Update to 5.3.0

* Sun Mar 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-2
- Make sure we're built against mingw-qt5-qtbase >= 5.2.1 (RHBZ 1077213)

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-4
- Previous commit caused .dll.a files to disappear

* Sun Jan 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-3
- Don't carry .dll.debug files in main package

* Wed Jan  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-2
- Dropped manual rename of import libraries

* Sun Jan  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0

* Fri Nov 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.1.rc1
- Update to 5.2.0 RC1

* Mon Nov 18 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.1-1
- Update to 5.1.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0

* Fri May 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-5.git20130510.ceec1eda
- Update to 20130510 snapshot (rev ceec1eda)

* Sat Feb  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-4.git20130209.f7f1d56c
- Update to 20130209 snapshot (rev f7f1d56c) (upstream hasn't done an official release yet)

* Thu Jan  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-3.git20121112.ac76c8d5
- Fix filelist

* Mon Nov 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.2.beta1.git20121112.ac76c8d5
- Update to 20121112 snapshot (rev ac76c8d5)
- Rebuild against latest mingw-qt5-qtbase
- Dropped pkg-config rename hack as it's unneeded now

* Wed Sep 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.1.beta1
- Initial release

