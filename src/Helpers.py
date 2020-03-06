import hashlib
import logging
import os
import re
import subprocess
import xml.etree.ElementTree as ElementTree
from pathlib import Path
from platform import system
from zipfile import ZipFile, ZipInfo, BadZipFile
from sqlalchemy.exc import DatabaseError


import wx


class FileHelpers:

    @staticmethod
    def get_sku(path: Path):
        sku = 0

        if path.suffix != '.zip':
            logging.error('Path provided does not point to a zip file, returning 0')
            return sku

        with ZipFile(path, 'r') as zfile:
            info: ZipInfo
            for info in zfile.infolist():
                file_name = FileHelpers.clean_path(info.filename)
                if file_name[:23] == 'Runtime/Support/DAZ_3D_' and info.filename[-4:] == '.dsx':
                    return int(file_name[23:][:5])

        file_name = path.name
        if file_name[:2] == 'IM' and file_name[10] == '-' and file_name[13] == '_':
            file_name = file_name[:10]
            sku = int(file_name[2:])

        return sku

    @staticmethod
    def get_img_preview(zip_path: Path):
        logging.debug(f'Finding asset image for: {zip_path.name}')
        with ZipFile(zip_path, 'r') as zfile:
            root = 'Runtime/Support/'
            results = [i for i in zfile.namelist() if root in i and i[-4:] in ['.png', '.jpg']]
            local_path = Path(results[0]) if len(results) > 0 else None

            if local_path is not None:
                images_folder_path = FolderHelpers.get_user_folder() / 'images'
                if not images_folder_path.exists(): images_folder_path.mkdir()

                img_path = images_folder_path / local_path.name
                with open(img_path, 'wb') as out:
                    out.write(zfile.read(results[0]))

                return img_path.name
            else:
                return 'DNE'

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
    def parse_product_name(path: Path):
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
        if size > 2 ** 30:
            size /= 2 ** 30
            ext = ' GB'
        else:
            size /= 2 ** 20
            ext = ' MB'

        size = round(size, places)

        return str(size) + ext

    @staticmethod
    def get_file_size(path: Path):
        return os.path.getsize(str(path))

    @staticmethod
    def clean_path(path: str):
        if path[:8] == 'Content/':
            path = path[8:]
        elif path[:11] == 'My Library/':
            path = path[11:]
        elif path[:19] == 'My DAZ 3D Library/':
            path = path[19:]
        return path

    @staticmethod
    def open_location(path: Path):
        subprocess.Popen(r'explorer /select, ' + str(path))

    @staticmethod
    def delete_file(path: Path):
        path.unlink()


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

    @staticmethod
    def get_user_folder(subfolder=''):
        if system() == 'Windows':
            return Path(os.getenv('APPDATA') + '/ADI/' + subfolder)
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

    @staticmethod
    def delete_empty_dirs(path):
        for root, dir_names, file_names in os.walk(path, topdown=False):
            for dir_name in dir_names:
                path = os.path.join(root, dir_name)

                if len(os.listdir(path)) == 0:
                    FolderHelpers.delete_dir(path)

    @staticmethod
    def delete_dir(path):
        try:
            os.rmdir(path)
        except OSError as e:
            logging.error(e)

    @staticmethod
    def open_location(path: Path):
        subprocess.Popen(r'explorer ' + str(path))


class WXHelpers:

    @staticmethod
    def create_menu_option(self, parent_menu, label, method, *passed_args):
        menu_item = parent_menu.Append(-1, label)
        wrapper = lambda event: method(*passed_args)
        self.Bind(wx.EVT_MENU, wrapper, menu_item)


class SQLHelpers:

    @staticmethod
    def commit(session, row=None):
        try:
            if row is not None:
                session.add(row)
            session.commit()
        except DatabaseError as e:
            logging.critical(e)
            session.rollback()
        finally:
            session.close()