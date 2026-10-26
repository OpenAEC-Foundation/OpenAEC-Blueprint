%global debug_package %{nil}
%global __strip /bin/true
%define _build_id_links none

Name:           openaec-blueprint
Version:        %{number}
Release:        1
Summary:        Standard application of OpenAEC tools
License:        CC-BY-SA-4.0 AND LGPL-3.0-only
URL:            https://github.com/OpenAEC-Foundation/OpenAEC-Blueprint
BuildArch:      x86_64

%description
OpenAEC Blueprint shows the shared look, components and icons that every
OpenAEC tool is built from.

%install
install -Dm755 %{_sourcedir}/openaec-blueprint %{buildroot}/usr/bin/openaec-blueprint
install -Dm644 %{_sourcedir}/org.openaec.Blueprint.desktop %{buildroot}/usr/share/applications/org.openaec.Blueprint.desktop
install -Dm644 %{_sourcedir}/icon-256.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/org.openaec.Blueprint.png
install -Dm644 %{_sourcedir}/LICENSE %{buildroot}/usr/share/licenses/openaec-blueprint/LICENSE

%files
/usr/bin/openaec-blueprint
/usr/share/applications/org.openaec.Blueprint.desktop
/usr/share/icons/hicolor/256x256/apps/org.openaec.Blueprint.png
/usr/share/licenses/openaec-blueprint/LICENSE
