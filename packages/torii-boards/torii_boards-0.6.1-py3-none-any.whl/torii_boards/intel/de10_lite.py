# SPDX-License-Identifier: BSD-2-Clause

import warnings

from ..altera.de10_lite import DE10LitePlatform

__all__ = (
	'DE10LitePlatform',
)

warnings.warn(
	'The `IntelPlatform` and `torii_boards.intel` module have been renamed to `AlteraPlatform` and'
	' `torii_boards.altera` respectively.\n'
	f'Replace all instances of `{__name__}` with `torii_boards.altera.{__name__.split(".")[-1]}`.',
	DeprecationWarning, stacklevel = 2
)


if __name__ == '__main__':
	from ..test.blinky import Blinky
	DE10LitePlatform().build(Blinky(), do_program = True)
