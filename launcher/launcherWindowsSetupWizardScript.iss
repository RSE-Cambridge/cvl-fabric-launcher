; MASSIVE/CVL Launcher - easy secure login for the MASSIVE Desktop and the CVL
; Copyright (c) 2012-2013, Monash e-Research Centre (Monash University, Australia)
; All rights reserved.
; 
; This program is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; any later version.
; 
; In addition, redistribution and use in source and binary forms, with or without
; modification, are permitted provided that the following conditions are met:
; 
; -  Redistributions of source code must retain the above copyright
; notice, this list of conditions and the following disclaimer.
; 
; -  Redistributions in binary form must reproduce the above copyright
; notice, this list of conditions and the following disclaimer in the
; documentation and/or other materials provided with the distribution.
; 
; -  Neither the name of the Monash University nor the names of its
; contributors may be used to endorse or promote products derived from
; this software without specific prior written permission.
; 
; THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
; ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
; WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
; IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
; DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
; (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
; ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
; (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
; SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. SEE THE
; GNU GENERAL PUBLIC LICENSE FOR MORE DETAILS.
; 
; You should have received a copy of the GNU General Public License
; along with this program.  If not, see <http://www.gnu.org/licenses/>.
; 
; Enquiries: help@massive.org.au

;MASSIVE Launcher InnoSetup script
;Change OutputDir to suit your build environment

#define LauncherAppName "Strudel"
#define LauncherAppExeName "launcher.exe"

[Setup]
AppName={#LauncherAppName}
AppVersion=0.6.0
;DefaultDirName={pf}\{#LauncherAppName}
DefaultDirName={code:GetDefaultDirName}
DefaultGroupName={#LauncherAppName}
UninstallDisplayIcon={app}\{#LauncherAppExeName}
Compression=lzma2
SolidCompression=yes
;OutputDir=C:\launcher_build\
OutputDir=.

[Files]
Source: "dist\launcher\*.*"; DestDir: "{app}"; Flags: recursesubdirs
; Source: "{#LauncherAppName}.chm"; DestDir: "{app}"
;Source: "Readme.txt"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\{#LauncherAppName}"; Filename: "{app}\{#LauncherAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#LauncherAppName}}"; Filename: "{uninstallexe}"

[Dirs]
;Name: "{pf}\{#LauncherAppName}\openssh-cygwin-stdin-build\tmp"; Permissions: "users-modify"
Name: "{code:GetDefaultDirName}\openssh-cygwin-stdin-build\tmp"; Permissions: "users-modify"

[UninstallRun]
Filename: "{app}\kill-charade-processes.bat";

[Code]
function IsApp2Installed: boolean;
begin
  result := RegKeyExists(HKEY_LOCAL_MACHINE,
    'SOFTWARE\Classes\VncViewer.Config\shell\open\command');
end;

function InitializeSetup: boolean;
begin
  result := IsApp2Installed;
  if not result then
  begin
    result := Msgbox('Cannot find TurboVNC on your system. {#LauncherAppName} requires TurboVNC to be installed. Are you sure you want to continue ?', mbInformation, MB_YESNO) = IDYES;
  end	
end;

function GetDefaultDirName(Param: string): string;
begin
  if IsAdminLoggedOn then
  begin
    Result := ExpandConstant('{pf}\{#LauncherAppName}');
  end
    else
  begin
    Result := ExpandConstant('{userappdata}\{#LauncherAppName}');
  end;
end;
