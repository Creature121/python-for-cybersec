from libratom.lib.pff import PffArchive

file_name = "..\sample.pst"
archive = PffArchive(file_name)

stack_of_folders = [(folder, 0) for folder in list(archive.folders())[::-1]]
while stack_of_folders:
    folder, level = stack_of_folders.pop()
    spacing = "\t" * level

    print(f"{spacing}{folder.name}")
    if m_count := folder.get_number_of_sub_messages() != 0:
        for message, count in zip(folder.sub_messages, range(1, m_count + 1)):
            print(f"{spacing} Message {count}:")
            print(f"{spacing}   -> Sender: {message.get_sender_name()}")
            print(f"{spacing}   -> Subject: {message.get_subject()}")
            print(f"{spacing}   -> Message: {message.get_plain_text_body()}")

    stack_of_folders.extend(
        [(sub_folder, level + 1) for sub_folder in folder.sub_folders]
    )
