@echo off
REM Quick activation script for CUDA PyTorch environment
REM Usage: Just run this file or call it from other scripts

set TMP=D:\temp
set TEMP=D:\temp
if not exist "D:\temp" mkdir "D:\temp"

call D:\atles_pytorch_env\Scripts\activate.bat

echo CUDA PyTorch environment activated!
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"

