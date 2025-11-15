@echo off
REM Submit ATLES to MTEB Leaderboard
REM This runs comprehensive benchmarks and prepares submission

echo ====================================
echo MTEB LEADERBOARD SUBMISSION
echo ====================================
echo.
echo Model: spartan8806/atles
echo Target: TOP 15 Worldwide!
echo.
echo This will take several hours to complete.
echo The script will save progress and can be resumed if interrupted.
echo.
pause

echo.
echo Starting MTEB evaluation...
echo.

C:\Python313\python.exe submit_to_mteb_leaderboard.py

echo.
echo ====================================
echo Check mteb_results/ folder for results
echo ====================================
pause
