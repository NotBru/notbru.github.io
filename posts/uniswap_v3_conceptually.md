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
  - The formula
  - Price
  - Liquidity
  - Price and liquidity visually
  - The *actual* uniswap formula
- Novel concepts of Uniswap V3
  - The problem

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

### The formula

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

First of all, our AMM will provide liquidity between a pair at the time. We'll
call these tokens `X` and `Y`. Since we're providing liquidity, we need to have
reserves of these readily available for people to exchange; let us call `x` and
`y` the amount we have of each. Then, we'll allow people to make any change to
these reserves they'd like, as long as the product between these reserves is
the same after the transaction as it was before.

Quick example. Suppose our liquidity pool has the initial values
`(x, y) = (10, 1)`, and someone wants to extract `5 X` in exchange for some
`Y`. After the extraction, the amount of `X` will be `x = 5`. How much `Y`
must be added? well, the product `x . y` is `10 . 1 = 10` initially, and it
will be `5 . y` at the end. We can easily see that if `y = 2` in the previous
equation, then the product `5 . 2 = 10`, just as it was before. So, we must
provide `1 Y` in order to extract `5 X`.

The most important adavantage of this solution is that the price of the tokens
is updated automatically according to supply. For example, the above
transaction occurred at a price of `0.5 Y/X`. But if I wanted to buy `9 X`
instead, I'd have to provide `9 Y`, so it would happen at a price of `1 Y/X`,
double as before.

And this happens in such a way that the pool cannot be drained completely, too.
This means that bad pricing is *corrected* by arbitreurs, only to the point
where the price becomes precisely the market one. From then onwards, there's no
incentive to buy further, and the liquidity pool now operates at a proper
price.

I'll find it easier to explain this with some plots! If you're unfamiliar with
what's coming, bear with it for a second. It may be hard to understand at
first, but it's a great explanatory tool.

<img
    src="https://notbru.github.io/posts/uniswap_v3_conceptually/fig00.png"
    width="400"/>

In the graph, the horizontal displacement represents amount of `X` in the pool,
whereas the vertical one represents amount of `Y` in the pool. We can identify
any state our pool can be in through an `(x, y)` pair, which would be a point
in the graph. The bold line a set where all points `(x, y)` satisfy
`x . y = k`, with `k` a constant. In our example with numbers above, `k` would
be `10`, but whatever the value of `k`, the graph looks overall like that.

The dots represent posible states of the pool. Imagine I find the pool in the
state represented by the blue dot. I'm free to move the dot around, as long as
I keep it over the curve. The green dot then represents a posible final state,
after I perform a change in the state of the pool. `Δx` and `Δy` represent the
changes in `x` and `y`, the reserves of each token. In this transaction, we can
see I increased the amount of `X` and reduced the amount of `Y` in the pool,
meaning I bought `Y` in exchange for `X`.

One of the very important notions that this kind of pool satisfy, is that of
path independence. The pool has no proprietary (we'll talk about how it gets
its reserves shortly). It's just an entity of the aether, and people are free
to alter its state to their convenience, as long as one simple rule is
followed, and reap the benefits of “conservation of tokens”.

### Price

Now, there are two important notions that we'll need to define here. Namely,
“current price” and “liquidity”. But we've just seen that the exchange's price
depends on the size of the operation! Perhaps I exchange an euro and the price
is `1`, but if the amount of euros I want to exchange is close to the amount of
euros in the pool, the price may jump to infinity!

Yep. The price depends on the size of the transaction. But, as the name “pool”
implies, the pool is supposed to be a gigantic reserve of tokens. So, clients
that want modest exchanges shouldn't really reach a situation where the prices
go upwards to infinity. How is price computed exactly then? why, with
infinitesimals.

Suppose I find a pool with constant `x . y = k`, and want to buy `X`. Lets call
the amount of `x` we want `dx`, and the amount of `y` we'll have to incorporate
`dy`. Our operation will take the pool from a state `(x, y)` to a state
`(x - dx, y + dy)`.

But from the constant product constraint, `dx` and `dy` aren't arbitrary. We
must chose them so that `(x - dx)(y + dy) = k`. A simple application of the
distributive property, and the magic fact that `dx . dy` pales in comparison to
`dx` and to `dy` if they're both very very small, leads us to our result.

The price, for small changes `dx` and `dy`, of `X`, is `dy / dx = y / x`. What
a wonderful result! It's simply the ratio of suply between `Y` and `X`.

