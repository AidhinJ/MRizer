import customtkinter as tk
import re
import requests
import threading
import time
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import ApiRequestError

# --- Improved Google Drive Handling ---
class DriveConnector:
    """A class to handle a single, persistent connection to Google Drive."""
    def __init__(self):
        self.drive = None

    def authenticate(self):
        """Authenticate and create the drive object if it doesn't exist."""
        if self.drive is None:
            try:
                gauth = GoogleAuth()
                gauth.LocalWebserverAuth()  # Authenticate only once
                self.drive = GoogleDrive(gauth)
                return True
            except Exception as e:
                # Update the GUI with the authentication error
                results_textbox.insert("end", f"🚨 Google Drive Authentication Failed: {e}\n")
                return False
        return True

# Create a single instance of the DriveConnector
drive_connector = DriveConnector()

# --- Checking Functions (Refactored for Safety) ---

def check_on_website(mr_number):
    """Checks for a floorplan, now with error handling."""
    try:
        # Added a timeout to prevent indefinite waiting
        response = requests.get(f"https://www.myroof.co.za/{mr_number}", timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (like 404)
        return "Floor Plans" in response.text
    except requests.exceptions.RequestException as e:
        print(f"Website check failed for {mr_number}: {e}")
        return False

def check_on_google_drive(mr_number):
    """
    Checks Google Drive with a retry mechanism for handling API server errors.
    """
    if not drive_connector.drive:
        return {'found': False, 'reason': 'Google Drive not authenticated.'}

    query = f"title contains '{mr_number}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    
    # --- NEW: Retry Logic ---
    file_list = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # This is the line that was failing
            file_list = drive_connector.drive.ListFile({'q': query}).GetList()
            # If the line above succeeds, we break out of the retry loop
            break
        except ApiRequestError as e:
            # Check if the error is a 5xx server error
            if '50' in str(e): # Catches 500, 502, 503, etc.
                print(f"Google Drive API server error for {mr_number}. Retrying ({attempt + 1}/{max_retries})...")
                time.sleep(attempt + 1) # Wait 1s, then 2s, etc. (exponential backoff)
            else:
                # If it's another API error (like a 4xx permissions error), don't retry.
                return {'found': False, 'reason': f"API Error: {e}"}
        except Exception as e:
            # Catch any other unexpected errors
            return {'found': False, 'reason': f"An unexpected error occurred: {e}"}

    # If the loop finished without success after all retries
    if file_list is None:
        return {'found': False, 'reason': 'Google Drive API failed after multiple retries.'}
    # --- END: Retry Logic ---


    if not file_list:
        return {'found': False, 'reason': f"No folder containing '{mr_number}' found."}

    # Search for the specific BANK or PVT folder
    for folder in file_list:
        if "BANK" in folder['title'].upper() or "PVT" in folder['title'].upper():
            target_folder_id = folder['id']
            folder_contents = drive_connector.drive.ListFile({'q': f"'{target_folder_id}' in parents and trashed=false"}).GetList()
            owner = folder['ownerNames'][0] if 'ownerNames' in folder and folder['ownerNames'] else 'Unknown Owner'
            
            return {
                'found': True,
                'owner': owner,
                'item_count': len(folder_contents)
            }
            
    # If loop finishes without finding a BANK/PVT folder
    last_folder_owner = file_list[0]['ownerNames'][0] if 'ownerNames' in file_list[0] and file_list[0]['ownerNames'] else 'Unknown Owner'
    return {'found': False, 'reason': f"Folder found, but not a BANK/PVT type. (Owner: {last_folder_owner})"}

def check_on_cloudpano(mr_number):
    """Simulates checking Cloudpano status."""
    import random
    return "In process" if random.choice([True, False]) else "Not in process"

# --- Main Logic Function (Modified to run checks) ---

def run_checks():
    """The core logic that performs all checks. Meant to be run in a separate thread."""
    # Authenticate with Google Drive before starting
    if not drive_connector.authenticate():
        results_textbox.insert("end", "\n--- Check Aborted ---")
        get_button.configure(state="normal", text="Check 360 Availability") # Re-enable button
        return

    content = textbox.get("1.0", "end-1c")
    found_mrs = re.findall(r'\bMR\d+\b', content)
    unique_mr_numbers = sorted(list(set(found_mrs)))

    if not unique_mr_numbers:
        results_textbox.insert("end", "No MR numbers (e.g., MR123456) found in the input text.\n")
        results_textbox.insert("end", "\n--- Check Complete ---")
        get_button.configure(state="normal", text="Check 360 Availability") # Re-enable button
        return

    results_textbox.insert("end", f"Found {len(unique_mr_numbers)} unique MR numbers to check.\n\n")

    for mr in unique_mr_numbers:
        results_textbox.insert("end", f"Checking MR: {mr}\n")

        # 1. Check on Website
        if check_on_website(mr):
            results_textbox.insert("end", f"  ✅ {mr} - Floorplan found on website.\n")
            
            # 2. Check on Google Drive
            drive_result = check_on_google_drive(mr)
            if drive_result['found']:
                results_textbox.insert("end", f"  ✅ {mr} - Available on Google Drive.\n")
                
                # 3. Check on Cloudpano
                status = check_on_cloudpano(mr)
                results_textbox.insert("end", f"  ℹ️ {mr} - Cloudpano status: {status}.\n")

                item_count = drive_result['item_count']
                owner = drive_result['owner']
                
                if item_count > 0:
                    results_textbox.insert("end", f"  ✨ {mr} - Is available for 360 processing! ({item_count} items found)\n\n")
                else:
                    results_textbox.insert("end", f"  ⚠️ {mr} - Folder is EMPTY. {owner} must re-upload.\n\n")
            else:
                results_textbox.insert("end", f"  ❌ {mr} - Not on Google Drive. {drive_result.get('reason', 'Requires upload.')}\n\n")
        else:
            results_textbox.insert("end", f"  ❌ {mr} - Floorplan NOT found on website. Cannot proceed.\n\n")

    results_textbox.insert("end", "--- Check Complete ---")
    get_button.configure(state="normal", text="Check 360 Availability") # Re-enable button when done

def start_checks_thread():
    """Starts the 'run_checks' function in a new thread to keep the GUI responsive."""
    # Clear previous results and disable button before starting
    results_textbox.delete("1.0", "end")
    results_textbox.insert("end", "--- Starting 360 Availability Check ---\n")
    results_textbox.insert("end", "--------------------------------------\n\n")
    
    get_button.configure(state="disabled", text="Checking...") # Disable button
    
    # Create and start the thread
    check_thread = threading.Thread(target=run_checks)
    check_thread.daemon = True  # Allows main window to exit even if thread is running
    check_thread.start()


# --- GUI Setup ---
window = tk.CTk()
window.geometry("650x700")
window.title("360 Availability Checker")
window.resizable(False, False)

label = tk.CTkLabel(master=window, text="Paste the Reports QA page content (or any text with MR numbers):", font=("Arial", 14))
label.pack(pady=10)

textbox = tk.CTkTextbox(master=window, height=180, width=600, wrap="word", font=("Arial", 15))
textbox.pack(pady=5)
textbox.insert("1.0", "Here are some reports: MR12345, MR98765. Another one is MR112233.\nSome text without MRs. MR45678 is good. Also MR007.")

# Button now calls the thread starter function
get_button = tk.CTkButton(master=window, text="Check 360 Availability", command=start_checks_thread, font=("Arial", 14, "bold"), height=40)
get_button.pack(pady=15)

results_label = tk.CTkLabel(master=window, text="Results:", font=("Arial", 14))
results_label.pack(pady=5)

results_textbox = tk.CTkTextbox(master=window, height=250, width=600, wrap="word", font=("Consolas", 15), state="normal")
results_textbox.pack(pady=5)

window.mainloop()
