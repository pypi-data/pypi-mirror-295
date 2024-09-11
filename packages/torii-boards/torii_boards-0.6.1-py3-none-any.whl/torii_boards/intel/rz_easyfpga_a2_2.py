# SPDX-License-Identifier: BSD-2-Clause

import warnings

from ..altera.rz_easyfpga_a2_2 import RZEasyFPGAA2_2Platform

__all__ = (
	'RZEasyFPGAA2_2Platform',
)

warnings.warn(
	'The `IntelPlatform` and `torii_boards.intel` module have been renamed to `AlteraPlatform` and'
	' `torii_boards.altera` respectively.\n'
	f'Replace all instances of `{__name__}` with `torii_boards.altera.{__name__.split(".")[-1]}`.',
	DeprecationWarning, stacklevel = 2
)


if __name__ == '__main__':
	from ..test.blinky import Blinky
	RZEasyFPGAA2_2Platform().build(Blinky(), do_program = True)
