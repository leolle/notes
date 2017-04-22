#!/bin/bash
cp -R -u org/resources/ ./
git add *
git commit -m "update notes"
git push
