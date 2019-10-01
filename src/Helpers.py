import os
import re
import hashlib
import logging
import xml.etree.ElementTree as ElementTree
from pathlib import Path
from zipfile import ZipFile, BadZipFile
from platform import system


class FileHelpers:

    @staticmethod
    def get_sku(path: Path):
        # todo look at files in Runtime/Support for SKU
        if path.suffix != '.zip':
            logging.error('Path provided does not point to a zip file, returning 0')
            return 0

        sku = 0

        file_name = path.name
        if file_name[:2] == 'IM' and file_name[10] == '-' and file_name[13] == '_':
            file_name = file_name[:10]
            sku = int(file_name[2:])

        return sku

    @staticmethod
    def get_zip_hash(path: Path):

        if path.suffix != '.zip':
            logging.error('Path provided does not point to a zip file, returning \'null hash\'')
            return 'null hash'

        zip_hash = hashlib.md5()

        logging.debug('Hashing: ' + path.name)
        with open(str(path), "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):  # Read and update hash string value in blocks of 4K
                zip_hash.update(byte_block)

        return zip_hash.hexdigest()

    @staticmethod
    def get_product_name(path: Path):
        product_name = path.stem

        try:
            zf = ZipFile(path, 'r')
        except BadZipFile as e:
            logging.error('Error occurred while opening zip file: ' + str(path.name))
            logging.error(e)
            return product_name + " is an invalid zip"

        if 'Supplement.dsx' in zf.namelist():
            zf = ZipFile(path, 'r')
            zf.extract("Supplement.dsx", path='.')

            supplement_xml = ElementTree.parse("Supplement.dsx").getroot()
            product_name = supplement_xml.find('ProductName').get('VALUE')

            os.remove("Supplement.dsx")

        elif product_name[:2] == 'IM' and product_name[10] == '-' and product_name[13] == '_':
            temp = product_name[14:]
            temp = re.findall(r'[\dA-Z]+(?=[A-Z])|[\dA-Z][^\dA-Z]+', temp)
            product_name = ' '.join(temp)

        elif '-' in product_name:
            product_name = product_name.replace('-', ' ')

        elif '_' in product_name:
            product_name = product_name.replace('_', ' ')

        elif product_name.islower():
            pass

        elif ' ' in product_name:
            pass

        else:
            temp = re.findall(r'[\dA-Z]+(?=[A-Z])|[\dA-Z][^\dA-Z]+', product_name)
            product_name = ' '.join(temp)

        zf.close()

        return product_name

    @staticmethod
    def format_bytes(size, places=2):

        rnd = places * 10

        if size > 2 ** 30:
            size /= 2 ** 30
            ext = ' GB'
        else:
            size /= 2 ** 20
            ext = ' MB'

        return str(int(size * rnd) / rnd) + ext

    @staticmethod
    def get_file_size(path: Path):
        return os.path.getsize(str(path))


class FolderHelpers:

    @staticmethod
    def get_folder_size(path: Path):

        if not path.is_dir():
            logging.warning('Path provided does not point to a directory, returning 0')
            return 0

        total_size = 0
        path = str(path)

        for dir_path, dir_names, file_names in os.walk(path):
            for f in file_names:
                fp = os.path.join(dir_path, f)

                if not os.path.islink(fp):  # skip if it is symbolic link
                    total_size += os.path.getsize(fp)

        return total_size

    @staticmethod
    def get_zip_count(path: Path):
        count = 0
        path = str(path)

        for dir_path, dir_names, file_names in os.walk(path):
            for f in file_names:
                if f[-4:] == '.zip':
                    count += 1

        return count

    # todo make these better?
    @staticmethod
    def get_user_folder():
        if system() == 'Windows':
            return Path(os.getenv('APPDATA') + '/ADI/')
        elif system() == 'Darwin':  # mac
            return Path(os.path.expanduser('~/Library/Application Support/ADI/'))
        else:  # linux
            return Path(os.path.expanduser('~/.ADI/'))

    @staticmethod
    def get_default_library_path():
        if system() == 'Windows':
            return Path('C:/Users/Public/Documents/My DAZ 3D Library/')
        elif system() == 'Darwin':  # mac
            return Path(os.path.expanduser('~/Studio3D/DazStudio/Content/'))
        else:  # linux
            return Path(os.path.expanduser('~/Daz3D Library/'))

    @staticmethod
    def get_default_archive_path():
        if system() == 'Windows':
            return Path('C:/Users/Public/Documents/DAZ 3D/InstallManager/Downloads')
        elif system() == 'Darwin':  # mac
            return Path(os.path.expanduser('~/Studio3D/DazStudio/InstallManager/Download/'))
        else:  # linux
            return Path(os.path.expanduser('~/Daz3D Zips/'))
