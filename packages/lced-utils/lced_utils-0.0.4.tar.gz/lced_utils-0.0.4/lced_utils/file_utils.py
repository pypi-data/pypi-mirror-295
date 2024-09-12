import os

from lced_utils.buffer_utils import get_project_root_path


def create_required_directories(directories):
    """
    检查并创建必需的目录
    :param directories: 必需的目录列表
    """
    for directory in directories:
        directory_full_path = os.path.join(get_project_root_path(), directory)
        if not os.path.exists(directory_full_path):
            try:
                os.makedirs(directory)
            except OSError as e:
                pass


def get_file_extensions(directory):
    """
    获取目录中所有文件的扩展名
    :param directory: 目录路径
    :return: 文件扩展名的集合
    """
    extensions = set()
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            _, ext = os.path.splitext(filename)
            if ext:
                extensions.add(ext)
    return extensions


if __name__ == "__main__":
    create_required_directories(["logs"])
