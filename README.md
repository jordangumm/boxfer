# Box Transfer Utility for Linux
Box currently only provides a CLI to developers for OSX and Windows, so I figured I'd create one so I can interface directly with my lab's Box directories.  I plan to eventually implement an automated archive command that can be used via a timed systemd service or cron job.  Right now the only way to use the utility is by leveraging a Developer Token and OAuth 2.0 Credentials, all of which can be acquired by signing up for a developer account at [Box Developers](https://developer.box.com/).

## Setup
Install dependencies:
>$pip install -r requirements.txt
</br>
Populate `config.yaml` with Developer Token and OAuth2.0 Credentials

## Usage
List files and directories:
>$python pyboxfer.py ls [path]
</br>

Download files and full directories:
>$python pyboxfer.py download [path]
