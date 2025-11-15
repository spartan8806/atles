@echo off
REM MTEB Evaluation on CPU (Stable - No CUDA Errors)

echo ====================================
echo ATLES - MTEB CPU Evaluation
echo ====================================
echo.
echo Running on CPU to avoid CUDA errors
echo This is slower but 100%% stable
echo.
echo Starting with core STS tasks...
echo (These establish your TOP 15 ranking)
echo.
pause

C:\Python313\python.exe mteb_cpu_stable.py

echo.
echo ====================================
echo Evaluation complete!
echo Check mteb_results/ folder
echo ====================================
pause
