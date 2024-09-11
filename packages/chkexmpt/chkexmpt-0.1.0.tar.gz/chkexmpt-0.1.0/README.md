# Check Exemptions

Check for unintentional security exemptions vs exceptions buried in code. An exception is meant to be temporary, an exemption is permanent. Some SAST tools do not support the reporting or management of exceptions.

This tool currently supports inline checkov exceptions, and diffs the timestamp when each line was committed to the current date. If the exception timestamp exceeds the defined `allowed_days` the scan will fail.

## Install

Run `pip install chkexmpt` to install `chkexmpt`.

>NOTE: requires python >= 3.8 Tested on 3.8 and 3.12

## Usage

Run `chkexmpt` to search all sub-directories for files containing security exceptions.

### Configuration

A config file in the current directory or `~/.chkexmpt.yml` can override default values. Supported attributes are listed below.

```yaml
allowed_days: 30
directory_path: "/Full/path/to/code/directory"
dryrun: false
ignore_paths:
  - ".terraform"
```
