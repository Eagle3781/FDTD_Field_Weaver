@echo off
REM Insert your commit message below:
set COMMIT_MESSAGE=Better git batch scripts
set BRANCH_NAME=main

cd ../

git checkout %BRANCH_NAME%

echo Commit message: %COMMIT_MESSAGE%
echo Branch name: %BRANCH_NAME%
echo Would you like to continue to add and commit only?
pause

git add .
git commit -m "%COMMIT_MESSAGE%"