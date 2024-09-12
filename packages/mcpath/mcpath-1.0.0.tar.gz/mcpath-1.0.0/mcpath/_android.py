"""Android paths"""

import os

__all__ = ["java", "bedrock", "preview", "education"]

from mcpath import BEPath


class AndroidBEPath(BEPath):
    platform = "android"

    @property
    def root(self) -> str:
        return os.path.join(
            "data", "user", "0", "com.mojang.minecraftpe", "games", "com.mojang"
        )


java = None
bedrock = AndroidBEPath()
preview = None
education = None
