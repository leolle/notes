#!/bin/bash
rm -rf ./docs/docs/
cp -R -u ./ipynb/site/fonts ./docs/ipynb/site/
cp -R -u ./ipynb/site/ ./docs/ipynb/
git add *

if [ -z "$*" ]
then
    echo "AA"
else
    git commit -m "$*"
    fi
#  else
git commit -m "update notes"
#git checkout master
#git merge home
git push origin master
#git checkout home
