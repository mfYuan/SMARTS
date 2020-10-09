import hashlib
import os
import shutil
import dataclasses

# https://stackoverflow.com/a/2166841
def isnamedtupleinstance(x):
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, "_fields", None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)


def isdataclass(x):
    return dataclasses.is_dataclass(x)


def unpack(obj):
    """A helper that can be used to print `nestedtuples`. For example,
    ```python
    pprint(unpack(obs), indent=1, width=80, compact=True)
    ```
    """
    if isinstance(obj, dict):
        return {key: unpack(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [unpack(value) for value in obj]
    elif isnamedtupleinstance(obj):
        return {key: unpack(value) for key, value in obj._asdict().items()}
    elif isdataclass(obj):
        return dataclasses.asdict(obj)
    elif isinstance(obj, tuple):
        return tuple(unpack(value) for value in obj)
    else:
        return obj


def copy_tree(from_path, to_path, overwrite=False):
    if os.path.exists(to_path):
        if overwrite:
            shutil.rmtree(to_path)
        else:
            raise FileExistsError(
                "The destination path={} already exists.".format(to_path)
            )

    shutil.copytree(from_path, to_path)


def path2hash(file_path: str):
    m = hashlib.md5()
    m.update(bytes(file_path, "utf-8"))
    return m.hexdigest()