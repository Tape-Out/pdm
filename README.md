# pdm

One sentence saying what this block does.

![maturity](https://img.shields.io/badge/maturity-planned-lightgrey) ![license](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0%20OR%20MulanPSL--2.0-blue)

Part of the [Tape-Out](https://github.com/Tape-Out) IP library: Bluespec IP over the bus-neutral contracts in
[`hwcore`](https://github.com/Tape-Out/hwcore), assembled by [`xirang`](https://github.com/Tape-Out/xirang). Maturity runs
`planned` -> `simulated` -> `fpga-proven` -> `asic-ready` -> `silicon-proven`.

## Status

Planned. The skeleton implements a scratch register mirrored to a read-only register while
enabled, so that generation, type checking and the register consistency test all have
something real to run against. Replace it.

## Parameters

| Parameter | Range | Meaning |
| :--: | :--: | :-- |
| `dataWidth` | 1 to 32 | width of `data` and `mirror` |
| `invert` | bool | mirror the complement |

## Registers

| Offset | Register | Contents |
| :--: | :-- | :-- |
| 0x00 | `ctrl` | bit 0 enables the mirror |
| 0x04 | `data` | value written by software |
| 0x08 | `mirror` | `data` while enabled, zero otherwise |

## License

任选其一：

- [MIT](LICENSE-MIT)
- [Apache 2.0](LICENSE-APACHE)
- [木兰宽松许可证 第2版](LICENSE-MULAN)

`SPDX-License-Identifier: MIT OR Apache-2.0 OR MulanPSL-2.0`

除非另行说明，你提交的贡献按上述三者同时授权，不附加其他条件。
