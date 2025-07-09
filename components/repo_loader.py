import os
import shutil
import stat
import time
from git import Repo, GitCommandError

# Function for cloning a repositry
def handle_remove_readonly(func, path, _):
    """
    Helper to force remove read-only files on Windows
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(repo_url, clone_dir="repo_temp"):
    try:
        if os.path.exists(clone_dir):
            print("🧹 Cleaning old repo_temp...")
            shutil.rmtree(clone_dir, onerror=handle_remove_readonly)
            time.sleep(0.5)  # give Windows time to release handles

        print("🔄 Cloning repository...")
        Repo.clone_from(repo_url, clone_dir)
        print(f"✅ Repo cloned to: {clone_dir}")
        return clone_dir

    except GitCommandError as e:
        print(f"❌ Git error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
    
# Function to load files and it's content from the clone repositry

def load_repo_files(clone_dir):
    supported_extensions = ['.py','.md','.js','.ts','.html','.txt']
    files_data = []

    for root,_,files in os.walk(clone_dir):
        for file in files:
            if any(file.endswith(ext) for ext in supported_extensions):
                file_path = os.path.join(root,file)
                try:
                    with open(file_path,'r',encoding = "utf-8", errors='ignore') as f:
                        content = f.read()
                        files_data.append({
                            "path":file_path,
                            "content":content
                        })
                except Exception as e:
                    print(f"[!] Failed to read file:{file_path} — {str(e)} ")
    return files_data