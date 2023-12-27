#!/usr/bin/env bash
python3 -m coverage run --omit=tests/* -m pytest tc_python_library_template/tests
python3 -m coverage lcov -o coverage/lcov.info