try
	do shell script "/usr/local/bin/cmus-remote -u"
	return true
end try
tell application "System Events"
	set MyList to (name of every process)
end tell
if (MyList contains "Spotify") is true then
	tell application "Spotify" to playpause
	return true
end if
if (MyList contains "iTunes") is true then
	tell application "iTunes" to playpause
	return true
end if
if (MyList contains "VLC") is true then
	tell application "VLC" to play
	return true
end if
if (MyList contains "Google Chrome") is true then
	tell application "Google Chrome"
		repeat with w in (every window)
			repeat with t in every tab of w
				if URL of t contains "play.spotify.com" then
					tell t to execute javascript "(document.getElementById('app-player').contentWindow.document.getElementById('play-pause')).click();"
					return true
				end if
				if URL of t contains "play.google.com/music" then
					tell t to execute javascript "(document.querySelector('[data-id=\"play-pause\"]')).click();"
					return true
				end if
				if URL of t contains "amazon.com/gp/dmusic/mp3/player" then
					tell t to execute javascript "if (window.document.getElementsByClassName('paused').length){ window.amznMusic.widgets.player.resume(); }else{ window.amznMusic.widgets.player.pause(); }"
					return true
				end if
				if URL of t contains "listen.beatsmusic.com" then
					tell t to execute javascript "(document.getElementById('play_pause_icon')).click();"
					return true
				end if
			end repeat
		end repeat
	end tell
end if