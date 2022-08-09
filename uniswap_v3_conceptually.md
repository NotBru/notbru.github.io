# Uniswap V3 conceptually

Uniswap is an AMM (Automated Market Maker). A smart contract you can use for
exchange between currencies. In the passing from operated market makers (i.e.,
traditional exchanges) to AMMs, many problems had to be solved *differently*.

This post aims to incrementally explain Uniswap's latest version, V3, which
features concentrated liquidity provision. If you don't know anything about
Uniswap, this hopefully serves as a brief introduction. If you are familiar
with V1 and V2, or even if you're already digging V3's wonderful
[whitepaper][v3swp], it may still be useful to read the sections on V3, since I
intend on explaining the conceptual differences I struggled with upon my first
approach to UniV3.

### Sections

- [From traditional exchanges to blockchain][trad-to-block]
- Uniswap's constant product formula
- Novel concepts of Uniswap V3

## From traditional exchanges to blockchain

[v3swp]: https://uniswap.org/whitepaper-v3.pdf
[trad-to-block]: #from-traditional-exchanges-to-blockchain
