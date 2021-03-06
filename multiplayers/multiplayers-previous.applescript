try
	do shell script "/usr/local/bin/cmus-remote -r"
	return true
end try
tell application "System Events"
	set MyList to (name of every process)
end tell
if (MyList contains "VOX") is true then
	tell application "VOX" to previous track
	return true
end if
if (MyList contains "Spotify") is true then
	tell application "Spotify.app" to �event spfyPrev�
	return true
end if
if (MyList contains "iTunes") is true then
	tell application "iTunes" to previous track
	return true
end if
if (MyList contains "VLC") is true then
	tell application "VLC" to previous
	return true
end if
if (MyList contains "Google Chrome") is true then
	tell application "Google Chrome"
		repeat with w in (every window)
			repeat with t in every tab of w
				if URL of t contains "player.spotify.com" then
					tell t to execute javascript "(document.getElementById('main').contentWindow.document.getElementById('previous')).click();"
					return true
				end if
				if URL of t contains "play.google.com/music" then
					tell t to execute javascript "(document.querySelector('[data-id=\"rewind\"]')).click();"
					return true
				end if
				if URL of t contains "amazon.com/gp/dmusic/mp3/player" then
					tell t to execute javascript "window.amznMusic.widgets.player.playHash('previous', null, null);"
					return true
				end if
				if URL of t contains "listen.beatsmusic.com" then
					tell t to execute javascript "(document.getElementById('t-prev')).click();"
					return true
				end if
			end repeat
		end repeat
	end tell
end if