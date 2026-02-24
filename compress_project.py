import os
import zipfile

def create_distribution_zip():
    source_dir = "."
    output_filename = "AI_Guitar_Pedal_Project_Dist.zip"
    
    # Things to completely ignore to keep the zip file lean
    ignore_dirs = {"node_modules", "__pycache__", ".git"}
    ignore_files = {output_filename, "ai_guitar_pedal.db"} # We shouldn't export standard local DB file

    print(f"📦 Starting compression of the AI Guitar Pedal ecosystem into '{output_filename}'...")

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Mutate dirs in-place to prevent os.walk from entering ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if file in ignore_files or file.endswith('.zip') or file.endswith('.pyc'):
                    continue
                    
                filepath = os.path.join(root, file)
                # Calculate the relative path so the zip structure remains clean
                arcname = os.path.relpath(filepath, start=source_dir)
                zipf.write(filepath, arcname)
                
    zip_size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"✅ Success! Generated lean distribution file: '{output_filename}' ({zip_size_mb:.2f} MB)")
    print("This file can now be moved or shared to any other computer to continue work!")

if __name__ == "__main__":
    create_distribution_zip()
