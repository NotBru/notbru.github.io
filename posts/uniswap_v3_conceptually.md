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
- [Uniswap's constant product formula][ucpf]
- Novel concepts of Uniswap V3

## From traditional exchanges to blockchain

**Full disclosure**: I know very little about traditional finances. But, as an
Argentinian, I feel the *compulsion* to explain things I know not so much
about. Feel free to contact me for any change suggestions or, heck, push a
merge request.

Traditional markets date back to the very first human exchange. Maybe I have a
pretty stone and the meat you're holding looks tasty, and I'd rather eat your
meat (*e_e*) than have my stone, and you'd rather have my stone than eat your
meat. Trade is the essence of all markets.

But before money, you'd exchange things with “intrinsic” value only, with the
dissadvantage that the value of something may be a fraction of something else.
Hence money. People learnt that instead of long chains of trades, they may as
well define something as representing a unit of value and use it as an
intermediary.

But then some people only take some kind of money, most notably based on
geography. You can't probably buy coffee at an European store with Argentinian
pesos (ARS). So if you live where currency X is used, but you wanna travel (or
move) where currency Y is used, you're gonna need someone that wants currency
X and is willing to pay for it in currency Y.

Hence centralized exchanges. Places where people gather to exchange stuff. Some
seople realized they can sell the *convenience* of not having to look for
another party. Those people or entities became *liquidity providers*. Liquidity
here means the property of your assets of being *usable*. And the way they
profit is that they exchange X for Y at a price different than they exchange Y
for X.

Let's use a concrete example: `EUR` to `ETH` exchanges. Bear in mind I'm using
made up market values. Do not exchange at this rate. Such a liquidity provider
would use `1 ETH = 1050 EUR` if you're getting ETH, but `1 ETH = 1000 ETH` if
you're getting USD. The gist of it is that they operate in places where there's
about the same demand both ways around.

This means for each person exchanging `1 ETH` one way, there's probably another
person exchanging `1 ETH` the other way. So someone wanted `1 ETH` and paid
`1050 EUR` for it, and someone else wanted `1000 EUR` and paid `1 ETH` for it.
At the end of those exchanges, the provider has `50 EUR` more.

There are other ways to provide liquidity, such as orchestrating an orderbook.
And there are other financial contracts that can be exchanged, such as options
or futures. But this post will only focus in currency-like stuff.

So, what has blockchain to do with it? Ethereum brought about a class of smart
contracts called [ERC20][erc20] tokens, which work precisely the way currencies
work: they can be owned and transferred. As a sidenote, some tokens cannot be
said to be truely *owned*, such as USDC or USDT, whose transfer can be
selectively frozen at will of the issuer.

This brings us to the issue at hand: provided these tokens exist, how do we go
about making a decentralized exchange over it?

## Uniswap's constant product formula

An AMM's value to an outsider is evident. Anything that takes some token and is
proven to return a specific amount of another token may serve to exchange
tokens. There's also the posibility of arbitraging: if the algorithm provides
an outdated price that's too cheap with respect to the market, then one can buy
cheap to the AMM and sell expensive outside.

This last “advantage” to outsiders may actually be seen as predatorial, and one
of the main issues for an AMM. A poor algorithm may lead to people draining the
AMM's funds if incentivized to do so.

Luckily, this problem has been proven (both theoretically and in practice) to
have a very neat solution (even, classes of solutions). Rather than introduce
the solution step by step, let's jump right into the solution and see how it
works!

$equation_test$

[v3swp]: https://uniswap.org/whitepaper-v3.pdf
[trad-to-block]: #from-traditional-exchanges-to-blockchain
[erc20]: https://ethereum.org/en/developers/docs/standards/tokens/erc-20/
[ucpf]: #uniswaps-constant-product-formula
