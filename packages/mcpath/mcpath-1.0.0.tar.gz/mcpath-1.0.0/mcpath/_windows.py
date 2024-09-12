"""Windows (win32) paths"""

import os

__all__ = ["java", "bedrock", "preview", "education"]

from mcpath import JEPath, BEPath, PREPath, EDUPath


class WindowsJEPath(JEPath):
    platform = "win32"

    @property
    def root(self) -> str:
        return os.path.expandvars("%appdata%\\.minecraft")


class WindowsBEPath(BEPath):
    platform = "win32"

    @property
    def root(self) -> str:
        return os.path.expandvars(
            "%localappdata%\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )


class WindowsPREPath(PREPath):
    platform = "win32"

    @property
    def root(self) -> str:
        return os.path.expandvars(
            "%localappdata%\\Packages\\Microsoft.MinecraftWindowsBeta_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )


class WindowsEDUPath(EDUPath):
    platform = "win32"

    @property
    def root(self) -> str:
        return os.path.expandvars(
            "%localappdata%\\Packages\\Microsoft.MinecraftEducationEdition_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )


java = WindowsJEPath()
bedrock = WindowsBEPath()
preview = WindowsPREPath()
education = WindowsEDUPath()
