#global relcan 1

# Use newer cmake on EL-6.
%if 0%{?el6}
%global cmake %cmake28
%endif

Name:           OCE
Version:        0.12
Release:        1%{?relcan:.rc%{relcan}}%{?dist}
Summary:        OpenCASCADE Community Edition

License:        Open CASCADE Technology Public License
URL:            https://github.com/tpaviot/oce
# Github source! Archive was generated on the fly with the following URL:
# https://github.com/tpaviot/oce/archive/OCE-0.11.tar.gz
Source0:        oce-%{name}-%{version}%{?relcan:-rc%{relcan}}.tar.gz

Patch0:         OCE-0.11-freeimage.patch

Source1:        DRAWEXE.1
Source2:        opencascade-draw.desktop
Source3:        oce-256.png
Source4:        oce-128.png
Source5:        oce-64.png
Source6:        oce-48.png

# Utilities
%if 0%{?el6}
BuildRequires:  cmake28
%else
BuildRequires:  cmake
%endif
BuildRequires:  desktop-file-utils
# Libraries
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  libXmu-devel
BuildRequires:  ftgl-devel
%if ! 0%{?el6}
BuildRequires:  freeimage-devel
%endif
BuildRequires:  gl2ps-devel
BuildRequires:  libgomp
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
%ifnarch %arm
BuildRequires:  tbb-devel
%endif


%description
OpenCASCADE Community Edition (OCE) is a suite for 3D surface and solid
modeling, visualization, data exchange and rapid application development. It
is an excellent platform for development of numerical simulation software
including CAD/CAM/CAE, AEC and GIS, as well as PDM applications.


%package foundation
Summary:        OpenCASCADE CAE platform shared libraries
Group:          System Environment/Libraries

%description foundation
OpenCASCADE CAE platform shared libraries

This package contains foundation classes which provide a variety of
general-purpose services such as automated management of heap memory,
exception handling, classes for manipulating aggregates of data, basic
math tools.


%package modeling
Summary:        OpenCASCADE CAE platform shared libraries
Group:          System Environment/Libraries

%description modeling
OpenCASCADE CAE platform shared libraries

This package supplies data structures to represent 2D and 3D geometric models,
as well as topological and geometrical algorithms.


%package ocaf
Summary:        OpenCASCADE CAE platform shared libraries
Group:          System Environment/Libraries

%description ocaf
OpenCASCADE CAE platform shared libraries

This package provides OpenCASCADE Application Framework services and
support for data exchange.


%package visualization
Summary:        OpenCASCADE CAE platform shared libraries
Group:          System Environment/Libraries

%description visualization
OpenCASCADE CAE platform shared libraries

This package provides services for displaying 2D and 3D graphics.


%package examples
Summary:        OpenCASCADE CAE platform shared libraries
Group:          System Environment/Libraries

%description examples
OpenCASCADE CAE platform shared libraries

This package contains example input files for OpenCASCADE in various formats.


%package draw
Summary:        OpenCASCADE CAE platform shared libraries
Group:          System Environment/Libraries

%description draw
OpenCASCADE CAE DRAW test harness.


%package devel
Summary:        OpenCASCADE CAE platform library development files
Group:          Development/Libraries
Requires:       %{name}-foundation%{?_isa} = %{version}-%{release}
Requires:       %{name}-modeling%{?_isa} = %{version}-%{release}
Requires:       %{name}-ocaf%{?_isa} = %{version}-%{release}
Requires:       %{name}-visualization%{?_isa} = %{version}-%{release}

%description devel
OpenCASCADE CAE platform library development files


%prep
%setup -q -n oce-%{name}-%{version}
#patch0 -p1 -b .cmake_freeimage

# Convert files to utf8
iconv --from=ISO-8859-1 --to=UTF-8 LICENSE.txt > LICENSE.txt.new && \
touch -r LICENSE.txt LICENSE.txt.new && \
mv LICENSE.txt.new LICENSE.txt


%build
rm -rf build && mkdir build && pushd build
# Stop excessive linking that cmake projects are prone to. 
LDFLAGS="-Wl,--as-needed";export LDFLAGS
%cmake -DOCE_BUILD_TYPE=RelWithDebInfo \
       -DOCE_INSTALL_PREFIX=%{_prefix} \
       -DOCE_INSTALL_LIB_DIR=%{_lib} \
       -DOCE_WITH_FREEIMAGE=ON \
       -DOCE_WITH_GL2PS=ON \
       -DOCE_MULTITHREAD_LIBRARY:STRING=TBB \
       -DOCE_DRAW=on \
       ../

make %{?_smp_mflags}


%install
pushd build
make install DESTDIR=%{buildroot}

# Remove empty .gxx files
find %{buildroot}%{_includedir} -name "*.gxx" -exec rm -f {} \;

# Install manpage for DRAWEXE
install -Dm 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/DRAWEXE.1

# Install and validate desktop file
desktop-file-install                           \
    --dir=%{buildroot}%{_datadir}/applications \
    %{SOURCE2}

# Install icons
for size in 256 128 64 48; do
    icon=%{_sourcedir}/oce-${size}.png
    install -Dm 0644 $icon \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/oce.png
done


%post foundation -p /sbin/ldconfig
%postun foundation -p /sbin/ldconfig

%post modeling -p /sbin/ldconfig
%postun modeling -p /sbin/ldconfig

