-- Hack to maximize window on Safari 10.1: https://groups.google.com/d/msg/webdriver/kWTYSsp73Gw/xbkllkWoBgAJ
tell application "System Events"
	tell process "Safari"
		click button 2 of window 1
		-- button 2 is the green "zoom" button for all applications
		-- window 1 is always the frontmost window
	end tell
end tell
