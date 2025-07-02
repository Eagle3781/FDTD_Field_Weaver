@echo off
REM Insert your commit message below:
set COMMIT_MESSAGE=Improved comments and documentation in FDTD simulation code
set BRANCH_NAME=main

cd ../

git checkout %BRANCH_NAME%
git add .
git commit -m "%COMMIT_MESSAGE%"
echo Commit message: %COMMIT_MESSAGE%
echo Would you like to continue?
pause

git pull origin %BRANCH_NAME%
git push origin %BRANCH_NAME%

if %errorlevel% neq 0 (
    echo Error: Failed to push changes to the remote repository.
    exit /b 1
)