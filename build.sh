#!/bin/bash
#
# Build the database and add placename data

set -o errexit   # Exit when a command fails

python build_db.py
python add_placename_data.py
