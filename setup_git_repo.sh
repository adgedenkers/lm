base_directory=$1
if [ -z "$base_directory" ]; then
    base_directory=basename "$PWD"
fi

git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/adgedenkers/{$base_directory}.git
git push -u origin main