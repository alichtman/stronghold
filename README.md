# fortify

People like their computers to be secure.

This script makes that easy.

`fortify` is a simple security configuration tool for MacOS Sierra and High Sierra.

[![asciicast demo](https://asciinema.org/a/MGEPQNTustyLj8m9pXKdUbPlM.png)](https://asciinema.org/a/MGEPQNTustyLj8m9pXKdUbPlM?theme=tango&speed=1.15)

**Warnings**
---

+ Ensure you have up-to-date backups. This script modifies system settings and there is always a possibility that it will damage your system.

**Installation Options**
---

1. Install with [pip](https://pypi.org/project/fortify/): `$ pip install fortify`

2. Download this repo as a zip and run with `Python 3`.


**Configuration Options**
---

1. Connectivity

    + Enable Firewall?
        - Enable Logging?
        - Enable Stealth Mode?
        - Prevent Automatic Whitelisting?

    + Disable Captive Portal Assistant?

2. User Metadata Storage and Collection

    + Clear language modeling, spelling and suggestion data and disable data collection?
    + Clear QuickLook metadata and disable logging?
    + Clear and disable SiriAnalytics database?
        - WARNING: This kills Siri.
    + Clear Quarantine Data and disable data collection from downloaded files?

3. General Safety

    + Lock Mac as soon as screen saver starts?
    + Display all file extensions?
    + Disable saving to the cloud by default?
    + Show hidden files in Finder?


**Sources**
-----

+ https://github.com/drduh/macOS-Security-and-Privacy-Guide
+ http://newosxbook.com/files/moxii3/AppendixA.pdf
+ https://pleiades.ucsc.edu/hyades/PF_on_Mac_OS_X

**How to Contribute**
---

1. Clone repo and create a new branch: `$ git checkout https://github.com/alichtman/fortify -b [name_for_new_branch]`.
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes
