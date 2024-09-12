# Check Exemptions

Check for unintentional security exemptions vs exceptions buried in code. An exception is meant to be temporary, an exemption is permanent. Some SAST tools do not support the reporting or management of exceptions.

This tool currently supports inline checkov exceptions, and diffs the timestamp when each line was committed to the current date. If the exception timestamp exceeds the defined `allowed_days` the scan will fail.

## Install

Run `pip install chkexmpt` to install `chkexmpt`.

>NOTE: requires python >= 3.8 Tested on 3.8 and 3.12

## Usage

Run `chkexmpt` to search all sub-directories for files containing security exceptions.

## Output

The output with a single failure would look similar to the example below.

```bash
2024-08-09 12:04:37-07:00, abc1234c, Eric Hoffmann
/home/user1/src/eks-cluster/cluster.tf
cluster.tf,2,#checkov:skip=CKV_TF_1:Ensure Terraform module sources use a commit hash
```

To add an `approved_exemption` for that exception, add the last line to the `approved_exemptions` list in the `.chkexmpt.yml` config.

### Configuration

A config file in the current directory or `~/.chkexmpt.yml` can override default values. Supported attributes are listed below.

```yaml
allowed_days: <integer>
directory_path: "/Full/path/to/code/directory"
dryrun: true|false
ignore_paths:
  - "file/paths"
approved_exemptions:
  - "<fileName>,<lineNumber>,<lineComment>"
```

An example `.chkexmpt.yml` could look like

```yaml
allowed_days: 30
directory_path: "/home/user1/src/project-name"
dryrun: true
ignore_paths:
  - ".terraform"
approved_exemptions:
  - "cluster.tf,2,#checkov:skip=CKV_TF_1:Ensure Terraform module sources use a commit hash"
```
