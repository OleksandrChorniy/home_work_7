from pathlib import Path
import shutil
import sys
import clean_folder.file_parser as parser
from clean_folder.normalize import normalize


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_document(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(
        filename.name.replace(filename.suffix, "")
    )
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)
    except shutil.ReadError:
        print("NOT archive")
        folder_for_file.rmdir()
    filename.unlink()


def handel_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete {folder}")


def main(folder: Path):
    parser.scan(folder)
    for file in parser.JPEG_IMG:
        handle_media(file, folder / "images" / "JPEG")
    for file in parser.JPG_IMG:
        handle_media(file, folder / "images" / "JPG")
    for file in parser.PNG_IMG:
        handle_media(file, folder / "images" / "PNG")
    for file in parser.SVG_IMG:
        handle_media(file, folder / "images" / "SVG")
    for file in parser.MP3_AUDIO:
        handle_media(file, folder / "audio" / "MP3")
    for file in parser.AVI_VIDEO:
        handle_media(file, folder / "video" / "AVI")
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / "video" / "MOV")
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / "video" / "MP4")

    for file in parser.TXT_DOCUMENTS:
        handle_document(file, folder / "documents" / "TXT")
    for file in parser.XLSX_DOCUMENTS:
        handle_document(file, folder / "documents" / "XLSX")
    for file in parser.DOC_DOCUMENTS:
        handle_document(file, folder / "documents" / "DOC")

    for file in parser.MY_OTHER:
        handle_other(file, folder / "MY_OTHER")
    for file in parser.ARCHIVES:
        handle_archive(file, folder / "ARCHIVES")

    for folder in parser.FOLDERS[::-1]:
        handel_folder(folder)


def run():
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        main(folder_for_scan.resolve())


if __name__ == "__main__":
    run()
