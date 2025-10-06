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
DefaultGroupName=SpeakAndSpeak
DisableProgramGroupPage=no
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=SpeakAndSpeak-Setup
SetupIconFile=welcome.ico
Compression=lzma2
SolidCompression=no
; License
LicenseFile=LICENSE
; Uninstall Configuration
UninstallDisplayName=SpeakAndSpeak
UninstallDisplayIcon={app}\welcome.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main executables
Source: "SpeakAndSpeak.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "discrimination.exe"; DestDir: "{app}"; Flags: ignoreversion
; Images for application UI
Source: "welcome.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "about.png"; DestDir: "{app}"; Flags: ignoreversion
; Data files
Source: "eng_sentences.tsv"; DestDir: "{app}"; Flags: ignoreversion
Source: "arpabet_ipa_database.csv"; DestDir: "{app}"; Flags: ignoreversion
Source: "ipa_confusion_groups.yaml"; DestDir: "{app}"; Flags: ignoreversion
; Configuration files
Source: "app-config.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "user-data.yaml"; DestDir: "{app}"; Flags: ignoreversion
; Icon file
Source: "welcome.ico"; DestDir: "{app}"; Flags: ignoreversion
; License file
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcuts
Name: "{group}\SpeakAndSpeak"; Filename: "{app}\SpeakAndSpeak.exe"; IconFilename: "{app}\welcome.ico"; Comment: "Launch SpeakAndSpeak Application"
Name: "{group}\Uninstall SpeakAndSpeak"; Filename: "{uninstallexe}"; IconFilename: "{app}\welcome.ico"; Comment: "Uninstall SpeakAndSpeak"
Name: "{group}\License"; Filename: "{app}\LICENSE"; Comment: "View SpeakAndSpeak License"
; Desktop shortcut
Name: "{autodesktop}\SpeakAndSpeak"; Filename: "{app}\SpeakAndSpeak.exe"; IconFilename: "{app}\welcome.ico"; Tasks: desktopicon
; Quick Launch shortcut (optional)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\SpeakAndSpeak"; Filename: "{app}\SpeakAndSpeak.exe"; IconFilename: "{app}\welcome.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\SpeakAndSpeak.exe"; Description: "{cm:LaunchProgram,SpeakAndSpeak}"; Flags: nowait postinstall skipifsilent
