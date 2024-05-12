import imaplib
import mailbox

def list_folders_and_upload(mbox_file, email, password, imap_server, imap_port):
    mbox = mailbox.mbox(mbox_file)

    imap_connection = imaplib.IMAP4_SSL(imap_server)
    imap_connection.login(email, password)

    status, folders = imap_connection.list()

    if status == 'OK':
        print("Folders:")
        for idx, folder in enumerate(folders, start=1):
            print(f"{idx}. {folder.decode('utf-8')}")

        # Prompt the user to select a folder
        folder_index = int(input("Enter the index of the folder you want to upload emails to: ")) - 1
        selected_folder = folders[folder_index].split()[-1].decode('utf-8').strip('"')

        # Select the destination folder on the server
        imap_connection.select(selected_folder)

        for message in mbox:
            # Convert the email message to string and upload it to the server
            email_message = message.as_string().encode('utf-8')
            imap_connection.append(selected_folder, None, None, email_message)

        # Close the connections
        mbox.close()
        imap_connection.close()
        imap_connection.logout()

# Example usage:
mbox_file = 'INBOX_emails.mbox'
email = 'test@maharramhuseynov.com'
password = '123456'
imap_server = 'mail.maharramhuseynov.com'
imap_port = 587

list_folders_and_upload(mbox_file, email, password, imap_server, imap_port)
