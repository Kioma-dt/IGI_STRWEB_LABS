import zipfile
import re

class FileService:
    @staticmethod
    def read(filename):
        if not re.search(r"\.txt$", filename):
            filename += '.txt'
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return file.read()
        except IOError as ex:
            raise IOError(f"Read File Error: {ex}")
            
    @staticmethod
    def write(filename, result):
        if not re.search(r"\.txt$", filename):
            filename += '.txt'
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(result)
        except IOError as ex:
            raise IOError(f"Write to File Error: {ex}")

    @staticmethod
    def zip_file(zipname, filename):
        if not re.search(r"\.zip$", zipname):
            zipname += '.zip'
        if not re.search(r"\.txt$", filename):
            filename += '.txt'
        try:
            with zipfile.ZipFile(zipname, 'w') as myzip:
                myzip.write(filename)
        except IOError as ex:
            raise IOError(f"Zipping File Error: {ex}")
        
    @staticmethod
    def zipped_file_info(zipname, filename):
        if not re.search(r"\.zip$", zipname):
            zipname += '.zip'
        if not re.search(r"\.txt$", filename):
            filename += '.txt'

        try:
            with zipfile.ZipFile(zipname, 'r') as myzip:
                # for item in myzip.infolist():
                item = myzip.getinfo(filename)
                return f"File Name: {item.filename}, Date: {item.date_time}, Size: {item.file_size}"
        except IOError as ex:
            raise IOError(f"Zipping File Error: {ex}")

