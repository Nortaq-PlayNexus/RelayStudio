Unicode true
!include "MUI2.nsh"
Name "Relay Studio"
OutFile "..\node_modules\desktop-runtime\RelayStudio-0.4.0-Windows-x64-Setup.exe"
InstallDir "$LOCALAPPDATA\Programs\RelayStudio"
RequestExecutionLevel user
SetCompressor /SOLID lzma
SetCompressorDictSize 64
BrandingText "Relay Studio • Desktop evaluation build"
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"
!define MUI_ABORTWARNING
!define MUI_WELCOMEPAGE_TITLE "A little clarity. A real desktop."
!define MUI_WELCOMEPAGE_TEXT "Install Relay Studio for this Windows user.$\r$\n$\r$\nIncludes the desktop runtime. No separate Node.js installation is needed.$\r$\n$\r$\nModel inference requires an internet connection and your own provider account. Local interface and optional 3D still use system resources.$\r$\n$\r$\nThis is an unsigned evaluation build."
!define MUI_FINISHPAGE_RUN "$INSTDIR\RelayStudio.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Open Relay Studio"
!define MUI_FINISHPAGE_RUN_NOTCHECKED
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"
VIProductVersion "0.4.0.0"
VIAddVersionKey "ProductName" "Relay Studio"
VIAddVersionKey "FileDescription" "Relay Studio Desktop Setup"
VIAddVersionKey "FileVersion" "0.4.0"
VIAddVersionKey "LegalCopyright" "Bundled components retain their respective licenses."
Section "Relay Studio" SEC_MAIN
 SetShellVarContext current
 SetOutPath "$INSTDIR"
 File /r "..\node_modules\desktop-runtime\staging\*"
 WriteUninstaller "$INSTDIR\Uninstall.exe"
 CreateDirectory "$SMPROGRAMS\Relay Studio"
 CreateShortcut "$SMPROGRAMS\Relay Studio\Relay Studio.lnk" "$INSTDIR\RelayStudio.exe" "" "$INSTDIR\resources\app\desktop\icon.ico"
 CreateShortcut "$SMPROGRAMS\Relay Studio\Uninstall Relay Studio.lnk" "$INSTDIR\Uninstall.exe"
 WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelayStudio" "DisplayName" "Relay Studio"
 WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelayStudio" "UninstallString" '$\"$INSTDIR\Uninstall.exe$\"'
 WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelayStudio" "DisplayVersion" "0.4.0"
 WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelayStudio" "InstallLocation" "$INSTDIR"
 WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelayStudio" "DisplayIcon" "$INSTDIR\resources\app\desktop\icon.ico"
 WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelayStudio" "NoModify" 1
 WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelayStudio" "NoRepair" 1
SectionEnd
Section "Uninstall"
 SetShellVarContext current
 RMDir /r "$INSTDIR"
 RMDir /r "$SMPROGRAMS\Relay Studio"
 DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\RelayStudio"
 MessageBox MB_YESNO|MB_ICONQUESTION|MB_DEFBUTTON2 "Also delete this user's Relay Studio settings and encrypted saved keys? Conversation transcripts are not automatically stored here." IDNO keep_data
 RMDir /r "$APPDATA\Relay Studio"
 keep_data:
SectionEnd
