# Measures what a screen reader on Windows gets from the trial window: the UI
# Automation tree (name, role, value, state) and the Tab route. Narrator and NVDA
# read the same UI Automation data. Usage:
#   powershell -File meet-uia.ps1 -Exe <path to trial exe> [-Tabs 14] [-Out result.txt]
param([Parameter(Mandatory)][string]$Exe, [int]$Tabs = 14, [string]$Out = "")

Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes, System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
}
"@
$A = [System.Windows.Automation.AutomationElement]
$lines = New-Object System.Collections.Generic.List[string]
function Say([string]$s) { $lines.Add($s); Write-Output $s }

function Describe($e) {
    $c = $e.Current
    $role = $c.ControlType.ProgrammaticName -replace '^ControlType\.', ''
    $parts = @("$role", "naam='$($c.Name)'")
    if ($c.IsKeyboardFocusable) { $parts += "focusbaar" }
    if (-not $c.IsEnabled) { $parts += "uitgeschakeld" }
    $p = $null
    if ($e.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern, [ref]$p)) { $parts += "waarde='$($p.Current.Value)'" }
    if ($e.TryGetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern, [ref]$p)) { $parts += "stand=$($p.Current.ToggleState)" }
    if ($e.TryGetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern, [ref]$p)) { $parts += "uitklap=$($p.Current.ExpandCollapseState)" }
    if ($e.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$p)) { $parts += "activeerbaar" }
    return ($parts -join ' | ')
}

function Walk($e, [int]$depth) {
    Say ((' ' * (2 * $depth)) + (Describe $e))
    $walker = [System.Windows.Automation.TreeWalker]::RawViewWalker
    $child = $walker.GetFirstChild($e)
    while ($child -ne $null) {
        Walk $child ($depth + 1)
        $child = $walker.GetNextSibling($child)
    }
}

$proc = Start-Process -FilePath $Exe -PassThru
Start-Sleep -Seconds 4
$proc.Refresh()
$condition = New-Object System.Windows.Automation.PropertyCondition($A::ProcessIdProperty, $proc.Id)
$window = $A::RootElement.FindFirst([System.Windows.Automation.TreeScope]::Children, $condition)
if ($window -eq $null) { Say "Geen venster gevonden"; $proc | Stop-Process; exit 1 }
# The first request only activates AccessKit (it answers with the bare window);
# the full tree follows on the app's next redraw, so move the mouse over the
# window to make it draw again before reading the tree.
[Win]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
$r = $window.Current.BoundingRectangle
foreach ($step in 1..6) {
    [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point([int]($r.Left + 40 * $step), [int]($r.Top + 60 + 20 * $step))
    Start-Sleep -Milliseconds 150
}
# A resize also marks the tree as changed in forks that only push it after a change.
[Win]::SetWindowPos($proc.MainWindowHandle, [IntPtr]::Zero, [int]$r.Left, [int]$r.Top, [int]$r.Width + 2, [int]$r.Height, 0x0014) | Out-Null
Start-Sleep -Seconds 1

Say "== Toegankelijkheidsboom (UI Automation, ruwe weergave)"
Walk $window 0

Say ""
Say "== Tab-route"
[Win]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 500
for ($i = 1; $i -le $Tabs; $i++) {
    [System.Windows.Forms.SendKeys]::SendWait("{TAB}")
    Start-Sleep -Milliseconds 400
    $f = $A::FocusedElement
    $where = if ($f.Current.ProcessId -eq $proc.Id) { Describe $f } else { "buiten het venster" }
    Say ("Tab {0,2}: {1}" -f $i, $where)
}

$proc | Stop-Process
if ($Out) { $lines | Set-Content -Path $Out -Encoding utf8 }
