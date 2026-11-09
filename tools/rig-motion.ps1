param([Parameter(Mandatory=$true)][int]$SolidWorksProcessId)
$ErrorActionPreference='Stop'
$sw=& 'C:\Users\dy101\.codex\skills\solidworks\scripts\Connect-SolidWorks.ps1' -SolidWorksProcessId $SolidWorksProcessId -PassThru
$i='C:\Program Files\SOLIDWORKS 2025\SOLIDWORKS\api\redist\SolidWorks.Interop.sldworks.dll'
Add-Type -Path $i
Add-Type -ReferencedAssemblies @($i,'System.Web.Extensions') -Path @("$PSScriptRoot\RigMotion.cs","$PSScriptRoot\FinishMotion.cs")
$projectRoot=Split-Path $PSScriptRoot
[RigMotion]::Run($sw,$projectRoot)
[FinishMotion]::Run($sw,$projectRoot)
