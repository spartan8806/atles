@echo off
echo ========================================
echo ATLES Qwen2.5:7B Fine-Tuning Script
echo ========================================
echo.

REM Set temp directory to D: drive to avoid C: drive space issues
set TMP=D:\temp
set TEMP=D:\temp
if not exist "D:\temp" mkdir "D:\temp"

REM Check if virtual environment exists
if not exist "D:\atles_pytorch_env\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found at D:\atles_pytorch_env
    echo Please run the setup first or create the venv manually
    pause
    exit /b 1
)

echo Activating virtual environment with CUDA PyTorch...
call D:\atles_pytorch_env\Scripts\activate.bat

REM Verify CUDA is available
python -c "import torch; exit(0 if torch.cuda.is_available() else 1)" >nul 2>&1
if errorlevel 1 (
    echo WARNING: CUDA not available in virtual environment
    echo Training will use CPU (very slow)
) else (
    echo CUDA GPU detected and ready!
)

echo.
echo Step 2: Preparing training data...
if not exist "training_data\atles_training_data.jsonl" (
    echo Creating sample training data...
    python prepare_training_data.py --output ./training_data/atles_training_data.jsonl
    if errorlevel 1 (
        echo ERROR: Failed to prepare training data
        pause
        exit /b 1
    )
) else (
    echo Training data already exists
)

echo.
echo Step 3: Starting fine-tuning...
echo This may take a while depending on your GPU and data size...
echo.
python finetune_qwen.py --config finetune_config.json

if errorlevel 1 (
    echo ERROR: Fine-tuning failed
    pause
    exit /b 1
)

echo.
echo Step 4: Exporting to Ollama format...
python export_to_ollama.py --finetuned-model ./finetuned_models/atles_qwen2.5_7b --output-dir ./ollama_export

if errorlevel 1 (
    echo WARNING: Export failed, but fine-tuning completed successfully
    echo You can export manually later using:
    echo python export_to_ollama.py --finetuned-model ./finetuned_models/atles_qwen2.5_7b
) else (
    echo.
    echo ========================================
    echo Fine-tuning complete!
    echo ========================================
    echo.
    echo Model exported to: ./ollama_export
    echo See ollama_export/OLLAMA_EXPORT_INSTRUCTIONS.md for next steps
)

pause

