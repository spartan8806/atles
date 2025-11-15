@echo off
REM Upload ATLES embedding model to HuggingFace
REM Make sure you're logged in: huggingface-cli login

echo ====================================
echo ATLES Model Upload to HuggingFace
echo ====================================
echo.
echo Repository: spartan8806/atles
echo Model: atles_embedding_model
echo.

C:\Python313\python.exe upload_model_to_hf.py --model-dir models/atles_embedding_model --repo-id spartan8806/atles

echo.
echo ====================================
echo Upload Complete!
echo ====================================
echo View at: https://huggingface.co/spartan8806/atles
echo.
pause
