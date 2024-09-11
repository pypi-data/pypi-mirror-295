

# def shVersion():
#     code = {"a": "alpha", "b": "beta", "rc": "ReleaseCandidate", "f": "Final"}
#     nVer = f"{VERSION[0]}.{VERSION[1]}"
#     if VERSION[2] != 0:
#         nVer += f".{VERSION[2]}"
#     if VERSION[3].lower() != "f":
#         nVer += f".{code[VERSION[3].lower()]}"
#         if VERSION[4] != 0:
#             nVer += f".{VERSION[4]}"
#     return nVer


code = {"d": "devel", "a": "alpha", "b": "beta",
        "rc": "ReleaseCandidate", "f": "Final"}

numeric_map = {"d": 1, "a": 2, "b": 3, "rc": 4, "f": 5}


class Vers:
    """
    Class for the manipulation of objects version following the Semantic Versioning
    
    major.minor.patch-<prerel>.<build>
    
    Is implemented a special dialect.
    
    
    
    The admitted pre-release values are
    
        * d  for the developing version 
        * a  for the alpha version 
        * b  for the beta version
        * rc for the release candidate
        * f  for the final version
    """
    def __init__(self, ver: tuple| str)->None:
        if isinstance(ver, str):
            ver = tuple(map(int, ver.split('.')))
            
        self.major, self.minor, self.patch, *extra = ver
        # self.patch = extra[0] if extra else None
        self.type = extra[0] if len(extra)!=0 else None
        if self.type is not None:
            if not isinstance(self.type,str):
                raise Exception(
                    f"The fourth element of the version number must be a string")
            if not self.type in code.keys():
                raise ValueError(f"the fourth element of the version mus be one of {','.join(code.keys())}")
        self.build = extra[1] if len(extra) > 1 else None


    def full(self)->str:
        """
        Return the full version

        Returns:
            str: the version string
        """
        if self.type is None:
            nVer = f"{self.major}.{self.minor}.{self.patch}"
        elif self.type.lower() == 'f':
            nVer = f"{self.major}.{self.minor}.{self.patch}"
        else:
            nVer = f"{self.major}.{self.minor}.{self.patch}-{code[self.type]}.{self.build}"
        return nVer

    def short(self)->str:
        """
        Return the version in the form major.minor.patch

        Returns:
            str: the version string
        """
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self) -> str:
        return f"Version {self.full()}"

    def __eq__(self, other)->bool:
        if self.major == other.major and self.minor == other.minor and self.patch == other.patch:
            if self.type is None:
                return True
            else:
                if self.type == other.type and self.build == other.build:
                    return True
                else:
                    return False
        else:
            return False
        # return all(getattr(self, item) == getattr(other, item) for item in self.__dict__ if not item.startswith('_'))
    
    def __gt__(self, other) -> bool:
        if self.major != other.major:
            return self.major > other.major
        elif self.minor != other.minor:
            return self.minor > other.minor
        elif self.patch != other.path:
            return self.path > other.path
        elif numeric_map[self.type] != numeric_map[other.type]:
            return numeric_map[self.type] > numeric_map[other.type]
        else:
            return self.build > other.build
        
    def __ge__(self,other)->bool:
        if self > other or self == other:
            return True
        else:
            return False
        
    def __lt__(self,other)->bool:
        if self.major != other.major:
            return self.major < other.major
        elif self.minor != other.minor:
            return self.minor < other.minor
        elif self.patch != other.patch:
            return self.patch < other.patch
        elif numeric_map[self.type] != numeric_map[other.type]:
            return numeric_map[self.type] < numeric_map[other.type]
        else:
            return self.build < other.build

    def __le__(self, other) -> bool:
        if self < other or self == other:
            return True
        else:
            return False


# version = Vers(VERSION)
