@echo off
REM Upload ATLES Model to Hugging Face
REM Usage: upload_model_to_hf.bat [model_dir] [repo_id]

set MODEL_DIR=%~1
set REPO_ID=%~2

if "%MODEL_DIR%"=="" set MODEL_DIR=atles\training\finetuned_models\atles_qwen2.5_7b
if "%REPO_ID%"=="" set REPO_ID=spartan8806/atles-large

echo Uploading ATLES model to Hugging Face...
echo Model directory: %MODEL_DIR%
echo Repository: %REPO_ID%
echo.

python upload_model_to_hf.py --model_dir "%MODEL_DIR%" --repo_id "%REPO_ID%"

pause

