"""Configuration definitions

Part of `sopel-slap`.

Copyright 2024, dgw, technobabbl.es

https://sopel.chat
"""
from __future__ import annotations

from sopel.config import types

VERBS = (
    'annihilates',
    'destroys',
    'kicks',
    'owns',
    'punches',
    'pwns',
    'roundhouse kicks',
    'slaps',
)


class SlapSection(types.StaticSection):
    verbs = types.ListAttribute('verbs', default=VERBS)


def do_configure(section: types.StaticSection):
    section.configure_setting(
        'verbs',
        "\nEnter verbs to choose from when slapping someone, one per line.\n\n"
        "Alternatively, press Enter twice without typing anything to write\n"
        "the current list (shown below) to your bot's .cfg file, where it\n"
        "can be edited using your favorite text editor.\n\n"
        "Current verb list:",
    )
