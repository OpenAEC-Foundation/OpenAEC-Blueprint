# Presses Tab and reports the focus a screen reader sees, with (-Resize) or
# without (-Peek) a forced redraw after each press, then saves a screenshot.
#   powershell -File meet-tab.ps1 -Exe <trial exe> -Tabs 4 -Out tab.png -Resize
param([string]$Exe, [int]$Tabs, [string]$Out, [switch]$Resize, [switch]$Peek, [int]$Pre = 0)
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes, System.Windows.Forms, System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W2 {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
  public struct RECT { public int Left, Top, Right, Bottom; }
}
"@
[W2]::SetProcessDPIAware() | Out-Null
$A = [System.Windows.Automation.AutomationElement]
$proc = Start-Process -FilePath $Exe -PassThru
Start-Sleep -Seconds 4
$proc.Refresh()
$h = $proc.MainWindowHandle
[W2]::SetForegroundWindow($h) | Out-Null
$cond = New-Object System.Windows.Automation.PropertyCondition($A::ProcessIdProperty, $proc.Id)
$win = $A::RootElement.FindFirst([System.Windows.Automation.TreeScope]::Children, $cond)
Start-Sleep -Milliseconds 500
$r = New-Object W2+RECT
[W2]::GetWindowRect($h, [ref]$r) | Out-Null
if ($Pre) {
    # One redraw first, so AccessKit has the full tree before the Tab presses.
    [W2]::SetWindowPos($h, [IntPtr]::Zero, $r.Left, $r.Top, $r.Right - $r.Left + 2, $r.Bottom - $r.Top, 0x0014) | Out-Null
    Start-Sleep -Milliseconds 800
}
for ($i = 1; $i -le $Tabs; $i++) {
    [System.Windows.Forms.SendKeys]::SendWait("{TAB}")
    Start-Sleep -Milliseconds 300
    if ($Resize) {
        # Force a tree push, then ask what the screen reader would see as focus.
        [W2]::SetWindowPos($h, [IntPtr]::Zero, $r.Left, $r.Top, $r.Right - $r.Left + ($i % 2) * 2, $r.Bottom - $r.Top, 0x0014) | Out-Null
        Start-Sleep -Milliseconds 500
        $f = $A::FocusedElement
        "Tab {0,2}: {1} '{2}'" -f $i, ($f.Current.ControlType.ProgrammaticName -replace '^ControlType\.', ''), $f.Current.Name
    } elseif ($Peek) {
        Start-Sleep -Milliseconds 1500
        $f = $A::FocusedElement
        "Tab {0,2} (zonder hertekenen): {1} '{2}'" -f $i, ($f.Current.ControlType.ProgrammaticName -replace '^ControlType\.', ''), $f.Current.Name
    }
}
Start-Sleep -Milliseconds 400
[W2]::GetWindowRect($h, [ref]$r) | Out-Null
$bmp = New-Object System.Drawing.Bitmap ($r.Right - $r.Left), ($r.Bottom - $r.Top)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($r.Left, $r.Top, 0, 0, $bmp.Size)
$bmp.Save($Out)
$proc | Stop-Process
