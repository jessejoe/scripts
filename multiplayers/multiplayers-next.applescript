try
	do shell script "cmus-remote -n"
	return true
end try
tell application "System Events"
	set MyList to (name of every process)
end tell
if (MyList contains "Spotify") is true then
	tell application "Spotify" to next track
	return true
end if
if (MyList contains "iTunes") is true then
	tell application "iTunes" to next track
	return true
end if
if (MyList contains "VLC") is true then
	tell application "VLC" to next
	return true
end if
if (MyList contains "Google Chrome") is true then
	tell application "Google Chrome"
		repeat with w in (every window)
			repeat with t in every tab of w
				if URL of t contains "play.spotify.com" then
					tell t to execute javascript "(document.getElementById('app-player').contentWindow.document.getElementById('next')).click();"
					#return true
				end if
				if URL of t contains "play.google.com/music" then
					tell t to execute javascript "(document.querySelector('[data-id=\"forward\"]')).click();"
					return true
				end if
				if URL of t contains "amazon.com/gp/dmusic/mp3/player" then
					tell t to execute javascript "window.amznMusic.widgets.player.playHash('next', null, null);"
					return true
				end if
			end repeat
		end repeat
	end tell
end if