%post ocaf -p /sbin/ldconfig
%postun ocaf -p /sbin/ldconfig

%post visualization -p /sbin/ldconfig
%postun visualization -p /sbin/ldconfig

%post draw
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun draw
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans draw
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files foundation
%doc AUTHORS LICENSE.txt NEWS
# Foundation
%{_libdir}/libTKernel.so.*
%{_libdir}/libTKMath.so.*
%{_libdir}/libTKAdvTools.so.*
%{_datadir}/oce-%{version}%{?relcan:-rc%{relcan}}/

%files modeling
# Modeling Data
%{_libdir}/libTKG2d.so.*
%{_libdir}/libTKG3d.so.*
%{_libdir}/libTKGeomBase.so.*
%{_libdir}/libTKBRep.so.*
# Modeling Algorithms
%{_libdir}/libTKGeomAlgo.so.*
%{_libdir}/libTKTopAlgo.so.*
%{_libdir}/libTKPrim.so.*
%{_libdir}/libTKBO.so.*
%{_libdir}/libTKHLR.so.*
%{_libdir}/libTKMesh.so.*
%{_libdir}/libTKShHealing.so.*
%{_libdir}/libTKXMesh.so.*
%{_libdir}/libTKBool.so.*
%{_libdir}/libTKFillet.so.*
%{_libdir}/libTKFeat.so.*
%{_libdir}/libTKOffset.so.*
# Data exchange
%{_libdir}/libTKSTL.so.*
%{_libdir}/libTKXSBase.so.*
%{_libdir}/libTKSTEPBase.so.*
%{_libdir}/libTKIGES.so.*
%{_libdir}/libTKSTEPAttr.so.*
%{_libdir}/libTKSTEP209.so.*
%{_libdir}/libTKSTEP.so.*
%{_libdir}/libTKVRML.so.*
%{_libdir}/libTKXCAF.so.*
%{_libdir}/libTKXCAFSchema.so.*
%{_libdir}/libTKXmlXCAF.so.*
%{_libdir}/libTKBinXCAF.so.*
%{_libdir}/libTKXDEIGES.so.*
%{_libdir}/libTKXDESTEP.so.*

%files visualization
# Visualization Dependents
%{_libdir}/libTKService.so.*
%{_libdir}/libTKV2d.so.*
%{_libdir}/libTKV3d.so.*
# Visualization
%{_libdir}/libTKOpenGl.so.*
%{_libdir}/libTKMeshVS.so.*
%{_libdir}/libTKNIS.so.*
%{_libdir}/libTKVoxel.so.*

%files ocaf
# Application framework
%{_libdir}/libTKCDF.so.*
%{_libdir}/libPTKernel.so.*
%{_libdir}/libTKLCAF.so.*
%{_libdir}/libFWOSPlugin.so.*
%{_libdir}/libTKPShape.so.*
%{_libdir}/libTKBinL.so.*
%{_libdir}/libTKXmlL.so.*
%{_libdir}/libTKPLCAF.so.*
%{_libdir}/libTKTObj.so.*
%{_libdir}/libTKShapeSchema.so.*
%{_libdir}/libTKStdLSchema.so.*
%{_libdir}/libTKCAF.so.*
%{_libdir}/libTKBin.so.*
%{_libdir}/libTKXml.so.*
%{_libdir}/libTKPCAF.so.*
%{_libdir}/libTKBinTObj.so.*
%{_libdir}/libTKXmlTObj.so.*
%{_libdir}/libTKStdSchema.so.*

%files draw
# Draw Libraries
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/libTKDraw.so.*
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/libTKTopTest.so.*
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/libTKViewerTest.so.*
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/libTKXSDRAW.so.*
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/libTKDCAF.so.*
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/libTKXDEDRAW.so.*
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/libTKTObjDRAW.so.*
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/libTKQADraw.so.*
# DRAWEXE application
%{_bindir}/DRAWEXE
%{_mandir}/man1/DRAWEXE.1.gz
%{_datadir}/applications/opencascade-draw.desktop
%{_datadir}/icons/hicolor/*/apps/*

%files devel
%doc examples
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/*.so
%{_libdir}/oce-%{version}%{?relcan:-rc%{relcan}}/*.cmake


%changelog
* Tue Jul 15 2013 Richard Shaw <hobbes1069@gmail.com> - 0.12-1
- Update to latest upstream release as it adds some performance enhancements.

* Mon Feb 18 2013 Richard Shaw <hobbes1069@gmail.com> - 0.11-2
- Add tbb-devel as build requirement.

* Fri Feb 15 2013 Richard Shaw <hobbes1069@gmail.com> - 0.11-1
- Update to latest upstream release.

* Wed May 02 2012 Richard Shaw <hobbes1069@gmail.com> - 0.8.0-3
- Update icons.

* Mon Dec 19 2011 Richard Shaw <hobbes1069@gmail.com> - 0.8.0-2
- Build against OpenMP for parallelization.
- Fix problem with OCE overriding build flags.

* Mon Dec 12 2011 Richard Shaw <hobbes1069@gmail.com> - 0.8.0-1
- Update to 0.8.0.
- Use %%{buildroot} consistently.
- Fix excess linking.

* Tue Nov 08 2011 Richard Shaw <hobbes1069@gmail.com> - 0.7.0-1
- Initial release.
