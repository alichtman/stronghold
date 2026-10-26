#!/bin/bash
# Reads back each setting stronghold -lockdown changes. Exits 1 if any is wrong.
fw=/usr/libexec/ApplicationFirewall/socketfilterfw
status=0

check() {
	local name=$1 expected=$2 output
	shift 2
	output=$("$@" 2>&1)
	if grep -Eqi -- "$expected" <<< "$output"; then
		echo "ok    $name"
	else
		echo "FAIL  $name: $output"
		status=1
	fi
}

check "Firewall on" 'firewall is enabled' $fw --getglobalstate
check "Stealth mode on" 'stealth mode (enabled|is on)' $fw --getstealthmode
check "Signed apps need approval" '^2$' sh -c "$fw --getallowsigned | grep -c DISABLED"
check "Gatekeeper on" '^assessments enabled' spctl --status
check "Captive portal off" '^0$' defaults read /Library/Preferences/SystemConfiguration/com.apple.captive.control Active
check "File extensions shown" '^1$' defaults read NSGlobalDomain AppleShowAllExtensions
check "Cloud saving off" '^0$' defaults read NSGlobalDomain NSDocumentSaveNewDocumentsToCloud
check "Hidden files shown" '^1$' defaults read com.apple.finder AppleShowAllFiles
check "Remote Login off" '^Remote Login: Off$' sudo systemsetup -getremotelogin
check "Apache autostart off" '"org.apache.httpd" => disabled' launchctl print-disabled system
check "Language data cleared" '^0$' sh -c 'ls ~/Library/*/stronghold-test 2>/dev/null | wc -l | tr -d " "'
exit $status
