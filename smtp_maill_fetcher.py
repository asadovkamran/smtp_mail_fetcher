import imaplib
import mailbox

# Set your email credentials and server information
email = 'email@example.com'
password = 'password'
imap_server = 'imap.example.com'
imap_port = 993

# Connect to the IMAP server
imap_connection = imaplib.IMAP4_SSL(imap_server, imap_port)

# Login to your email account
imap_connection.login(email, password)

# List all available folders
status, folders = imap_connection.list()

if status == 'OK':
    print("Folders:")
    for idx, folder in enumerate(folders, start=1):
        print(f"{idx}. {folder.decode('utf-8')}")

    # Prompt the user to select a folder
    folder_index = int(input("Enter the index of the folder you want to fetch from: ")) - 1
    selected_folder = folders[folder_index].split()[-1].decode('utf-8').strip('"')

    # Select the chosen folder
    imap_connection.select(selected_folder)

    # Search for all emails in the selected folder
    status, email_ids = imap_connection.search(None, 'ALL')

    if status == 'OK':
        # Print the number of emails found
        num_emails = len(email_ids[0].split())
        print(f"Found {num_emails} emails in the '{selected_folder}' folder.")

        # Create a new mbox file for the selected folder
        mbox_file = f"{selected_folder.replace(' ', '_')}_emails.mbox"
        mbox = mailbox.mbox(mbox_file)

        # Fetch and save each email in mbox format
        for idx, email_id in enumerate(email_ids[0].split(), start=1):
            status, email_data = imap_connection.fetch(email_id, '(RFC822)')
            if status == 'OK':
                mbox.add(email_data[0][1])
                print(f"Processed email {idx}/{num_emails}")

        # Close the mbox file
        mbox.close()
        print(f"All emails from the '{selected_folder}' folder have been saved to {mbox_file}.")

# Logout from the server
imap_connection.logout()
