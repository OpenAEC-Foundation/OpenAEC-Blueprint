# Uses the actions a screen reader offers: press a button (Invoke), toggle a
# checkbox (Toggle), fill a field (SetValue) and open the dialog.
#   powershell -File meet-acties.ps1 -Exe <trial exe>
param([string]$Exe)
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W3 {
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  public struct RECT { public int Left, Top, Right, Bottom; }
}
"@
$A = [System.Windows.Automation.AutomationElement]
$TS = [System.Windows.Automation.TreeScope]
$proc = Start-Process -FilePath $Exe -PassThru
Start-Sleep -Seconds 4
$proc.Refresh(); $h = $proc.MainWindowHandle
$win = $A::RootElement.FindFirst($TS::Children, (New-Object System.Windows.Automation.PropertyCondition($A::ProcessIdProperty, $proc.Id)))
$r = New-Object W3+RECT
function Redraw([int]$d) { [W3]::GetWindowRect($h, [ref]$r) | Out-Null; [W3]::SetWindowPos($h, [IntPtr]::Zero, $r.Left, $r.Top, $r.Right - $r.Left + $d, $r.Bottom - $r.Top, 0x0014) | Out-Null; Start-Sleep -Milliseconds 800 }
function Find([string]$name) { $win.FindFirst($TS::Descendants, (New-Object System.Windows.Automation.PropertyCondition($A::NameProperty, $name))) }
Redraw 2
$save = Find "Opslaan"
"Knop gevonden: $($save -ne $null)"
$p = $save.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
$p.Invoke(); Start-Sleep -Milliseconds 600; $p.Invoke(); Start-Sleep -Milliseconds 600
Redraw -2
"Na twee keer Invoke: tekst 'Opgeslagen: 2 keer' aanwezig = $((Find 'Opgeslagen: 2 keer') -ne $null)"
$box = Find "Rapport meesturen"
$t = $box.GetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern)
$t.Toggle(); Start-Sleep -Milliseconds 600; Redraw 2
"Checkbox na Toggle: $($box.GetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern).Current.ToggleState)"
$edit = Find "Projectnaam"
try { $edit.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).SetValue("Kade 12"); Start-Sleep -Milliseconds 600; Redraw -2
      "Invoerveld na SetValue: '$($edit.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern).Current.Value)'" } catch { "Invoerveld SetValue: fout $($_.Exception.Message)" }
$del = Find ("Verwijderen" + [char]0x2026)
$del.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke(); Start-Sleep -Milliseconds 600; Redraw 2
$dialog = Find "Ligger 2 verwijderen?"
"Dialoog na Invoke zichtbaar in boom: $($dialog -ne $null)"
$opslaan = Find "Opslaan"
"Knop achter de dialoog nog in de boom: $($opslaan -ne $null)"
$proc | Stop-Process
