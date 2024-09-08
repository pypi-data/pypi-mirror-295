#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2022-05-25
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio

from typing import TYPE_CHECKING

import click

from . import parser


if TYPE_CHECKING:
    from lvmecp.actor import ECPCommand
    from lvmecp.module import PLCModule


@parser.command()
@click.option("--no-registers", is_flag=True, help="Does not output registers.")
async def status(command: ECPCommand, no_registers: bool = False):
    """Returns the enclosure status."""

    plc = command.actor.plc

    if no_registers is False:
        command.info(registers=(await plc.read_all_registers(use_cache=False)))

    modules: list[PLCModule] = [plc.dome, plc.safety, plc.lights]
    await asyncio.gather(
        *[
            module.update(force_output=True, command=command, use_cache=True)
            for module in modules
        ]
    )

    command.info(
        o2_percent_utilities=plc.safety.o2_level_utilities,
        o2_percent_spectrograph=plc.safety.o2_level_spectrograph,
    )

    return command.finish()
