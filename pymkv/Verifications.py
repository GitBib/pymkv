# sheldon woodward
# 3/24/18

"""Verification functions for mkvmerge and associated files."""

import json
import os
from os.path import expanduser, isfile
from re import match
import subprocess as sp


def verify_mkvmerge(mkvmerge_path='mkvmerge'):
    """Verify mkvmerge is working.

    mkvmerge_path (str):
        Alternate path to mkvmerge if it is not already in the $PATH variable.
    """
    try:
        output = sp.check_output([mkvmerge_path, '-V']).decode()
    except (sp.CalledProcessError, FileNotFoundError):
        return False
    return bool(match('mkvmerge.*', output))


def verify_matroska(file_path, mkvmerge_path='mkvmerge'):
    """Verify if a file is a Matroska file.

    file_path (str):
        Path of the file to be verified.
    mkvmerge_path (str):
        Alternate path to mkvmerge if it is not already in the $PATH variable.
    """
    if not verify_mkvmerge(mkvmerge_path=mkvmerge_path):
        raise FileNotFoundError('mkvmerge is not at the specified path, add it there or change the mkvmerge_path '
                                'property')

    if isinstance(file_path, os.PathLike):
        file_path = str(file_path)
    elif not isinstance(file_path, str):
        raise TypeError(f'"{file_path}" is not of type str')
    file_path = expanduser(file_path)
    if not isfile(file_path):
        raise FileNotFoundError(f'"{file_path}" does not exist')
    try:
        info_json = json.loads(sp.check_output([mkvmerge_path, '-J', expanduser(file_path)]).decode())

    except sp.CalledProcessError as e:
        raise ValueError(f'"{file_path}" could not be opened') from e
    return info_json['container']['type'] == 'Matroska'


def verify_recognized(file_path, mkvmerge_path='mkvmerge'):
    """Verify a file is recognized by mkvmerge.

    file_path (str):
        Path to the file to be verified.
    mkvmerge_path (str):
        Alternate path to mkvmerge if it is not already in the $PATH variable.
    """
    if not verify_mkvmerge(mkvmerge_path=mkvmerge_path):
        raise FileNotFoundError('mkvmerge is not at the specified path, add it there or change the mkvmerge_path '
                                'property')

    if not isinstance(file_path, str):
        raise TypeError(f'"{file_path}" is not of type str')
    file_path = expanduser(file_path)
    if not isfile(file_path):
        raise FileNotFoundError(f'"{file_path}" does not exist')
    try:
        info_json = json.loads(sp.check_output([mkvmerge_path, '-J', file_path]).decode())

    except sp.CalledProcessError as e:
        raise ValueError(f'"{file_path}" could not be opened') from e
    return info_json['container']['recognized']


def verify_supported(file_path, mkvmerge_path='mkvmerge'):
    """Verify a file is supported by mkvmerge.

    file_path (str):
        Path to the file to be verified.
    mkvmerge_path (str):
        Alternate path to mkvmerge if it is not already in the $PATH variable.
    """
    if not verify_mkvmerge(mkvmerge_path=mkvmerge_path):
        raise FileNotFoundError('mkvmerge is not at the specified path, add it there or change the mkvmerge_path '
                                'property')

    if not isinstance(file_path, str):
        raise TypeError(f'"{file_path}" is not of type str')
    file_path = expanduser(file_path)
    if not isfile(file_path):
        raise FileNotFoundError(f'"{file_path}" does not exist')
    try:
        info_json = json.loads(sp.check_output([mkvmerge_path, '-J', file_path]).decode())

    except sp.CalledProcessError as e:
        raise ValueError('"{}" could not be opened') from e
    return info_json['container']['supported']
