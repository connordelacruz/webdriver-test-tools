#!/usr/bin/env bash
# Convert README.md and TEST_PROJECTS.md to .rst and output in docs/source/

pandoc -f markdown -t rst -o ./docs/source/README.rst README.md
pandoc -f markdown -t rst -o ./docs/source/TEST_PROJECTS.rst TEST_PROJECTS.md
