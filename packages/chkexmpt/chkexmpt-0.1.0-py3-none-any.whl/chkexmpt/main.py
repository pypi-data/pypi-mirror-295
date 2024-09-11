import fnmatch
import os
import re
import subprocess
import sys
import shlex
import yaml
from datetime import datetime, timedelta


def parse_blame_output(blame_output, blame_pattern):
    try:
        author = None
        git_hash = None
        timestamp = None
        timestamp_str = None
        match = re.match(blame_pattern, blame_output)

        if match:
            git_hash = match.group(1)
            author = match.group(2)
            timestamp_str = match.group(3)
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S %z")

        return git_hash, author, timestamp

    except Exception as e:
        print(f"[ERROR] could not parse_blame_output: {e}")
        sys.exit(1)


def run_grep(grep_pattern, file_name):
    try:

        grep_result = subprocess.run(
            ["grep", "-n", grep_pattern, shlex.quote(file_name)],
            capture_output=True,
            text=True,
        )

        return grep_result.returncode, grep_result.stdout.splitlines()

    except Exception as e:
        print(f"[ERROR] could not run_grep: {e}")
        sys.exit(1)


def run_git_blame(line_number, file_name):
    try:
        result = subprocess.run(
            [
                "git",
                "blame",
                "-L",
                f"{int(line_number)},{int(line_number)}",
                shlex.quote(file_name),
            ],
            capture_output=True,
            text=True,
        )

        return result.returncode, result.stdout

    except Exception as e:
        print(f"[ERROR] could not run_git_blame: {e}")
        sys.exit(1)


def get_threshold_date(blame_timestamp, allowed_days):
    try:
        threshold_date = datetime.now(tz=blame_timestamp.tzinfo) - timedelta(
            days=allowed_days
        )
        return threshold_date

    except Exception as e:
        print(f"[ERROR] could not get_threshold_date: {e}")
        sys.exit(1)


def run_reporting(results, dryrun):
    for r in sorted(results):
        print(r)

    if results and not dryrun:
        sys.exit(1)


def run(config):
    try:
        # set the required vars
        allowed_days = config["allowed_days"]
        git_blame_pattern = config["git_blame_pattern"]
        directory_path = config["directory_path"]
        ignore_paths = config["ignore_paths"]
        dryrun = config["dryrun"]

        results = set()
        # for each tool, check for it's file patterns and matching
        # lines with exceptions defined
        for tools in config["tool_patterns"]:
            for tool in tools:
                file_patterns = tools[tool]["file_patterns"]
                tool_blame_pattern = tools[tool]["blame_pattern"]
                tool_grep_pattern = tools[tool]["grep_pattern"]
                blame_pattern = rf"{git_blame_pattern}{tool_blame_pattern}"
                files = list_files(file_patterns, directory_path, ignore_paths)

                for file_path in files:
                    # figure out pathing for git blame
                    original_dir = os.getcwd()
                    file_dir = os.path.dirname(file_path)
                    file_name = os.path.basename(file_path)
                    os.chdir(file_dir)

                    try:
                        grep_result, grep_lines = run_grep(tool_grep_pattern, file_name)
                        if grep_result == 0:
                            for line in grep_lines:
                                line_number, line_comment = line.split(":", 1)
                                blame_result, blame_output = run_git_blame(
                                    line_number, file_path
                                )

                                try:
                                    if blame_result == 0:
                                        git_hash, author, blame_timestamp = (
                                            parse_blame_output(
                                                blame_output, blame_pattern
                                            )
                                        )
                                        if blame_timestamp:
                                            # Filter if older than N days
                                            threshold_date = get_threshold_date(
                                                blame_timestamp, allowed_days
                                            )
                                            if blame_timestamp < threshold_date:
                                                results.add(
                                                    f"""
{blame_timestamp}, {git_hash}, {author}
{file_path}
{line_number}, {line_comment.strip()}"""
                                                )
                                except Exception as e:
                                    print(f"[ERROR] parse_blame_output: {e}")
                    finally:
                        os.chdir(original_dir)

                run_reporting(results, dryrun)

    except Exception as e:
        print(f"[ERROR] could not run run: {e}")
        sys.exit(1)


def list_files(file_patterns, directory_path, ignore_paths):
    try:
        matching_files = set()
        for root, dirs, files in os.walk(directory_path):
            # ignore any defined directory paths
            if any(ignore_path in root for ignore_path in ignore_paths):
                continue

            for file in files:
                for file_pattern in file_patterns:
                    if fnmatch.fnmatch(file, file_pattern):
                        matching_files.add(os.path.join(root, file))

        return sorted(matching_files)

    except Exception as e:
        print(f"[ERROR] list_files: {e}")
        sys.exit(1)


def load_config(file_name):
    try:
        # set the defaults, allow local config to override
        default_config = {
            "allowed_days": 30,
            "directory_path": os.getcwd(),
            "dryrun": False,
            "ignore_paths": [".terraform"],
            # below not surfaced to user_configs
            "git_blame_pattern": rf"(\w{{8}}) \((.*?) (\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}} [-+]\d{{4}}) .*?\)\s+",
            "tool_patterns": [
                {
                    "checkov": {
                        "blame_pattern": "#checkov:skip=([^:]+):(.*)",
                        "grep_pattern": "#checkov:skip=",
                        "file_patterns": ["*.tf"],
                    },
                }
            ],
        }
        home_dir = os.path.expanduser("~")
        current_dir = os.getcwd()
        config_paths = [
            os.path.join(home_dir, file_name),
            os.path.join(current_dir, file_name),
        ]

        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r") as file:
                        user_config = yaml.safe_load(file)
                        # Merge the default config with user config
                        # (user config takes precedence)
                        final_config = {**default_config, **user_config}
                        if final_config["dryrun"]:
                            print(
                                f"[INFO] Running in 'dryrun: {final_config['dryrun']}' mode."
                            )

                        return final_config
                except FileNotFoundError:
                    print(f"[INFO] Config file not found. Using default configuration.")
                    return default_config
                except yaml.YAMLError as e:
                    print(
                        f"[ERROR] Failed to parse config file: {e}. Using default configuration."
                    )
                    return default_config

        print(f"[INFO] No config file found. Using default configuration.")
        return default_config
    except Exception as e:
        print(f"[ERROR] could not load_config: {e}")


def main():
    try:
        config_file_name = ".chkexmpt.yml"
        config = load_config(config_file_name)
        run(config)

    except Exception as e:
        print(f"[ERROR] could not run main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
