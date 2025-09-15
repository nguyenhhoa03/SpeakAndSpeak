; Inno Setup Script for SpeakAndSpeak Application
; GNU GPL v3 Licensed Application

[Setup]
; Basic Information
AppName=SpeakAndSpeak
AppVersion=1.0.0
AppPublisher=SpeakAndSpeak Project
AppPublisherURL=https://github.com/nguyenhhoa03/SpeakAndSpeak

; Installation Configuration
DefaultDirName={localappdata}\Programs\SpeakAndSpeak
DefaultGroupName=
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=SpeakAndSpeak-Setup
SetupIconFile=welcome.ico
Compression=lzma
SolidCompression=yes

; License
LicenseFile=LICENSE

; Uninstall Configuration
UninstallDisplayName=SpeakAndSpeak
UninstallDisplayIcon={app}\welcome.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Main executable
Source: "app.exe"; DestDir: "{app}"; Flags: ignoreversion

; Images for application UI
Source: "welcome.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "about.png"; DestDir: "{app}"; Flags: ignoreversion

; Data files
Source: "eng_sentences.tsv"; DestDir: "{app}"; Flags: ignoreversion

; Configuration files
Source: "app-config.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "user-data.yaml"; DestDir: "{app}"; Flags: ignoreversion

; Icon file
Source: "welcome.ico"; DestDir: "{app}"; Flags: ignoreversion

; License file
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Desktop shortcut
Name: "{autodesktop}\SpeakAndSpeak"; Filename: "{app}\app.exe"; IconFilename: "{app}\welcome.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\app.exe"; Description: "{cm:LaunchProgram,SpeakAndSpeak}"; Flags: nowait postinstall skipifsilent
