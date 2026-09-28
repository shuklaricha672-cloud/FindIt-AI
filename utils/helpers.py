import os
import uuid


def save_uploaded_file(uploaded_file, folder):

    os.makedirs(folder, exist_ok=True)

    extension = uploaded_file.name.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    file_path = os.path.join(
        folder,
        filename
    )

    with open(file_path, "wb") as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return file_path