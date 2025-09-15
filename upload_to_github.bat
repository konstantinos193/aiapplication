@echo off
echo Initializing Git repository...
git init

echo Adding remote origin...
git remote add origin https://github.com/konstantinos193/aiapplication.git

echo Configuring git user...
git config user.name "Nexlify Developer"
git config user.email "developer@nexlify.com"

echo Adding all files...
git add .

echo Creating initial commit...
git commit -m "Initial commit: Nexlify Game Engine"

echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo Done! Check https://github.com/konstantinos193/aiapplication.git
pause
