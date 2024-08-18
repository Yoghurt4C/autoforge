#MaxThreadsPerHotkey 2
CoordMode "Mouse", "Screen"
global Toggle := 0
global x1 := 0
global y1 := 0

;save pos (Ctrl + Q)
^q::{
	global x1
	global y1
    MouseGetPos &x1, &y1
    MsgBox x1 " " y1
}
;eat tomes (Right Alt + [)
>![::{
	global x1
	global y1
	global Toggle
	Toggle := !Toggle
	Loop {
		if Toggle {
			Click x1, y1
			Sleep 100
			Click x1, y1
			Sleep 250
			Click 947, 590
			Sleep 25
		} else {
			break
		}
	}
}
;selectable container, no scrolling support (Right Alt + ])
>!]::{
	global x1
	global y1
	global Toggle
	Toggle := !Toggle
	Loop {
		if Toggle {
			Click x1, y1
			Sleep 100
			Click x1, y1
			Sleep 250
			Click 1060, 514
			Sleep 100
			Click 954, 680
			Sleep 100
			Click 954, 588
			Sleep 25
		} else {
			break
		}
	}
}
;autoforge (Right Alt + K)
>!k::{
    global Toggle
    Toggle := !Toggle
    Loop {
        if Toggle {
            Click 1019, 694
            Sleep 100 
            Click 1126, 694
            Sleep 2150
        } else {
            break
        }
    }
}
;quick exit (Ctrl + P)
^p:: ExitApp
