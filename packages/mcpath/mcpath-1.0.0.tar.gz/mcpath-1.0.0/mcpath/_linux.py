"""Linux paths"""

import os

__all__ = ["java", "bedrock", "preview", "education"]

from mcpath import JEPath


class LinuxJEPath(JEPath):
    platform = "linux"

    @property
    def root(self) -> str:
        return os.path.join(os.path.expanduser("~"), ".minecraft")


java = LinuxJEPath()
bedrock = None
preview = None
education = None
