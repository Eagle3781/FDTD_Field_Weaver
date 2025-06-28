@echo off
REM Insert your commit message below:
set COMMIT_MESSAGE=Your commit message
set BRANCH_NAME=main

git checkout %BRANCH_NAME%
git add .
git commit -m "%COMMIT_MESSAGE%"
git pull origin %BRANCH_NAME%
git push origin %BRANCH_NAME%

if %errorlevel% neq 0 (
    echo Error: Failed to push changes to the remote repository.
    exit /b 1
)