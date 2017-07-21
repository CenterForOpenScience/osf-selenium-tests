#!/bin/bash
echo "hello, $USER. Running a few tests in BrowserStack..."
python Login.py
python CreateComponent.py
python BottomBanner.py
python AddonEnable.py
python DisableAddons.py
python DisconnectAllAccounts.py
python Login.py
python Login.py
python Login.py
python Login.py
python Login.py
python Login.py
python Login.py