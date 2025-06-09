#!/bin/bash

# Loop through all .txt files in the current directory
for file in *.txt; do
  # Check if any .txt files exist
  [ -e "$file" ] || continue

  # Extract the base name (remove .txt) and rename to .csv
  mv -- "$file" "${file%.txt}.csv"
done