As a quick detour in our discussions, it's worth mentioning that price changes
lead to impermanent loss. It can be proven that if a pool is initalized at a
price in agreement with the market, and the market price changes, then the
worth of the pool (calculated as the sum of its assets in units of any of the
tokens) strictly diminishes. We'll talk more about that later.

Now, what constitutes a small exchange depends on how much of both `x` and `y`
there is, really. This leads us to the concept of “liquidity”. This quantity is
most precisely defined in Uniswap V3, where things get *reeeal*.

### Liquidity

To get an idea why liquidity will be defined as it will, let us notice that
supplying liquidity requires increasing `k`. Why? because the *rate* of change
of the price `p` with respect to changes `dx` is proportional to `1 / sqrt(k)`,
where `sqrt` stands for “square root of”. This means the higher `k` is, the
smaller the change in price will be.

We could thus simply define liquidity as `k`. Or, as already suggested by the
rate of change of price, as its square root. But any monotonously increasing
function of `k` suffices really. So, how do we pick one among the infinite
posibilities?

Well, there's a second nice property that `sqrt(k)` satisfies that is crucial.
Namely, it is *linear* on the amount of token that gets incorporated.

To see this, let us consider a pool that's initialized at a certain value of
`k0 = x . y` and at a certain price `p = y / x`. When providing liquidity at
the current price, with a proper increase `Δx` and `Δy`, it can be shown that
`k` changes from `k0` to `k1 = (sqrt(k0) + sqrt(Δx . Δy)) ^ 2`. But! if instead
of speaking about `k0` and `k1` we spoke about `L0 = sqrt(k0)` and
`L1 = sqrt(k1)`, we would say that liquidity `L` goes from `L0` to
`L1 = L0 + ΔL`, where `L0 = sqrt(x . y)` and `ΔL = sqrt(Δx . Δy)`.

By this definition of liquidity, two equal provisions of tokens represent the
same liquidity increase each, independent of their order. Any other definition
of liquidity, such as `L = k`, would lead to odd state-dependent changes in
liquidity for the very same operation!

Furthermore, the linearity property guarantees that if someone provides a given
amount of `X` and `Y`, and I provide a fraction of it, the differences in
liquidity will be related by this very same relationship.

## Price and liquidity visually

Uniswap V2 is moved by two kind of actors. I'll call them “swappers” and
“liquidity providers”. Liquidity providers increase liquidity at constant
price, and swappers “swap” between tokens at constant liquidity, moving the
price at its wake.

You've already seen what constant liquidity surfaces look like. It's the
painted curve in the first figure we've seen. But what do constant price
surfaces look like? Well, those surfaces are described by `p = y / x`, or to
put it another way, `y = p . x`. They're straight lines through the origin!

This graph shows both constant liquidity curves (solid lines) and constant
price curves (dashed lines).

<img
    src="https://notbru.github.io/posts/uniswap_v3_conceptually/fig01.png"
    width="400"/>

If you're a liquidity provider, you'll move along the dashed lines to take the
pool to higher liquidity states. If you're a swapper, you'll move along the
solid lines to exchange a few tokens, altering the price.

## The *actual* Uniswap V2 formula

Iiiit's not technically *a formula*. But, what incentives do liquidity
providers really have? Uniswap as we've already seen would simply have their
funds moved around, and provide nothing in return. The best that can happen is
you feel happy with yourself for helping other people play around with money.

But Uniswap doesn't apply this “constant product formula” as is. Rather, it
takes some profit from the input, which is the “fee”. So, whenever you're
actually swapping, the token that you provide has this fee substracted before
actually verifying that the new `x` and `y` values reached satisfy the
constraint.

Further, of course exact equality is not checked, but rather the inequality
`x . y >= L^2`. You're free to provide liquidity as part of the operation!

With those two in mind, each swap actually increases the pool's liquidity
slightly, which is then offered to the liquidity providers as a sacrifice
(others may call it revenue). Thus, you're incentivized to be a liquidity
provider whenever you expect the money you collect from fees to offset the
losses from possible price movements.

[v3swp]: https://uniswap.org/whitepaper-v3.pdf
[trad-to-block]: #from-traditional-exchanges-to-blockchain
[erc20]: https://ethereum.org/en/developers/docs/standards/tokens/erc-20/
[ucpf]: #uniswaps-constant-product-formula
