#!/usr/bin/env bash

pandoc --verbose \
  -o output/manuscript_docx.md \
  -t markdown-simple_tables \
  --atx-headers \
  --wrap=preserve \
  output/manuscript.docx

python build/extract_docx.py
