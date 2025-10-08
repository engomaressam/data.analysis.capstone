#!/usr/bin/env python3
"""
Kaggle Upload Automation Script
Automatically uploads datasets and notebooks to Kaggle using the API
"""

import os
import json
import subprocess
import sys
from pathlib import Path
import shutil

class KaggleUploader:
    def __init__(self, credentials_path="kaggle/kaggle.json"):
        """Initialize Kaggle uploader with credentials"""
        self.credentials_path = credentials_path
        self.setup_kaggle_credentials()
    
    def setup_kaggle_credentials(self):
        """Set up Kaggle API credentials"""
        try:
            # Read credentials from JSON file
            with open(self.credentials_path, 'r') as f:
                credentials = json.load(f)
            
            # Set environment variables for Kaggle API
            os.environ['KAGGLE_USERNAME'] = credentials['username']
            os.environ['KAGGLE_KEY'] = credentials['key']
            
            print(f"✅ Kaggle credentials loaded for user: {credentials['username']}")
            
        except FileNotFoundError:
            print(f"❌ Error: Kaggle credentials file not found at {self.credentials_path}")
            print("Please ensure your kaggle.json file is in the correct location")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON in credentials file {self.credentials_path}")
            sys.exit(1)
    
    def run_kaggle_command(self, command):
        """Run a Kaggle API command and return the result"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Command successful: {command}")
                if result.stdout:
                    print(f"Output: {result.stdout}")
                return True
            else:
                print(f"❌ Command failed: {command}")
                print(f"Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Exception running command: {command}")
            print(f"Error: {str(e)}")
            return False
    
    def create_dataset(self, dataset_name, description, files_path, tags=None):
        """Create a new dataset on Kaggle"""
        if tags is None:
            tags = ["bike-share", "transportation", "chicago", "divvy", "data-analysis"]
        
        # Create metadata file
        metadata = {
            "title": dataset_name,
            "id": f"engomaressam/{dataset_name.lower().replace(' ', '-')}",
            "licenses": [{"name": "other"}],
            "keywords": tags,
            "collaborators": [],
            "data": []
        }
        
        # Add files to metadata
        files_path = Path(files_path)
        if files_path.is_file():
            metadata["data"].append({"description": f"{files_path.name}", "name": f"{files_path.name}", "totalBytes": files_path.stat().st_size, "columns": []})
        elif files_path.is_dir():
            for file_path in files_path.glob("*"):
                if file_path.is_file():
                    metadata["data"].append({"description": f"{file_path.name}", "name": f"{file_path.name}", "totalBytes": file_path.stat().st_size, "columns": []})
        
        # Write metadata file
        metadata_path = files_path.parent / "dataset-metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create dataset
        dataset_path = files_path.parent if files_path.is_file() else files_path
        command = f"kaggle datasets create -p {dataset_path}"
        
        print(f"📁 Creating dataset: {dataset_name}")
        return self.run_kaggle_command(command)
    
    def upload_notebook(self, notebook_path, notebook_name, description, tags=None):
        """Upload a notebook to Kaggle"""
        if tags is None:
            tags = ["data-analysis", "python", "pandas", "matplotlib", "seaborn", "business-intelligence"]
        
        notebook_path = Path(notebook_path)
        if not notebook_path.exists():
            print(f"❌ Notebook not found: {notebook_path}")
            return False
        
        # Convert notebook to script if needed (optional)
        print(f"📓 Uploading notebook: {notebook_name}")
        
        # Note: Kaggle API doesn't directly support notebook upload
        # This would need to be done manually through the web interface
        # or converted to a script first
        
        print("⚠️  Note: Notebook upload via API is limited.")
        print("Please upload manually through Kaggle web interface:")
        print("1. Go to kaggle.com/code")
        print("2. Click '+ Create' → 'New Notebook'")
        print("3. Upload your .ipynb file")
        print("4. Add your dataset and run")
        
        return True
    
    def list_datasets(self):
        """List all datasets for the user"""
        print("📊 Listing your datasets:")
        return self.run_kaggle_command("kaggle datasets list --mine")
    
    def list_notebooks(self):
        """List all notebooks for the user"""
        print("📓 Listing your notebooks:")
        return self.run_kaggle_command("kaggle kernels list --mine")

    def ensure_kaggle_cli_path(self):
        """Ensure Kaggle CLI is available on PATH for subprocess calls."""
        if shutil.which("kaggle"):
            return True
        # Try common per-user Scripts path for Windows (Python 3.13)
        user_scripts = os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Roaming", "Python", "Python313", "Scripts")
        kaggle_exe = os.path.join(user_scripts, "kaggle.exe")
        if os.path.exists(kaggle_exe):
            os.environ["PATH"] = user_scripts + os.pathsep + os.environ.get("PATH", "")
            return True
        print("❌ Kaggle CLI not found. Please ensure 'kaggle' is installed and on PATH.")
        print("   Try: pip install --user kaggle")
        return False

    def create_or_update_dataset(self, dataset_dir, version_message="Automated dataset update"):
        """Create a new dataset or update existing dataset version using Kaggle CLI."""
        dataset_dir = Path(dataset_dir)
        metadata_path = dataset_dir / "dataset-metadata.json"
        if not metadata_path.exists():
            print(f"❌ dataset-metadata.json not found in {dataset_dir}. Aborting.")
            return False
        print(f"📁 Ensuring dataset up to date: {dataset_dir}")
        # Try create first
        create_cmd = f"kaggle datasets create -p {dataset_dir}"
        result_create = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)
        if result_create.returncode == 0:
            print(f"✅ Dataset created: {dataset_dir}")
            if result_create.stdout:
                print(f"Output: {result_create.stdout}")
            return True
        # If create failed because already exists, version it
        stderr = (result_create.stderr or "").lower()
        if "already exists" in stderr or "409" in stderr or "conflict" in stderr:
            print("ℹ️ Dataset already exists, creating a new version...")
            version_cmd = f"kaggle datasets version -p {dataset_dir} -m \"{version_message}\""
            result_version = subprocess.run(version_cmd, shell=True, capture_output=True, text=True)
            if result_version.returncode == 0:
                print("✅ Dataset version created successfully")
                if result_version.stdout:
                    print(f"Output: {result_version.stdout}")
                return True
            print("❌ Dataset version failed")
            print(f"Error: {result_version.stderr}")
            return False
        # Unknown failure
        print("❌ Dataset create failed")
        print(f"Error: {result_create.stderr}")
        return False

    def push_kernel(self, kernel_dir):
        """Push a Kaggle kernel from a directory containing kernel-metadata.json."""
        kernel_dir = Path(kernel_dir)
        metadata_path = kernel_dir / "kernel-metadata.json"
        if not metadata_path.exists():
            print(f"❌ kernel-metadata.json not found in {kernel_dir}")
            return False
        print(f"🚀 Pushing Kaggle kernel from: {kernel_dir}")
        push_cmd = f"kaggle kernels push -p {kernel_dir}"
        result_push = subprocess.run(push_cmd, shell=True, capture_output=True, text=True)
        if result_push.returncode == 0:
            print("✅ Kernel pushed successfully")
            if result_push.stdout:
                print(f"Output: {result_push.stdout}")
            return True
        print("❌ Kernel push failed")
        print(f"Error: {result_push.stderr}")
        return False

def main():
    """Main function to demonstrate Kaggle upload automation"""
    print("🚀 Kaggle Upload Automation")
    print("=" * 50)
    
    # Initialize uploader
    uploader = KaggleUploader()

    # Ensure Kaggle CLI is available
    uploader.ensure_kaggle_cli_path()
    
    # Create or update dataset from portfolio directory
    print("\n📁 Creating/Updating Cyclistic Dataset...")
    uploader.create_or_update_dataset(
        dataset_dir="portfolio/kaggle_dataset",
        version_message="Automated update from local portfolio"
    )
    
    # Push Python kernel (automated via CLI)
    print("\n📓 Pushing Python Kernel...")
    uploader.push_kernel(
        kernel_dir="portfolio/kaggle_kernel_python"
    )
    
    # List current datasets and notebooks
    print("\n📊 Current Datasets:")
    uploader.list_datasets()
    
    print("\n📓 Current Notebooks:")
    uploader.list_notebooks()
    
    print("\n✅ Upload automation complete!")
    print("\n📋 Next Steps:")
    print("1. Check your datasets at: https://www.kaggle.com/datasets")
    print("2. Review your kernels at: https://www.kaggle.com/code")
    print("3. Link your notebook to your dataset if needed")
    print("4. Run all cells to test")
    print("5. Make public and share!")

if __name__ == "__main__":
    main()
