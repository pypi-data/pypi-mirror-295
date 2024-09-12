"""Darwin (MacOS) paths"""

import os

__all__ = ["java", "bedrock", "preview", "education"]

from mcpath import JEPath


class DarwinJEPath(JEPath):
    platform = "darwin"

    @property
    def root(self) -> str:
        return os.path.join(
            os.path.expanduser("~"), "Library", "Application Support", "minecraft"
        )


java = DarwinJEPath()
bedrock = None
preview = None
education = None
