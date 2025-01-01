'''
Title: sam_dropbox.py
Author: Samuel J. Huskey (with assistance from Chat GPT 4o)

Purpose: Helper functions for working in Colab, to upload large files to Dropbox

Note: Needs an access token from the Dropbox App Console
'''

import dropbox
import os

# Initialize Dropbox client
dbx = dropbox.Dropbox('') # Insert access token from Dropbox App Console here

# Check if the authentication works
dbx.users_get_current_account()


# Function to download a file from Dropbox and save it locally in Colab
def download_from_dropbox(dropbox_file_path, local_file_path):
    with open(local_file_path, "wb") as f:
        metadata, res = dbx.files_download(path=dropbox_file_path)
        f.write(res.content)

# Function to handle chunked upload for large files
def upload_large_file_to_dropbox(local_file_path, dropbox_file_path, chunk_size=4 * 1024 * 1024):
    """Uploads large files in chunks to Dropbox (supports files larger than 150 MB)."""
    file_size = os.path.getsize(local_file_path)
    with open(local_file_path, 'rb') as f:
        if file_size <= chunk_size:
            print(f"Uploading {local_file_path} directly (size: {file_size} bytes)")
            dbx.files_upload(f.read(), dropbox_file_path)
        else:
            print(f"Uploading {local_file_path} in chunks (size: {file_size} bytes)")
            upload_session_start_result = dbx.files_upload_session_start(f.read(chunk_size))
            cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                       offset=f.tell())
            commit = dropbox.files.CommitInfo(path=dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)

            # Upload chunks
            while f.tell() < file_size:
                if ((file_size - f.tell()) <= chunk_size):
                    print("Finishing upload...")
                    dbx.files_upload_session_finish(f.read(chunk_size), cursor, commit)
                else:
                    dbx.files_upload_session_append_v2(f.read(chunk_size), cursor)
                    cursor.offset = f.tell()

# Function to upload all files in a directory (handles large files)
def upload_directory_to_dropbox(local_dir_path, dropbox_dir_path):
    """Uploads all files in a local directory to Dropbox, handling large files with chunked upload."""
    for root, dirs, files in os.walk(local_dir_path):
        for filename in files:
            local_file_path = os.path.join(root, filename)
            dropbox_file_path = os.path.join(dropbox_dir_path, filename).replace('\\', '/')
            file_size = os.path.getsize(local_file_path)

            # Upload file using chunked upload if it exceeds 150 MB, otherwise use standard upload
            if file_size > 150 * 1024 * 1024:  # 150 MB limit for Dropbox API
                print(f"File {local_file_path} exceeds 150 MB, using chunked upload.")
                upload_large_file_to_dropbox(local_file_path, dropbox_file_path)
            else:
                print(f"File {local_file_path} is smaller than 150 MB, using standard upload.")
                with open(local_file_path, "rb") as f:
                    dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)

def save_model_to_dropbox(model, output_dir, dropbox_dir):
    # Save the model locally first
    model.save_pretrained(output_dir)

    # Loop over files saved in the directory and upload them to Dropbox
    for root, dirs, files in os.walk(output_dir):
        for filename in files:
            local_path = os.path.join(root, filename)
            dropbox_path = os.path.join(dropbox_dir, filename).replace('\\', '/')
            upload_to_dropbox(local_path, dropbox_path)

def upload_logs_to_dropbox(log_file_path, dropbox_log_dir):
    upload_to_dropbox(log_file_path, dropbox_log_dir)