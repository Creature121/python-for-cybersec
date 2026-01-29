from libratom.lib.pff import PffArchive

file_name = "sample.pst"
archive = PffArchive(file_name)

for folder in archive.folders():
    if folder.get_number_of_sub_messages() != 0:
        for message in folder.sub_messages:
            print(f"Sender: {message.get_sender_name()}")
            print(f"Subject: {message.get_subject()}")
            print(f"Message: {message.get_plain_text_body()}")
