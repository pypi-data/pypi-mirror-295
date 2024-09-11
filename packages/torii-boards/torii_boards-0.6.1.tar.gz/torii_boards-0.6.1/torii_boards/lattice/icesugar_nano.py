# SPDX-License-Identifier: BSD-2-Clause

from torii.build                         import Connector, Resource, Pins, Clock, Attrs
from torii.build.run                     import BuildProducts
from torii.platform.vendor.lattice.ice40 import ICE40Platform
from torii.platform.resources            import (
	LEDResources, UARTResource, SPIFlashResources
)

__all__ = (
	'ICESugarNanoPlatform',
)


class ICESugarNanoPlatform(ICE40Platform):
	device      = 'iCE40LP1K'
	package     = 'CM36'
	default_clk = 'clk12'

	resources   = [
		Resource(
			'clk12', 0, Pins('D1', dir = 'i'), Clock(12e6),
			Attrs(GLOBAL = True, IO_STANDARD = 'LVCMOS33')
		),

		*LEDResources(pins = 'B6', invert = False, attrs = Attrs(IO_STANDARD = 'LVCMOS33')),

		UARTResource(0,
			tx = 'B3', rx = 'A3',
			attrs = Attrs(IO_STANDARD = 'LVTTL33', PULLUP = 1)
		),

		*SPIFlashResources(0,
			cs_n = 'D5', clk = 'E5', copi = 'E4', cipo = 'F5',
			attrs = Attrs(IO_STANDARD = 'LVCMOS33')
		),
	]

	connectors = [
		Connector('pmod', 0, 'E2 D1 B1 A1 - -'),                    # PMOD1
		Connector('pmod', 1, 'B3 A3 B6 C5 - -'),                    # PMOD2
		Connector('pmod', 2, 'B4 B5 E1 B1 - - C6 E3 C2 A1 - -'),    # PMOD3
	]

	def toolchain_program(self, products: BuildProducts, name: str) -> None:
		from os         import environ
		from subprocess import check_call

		iceprog = environ.get('ICEPROG', 'iceprog')
		with products.extract(f'{name}.bin') as bitstream_filename:
			check_call([iceprog, bitstream_filename])


if __name__ == '__main__':
	from ..test.blinky import Blinky
	ICESugarNanoPlatform().build(Blinky(), do_program = True)
