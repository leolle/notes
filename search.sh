#!/bin/bash
grep -inR "$@" . --include \*.org
