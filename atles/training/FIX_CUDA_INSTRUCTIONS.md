# Fix CUDA Support for PyTorch

## Problem
PyTorch is installed with CPU-only support (`2.7.1+cpu`), but you have an NVIDIA RTX 3060 GPU with CUDA 13.0 available.

## Solution

### Option 1: Free Disk Space and Install CUDA PyTorch (Recommended)

1. **Free up at least 3GB on C: drive** (PyTorch CUDA version is ~2.5GB)

2. **Run PowerShell as Administrator** and execute:
```powershell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

3. **Verify CUDA is working**:
```powershell
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

### Option 2: Install to User Location (If you can't free system space)

If you can't free space on C: drive, try installing to user location:

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 --user
```

**Note**: This may still fail if temp directory (usually C:\Windows\Temp) is full.

### Option 3: Use Virtual Environment on Different Drive

If you have space on D: drive:

```powershell
# Create venv on D: drive
python -m venv D:\atles_env

# Activate it
D:\atles_env\Scripts\Activate.ps1

# Install CUDA PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

## Why This Happened

When you installed the fine-tuning requirements earlier, pip installed the CPU-only version of PyTorch because:
- The CPU version is smaller and installs by default
- Your system had the CPU version already installed
- pip didn't detect you needed CUDA support

## After Installing CUDA PyTorch

Once CUDA PyTorch is installed, run the verification again:

```powershell
cd atles\training
python verify_setup.py
```

You should see:
```
[OK] CUDA available
[OK] GPU device count: 1
[OK] GPU 0: NVIDIA GeForce RTX 3060
```

## Quick Check Commands

```powershell
# Check current PyTorch
python -c "import torch; print(torch.__version__); print('CUDA:', torch.cuda.is_available())"

# Check GPU
nvidia-smi

# Check disk space
Get-PSDrive C | Select-Object Used,Free
```

