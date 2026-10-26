; Per-user installer of OpenAEC Blueprint; no administrator rights needed.
; makensis /DNUMBER=2026.44.0 /DSOURCE=<folder with openaec-blueprint.exe> installer.nsi
Unicode true
!include "MUI2.nsh"

Name "OpenAEC Blueprint ${NUMBER}"
OutFile "openaec-blueprint_${NUMBER}_x64-setup.exe"
InstallDir "$LOCALAPPDATA\Programs\OpenAEC Blueprint"
RequestExecutionLevel user
SetCompressor /SOLID lzma
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"
!define UNINST "Software\Microsoft\Windows\CurrentVersion\Uninstall\OpenAEC Blueprint"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Dutch"
!insertmacro MUI_LANGUAGE "English"

VIProductVersion "${NUMBER}.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "OpenAEC Blueprint"
VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "OpenAEC Foundation"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${NUMBER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductVersion" "${NUMBER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "OpenAEC Blueprint installer"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "OpenAEC Foundation"

Section "Install"
  SetOutPath "$INSTDIR"
  File "${SOURCE}\openaec-blueprint.exe"
  File "icon.ico"
  WriteUninstaller "$INSTDIR\uninstall.exe"
  CreateShortcut "$SMPROGRAMS\OpenAEC Blueprint.lnk" "$INSTDIR\openaec-blueprint.exe" "" "$INSTDIR\icon.ico"
  WriteRegStr HKCU "${UNINST}" "DisplayName" "OpenAEC Blueprint"
  WriteRegStr HKCU "${UNINST}" "DisplayVersion" "${NUMBER}"
  WriteRegStr HKCU "${UNINST}" "Publisher" "OpenAEC Foundation"
  WriteRegStr HKCU "${UNINST}" "DisplayIcon" "$INSTDIR\icon.ico"
  WriteRegStr HKCU "${UNINST}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKCU "${UNINST}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINST}" "NoRepair" 1
SectionEnd

Section "Uninstall"
  Delete "$SMPROGRAMS\OpenAEC Blueprint.lnk"
  Delete "$INSTDIR\openaec-blueprint.exe"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\uninstall.exe"
  RMDir "$INSTDIR"
  DeleteRegKey HKCU "${UNINST}"
SectionEnd
