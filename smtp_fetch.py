#SMTP mail fetcher v_01

import imaplib
import mailbox

email = 'info@vulcantravels.com'
password = 'resInfo!3'
imap_server = 'mail.vulcantravels.com'
imap_port = 993

imap_connection = imaplib.IMAP4_SSL(imap_server, imap_port)

imap_connection.login(email, password)

status, folders = imap_connection.list()

if status == 'OK':
    print("Folders:")
    for idx, folder in enumerate(folders, start=1):
        print(f"{idx}. {folder.decode('utf-8')}")

    # Prompt the user to select a folder
    folder_index = int(input("Enter the index of the folder you want to fetch from: ")) - 1
    selected_folder = folders[folder_index].split()[-1].decode('utf-8').strip('"')

    imap_connection.select(selected_folder)

    status, email_ids = imap_connection.search(None, 'ALL')

    if status == 'OK':
        num_emails = len(email_ids[0].split())
        print(f"Found {num_emails} emails in the '{selected_folder}' folder.")

        mbox_file = f"{selected_folder.replace(' ', '_')}_emails.mbox"
        mbox = mailbox.mbox(mbox_file)

        for idx, email_id in enumerate(email_ids[0].split(), start=1):
            status, email_data = imap_connection.fetch(email_id, '(RFC822)')
            if status == 'OK':
                mbox.add(email_data[0][1])
                print(f"Processed email {idx}/{num_emails}")

        mbox.close()
        print(f"All emails from the '{selected_folder}' folder have been saved to {mbox_file}.")

imap_connection.logout()
