#!/bin/bash
rm -rf ./docs/docs/
cp -R -u ./ipynb/site/fonts ./docs/ipynb/site/
cp -R -u ./ipynb/site/ ./docs/ipynb/
git add *

if [$1]; then
    echo $1
    fi
#then
 #   git commit -m "$1"
  #  else
git commit -m "update notes"
#git checkout master
#git merge home
git push origin master
#git checkout home
