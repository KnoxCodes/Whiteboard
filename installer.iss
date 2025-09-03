; Inno Setup Script for Whiteboard App

[Setup]
AppName=Whiteboard
AppVersion=1.0
DefaultDirName={pf}\Whiteboard
DefaultGroupName=Whiteboard
OutputBaseFilename=setup
SetupIconFile=logo1.ico
UninstallDisplayIcon={app}\main.exe
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\logo1.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Whiteboard"; Filename: "{app}\main.exe"; IconFilename: "{app}\logo1.ico"
Name: "{commondesktop}\Whiteboard"; Filename: "{app}\main.exe"; IconFilename: "{app}\logo1.ico"

[Run]
Filename: "{app}\main.exe"; Description: "Launch Whiteboard"; Flags: nowait postinstall skipifsilent
