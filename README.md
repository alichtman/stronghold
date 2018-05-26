![stronghold logo](img/stronghold-logo-left.png)

[![Downloads](http://pepy.tech/badge/stronghold)](http://pepy.tech/count/stronghold)

`stronghold` is the easiest way to securely configure your Mac.

![GIF demo](img/demo.gif)

Designed for MacOS Sierra and High Sierra.
Previously `fortify`.

**Featured On**
---

* [agarrharr/awesome-cli-apps](https://github.com/agarrharr/awesome-cli-apps)
* [jaywcjlove/awesome-mac](https://github.com/jaywcjlove/awesome-mac)
* [smashism/awesome-macadmin-tools](https://github.com/smashism/awesome-macadmin-tools)
* [alebcay/awesome-shell](https://github.com/alebcay/awesome-shell)
* [drduh/macOS-Security-and-Privacy-Guide](https://github.com/drduh/macOS-Security-and-Privacy-Guide#related-software)
* [sb2nov/mac-setup](https://github.com/sb2nov/mac-setup)
* [serhii-londar/open-source-mac-os-apps](https://github.com/serhii-londar/open-source-mac-os-apps)
* [ashishb/osx-and-ios-security-awesome](https://github.com/ashishb/osx-and-ios-security-awesome)
* [timsutton/python-macadmin-tools](https://github.com/timsutton/python-macadmin-tools)
* [morgant/tools-osx](https://github.com/morgant/tools-osx)

**Usage**
---

```
Usage: stronghold.py [OPTIONS]

  Securely configure your Mac.
  Developed by Aaron Lichtman -> (Github: alichtman)


Options:
  -lockdown  Set secure configuration without user interaction.
  -info      Display version and author information and exit.
  -help, -h  Show this message and exit.
```

**Installation Options**
---

1. Install with [`pip`](https://pypi.org/project/stronghold/)
    + `$ pip install stronghold`
    + `$ stronghold`

2. Download and run the `stronghold-script.sh` shell script.
    + `$ sudo ./stronghold-script.sh`

3. Download the `stronghold` binary from Releases tab.


**Configuration Options**
---

1. Firewall

    + Turn on Firewall?
        - This helps protect your Mac from being attacked over the internet.
    + Turn on logging?
        - If there IS an infection, logs are useful for determining the source.
    + Turn on stealth mode?
        - Your Mac will not respond to ICMP ping requests or connection attempts from closed TCP and UDP networks.

2. General System Protection

    + Enable Gatekeeper?
    	- Defend against malware by enforcing code signing and verifying downloaded applications before allowing them to run.
    + Prevent automatic software whitelisting?
        - Both built-in and downloaded software will require user approval for whitelisting.
    + Disable Captive Portal Assistant and force login through browser on untrusted networks?
        - Captive Portal Assistant could be triggered and direct you to a malicious site WITHOUT any user interaction.

3. User Metadata Storage

    + Clear language modeling metadata?
        - This includes user spelling, typing and suggestion data.
    + Disable language modeling data collection?
    + Clear QuickLook metadata?
    + Clear Downloads metadata?
    + Disable metadata collection from Downloads?
    + Clear SiriAnalytics database?

4. User Safety

    + Lock Mac as soon as screen saver starts?
    + Display all file extensions?
    	- This prevents malware from disguising itself as another file type.
    + Disable saving documents to the cloud by default?
        - This prevents sensitive documents from being unintentionally stored on the cloud.
    + Show hidden files in Finder?
    	- This lets you see all files on the system without having to use the terminal.
    + Disable printer sharing?
        - Offers redundancy in case the Firewall was not configured.

**How to Contribute**
---

1. Clone repo and create a new branch: `$ git checkout https://github.com/alichtman/stronghold -b name_for_new_branch`.
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes

**Acknowledgements**
---

+ [@shobrook](www.github.com/shobrook) for logo and UI design assistance.
+ Base logo vector made by [Freepik](https://www.freepik.com/) from [Flaticon](www.flaticon.com).
+ [drduh's macOS-Security-and-Privacy-Guide](https://github.com/drduh/macOS-Security-and-Privacy-Guide) and [Jonathan Levin's MacOS Security Guide](http://newosxbook.com/files/moxii3/AppendixA.pdf) were incredibly helpful while I was building `stronghold`.

**Donations**
---

This is free, open-source software. If you'd like to support the development of future projects, or say thanks for this one, you can donate BTC at `1FnJ8hRRNUtUavngswUD21dsFNezYLX5y9`. Everything is appreciated!
