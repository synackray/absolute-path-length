#!/usr/bin/env python3
"""Walk a directory and provide a report of all files which exceed the
specified absolute path length."""

import os
import argparse
import logging
from logging.handlers import RotatingFileHandler


# Logging configuration
DEFAULT_LOG_LEVEL = "warn" # Debug, Info, Warn, Error, Critical
log = logging.getLogger(__name__)
log_stream = logging.StreamHandler()
log_file = RotatingFileHandler(
    filename=f"{os.getcwd().split('/')[-1]}.log",
    maxBytes=10 * 1024 * 1024,  # Bytes to Megabytes
    backupCount=5
    )
log.setLevel(getattr(logging, DEFAULT_LOG_LEVEL.upper()))
log_format = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
    )
log_stream.setFormatter(log_format)
log_file.setFormatter(log_format)
log.addHandler(log_stream)
log.addHandler(log_file)

def main():
    """Main function to collect user arguments and execute functions"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--directory", metavar="/home/user/",
        required=True, type=str,
        help="Path to directory of files and folders to check length of."
        )
    parser.add_argument(
        "-c", "--crit", metavar="255",
        default=255, type=int,
        help="Generate critical length log for absolute path if equal or "
             "greater than the specified value."
        )
    parser.add_argument(
        "-l", "--log-level", metavar="info", type=str,
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set logging level for console and log file."
        )
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Don't log anything to console or the log file. Useful when "
             "paired with --report. Default: False"
        )
    parser.add_argument(
        "-r", "--report", action="store_true",
        help="Generate CSV report of files matching warn and critical lengths."
        "Default: False"
        )
    parser.add_argument(
        "-w", "--warn", metavar="225",
        default=225, type=int,
        help="Generate warn length log for absolute path if equal or "
             "greater than the specified value."
        )
    args = parser.parse_args()
    # Adjusts logging if requested
    if args.log_level:
        log.setLevel(getattr(logging, args.log_level.upper()))
    if args.quiet:
        logging.disable(logging.CRITICAL)
    # Process path
    parse_path(
        path=args.directory, path_crit_length=args.crit,
        path_warn_length=args.warn
        )

def parse_path(path, path_crit_length, path_warn_length):
    """Walks the specified directory and checks the lengths of all files and
    sub-directories within it."""
    crit_count, warn_count, total_count = 0, 0, 0
    for item in os.walk(path):
        folder = item[0]
        files = item[-1]
        log.debug("Parsing files in directory: %s", folder)
        for file in files:
            log.debug("Parsing file: %s", file)
            abs_path = os.path.abspath(folder) + "/"
            full_path = abs_path + file
            if len(full_path) >= path_crit_length:
                log.critical("[Length %s] %s", len(full_path), full_path)
                crit_count += 1
            elif len(full_path) >= path_warn_length:
                log.warning("[Length %s] %s", len(full_path), full_path)
                warn_count += 1
            else:
                log.debug("[Length %s] %s", len(full_path), full_path)
                total_count += 1
    log.info(
        "Completed! Processed %s total files, with %s warning and %s critical ",
        total_count, warn_count, crit_count,
        "matches."
        )

if __name__ == "__main__":
    main()
