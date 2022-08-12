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
  - The *actual* Uniswap formula
- [Nobel concepts of Uniswap V3][uv3]
  - The problem with Uniswap V2

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
state represented by the upper dot. I'm free to move the dot around, as long as
I keep it over the curve. The lower dot then represents a posible final state,
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

### The *actual* Uniswap V2 formula

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

It's also worth noting that, with this “loss” of input token, it's now
impractical to just play around. Going back and forth would be impossible, and
the oscillations would eventually die out.

## Nobel concepts of Uniswap V3

### The problem with Uniswap V2

Uniswap V2 distributes liquidity uniformly across al possible prices. But to
get a sense of what we mean by this, let's first go for an example.

Let's first assume we're dealing with coins without much volatility. For
example, `DAI` and `LUSD`, which are both pegged to the same value in dollars.
Even though they do have some fluctuations, they're known to oscillate around
`1` very consistently.

Now, suppose you're a trader who wants to swap `1000 DAI` for about
`1000 LUSD`. Now, suppose the fee is `3 / 1000` (for stablecoins these are
lower, but nevermind that), so you're okay with receiving `997 LUSD`. What's
more, you know you may move the price a little, so you decide you're okay with
a little less than that even.

Now, suppose the liquidity pool has a `10 kDAI` and `10 kLUSD`. This amounts to
a current price of precisely `1`, and liquidity `10000`. But the swapped amount
is so big in comparison, that the actual swap would yield about `907 LUSD`.
This trader would have to swap small amounts, and wait each time for someone to
swap about the same amount in the opposite direction so that the price of their
swaps are about the actual prices. And you don't even need a big trader for
this. A small run of `5` people who wanted to trade `2 kDAI` each would have
the same effect, except that after a few swaps the price would have changed so
much that the transactions would actually revert due to slippage constraints.

But the pool very much has the posibility to handle this one “big” transaction.
We know for a fact that stablecoins, when they don't fail, will really remain
at about the same exchange rate. So, it wouldn't really hurt to allow for the
transactions to happen at a higher “ficticious” liquidity. We know noone would
probably want to exchange `DAI` for `LUSD` at a rate of `0.9` nor viceversa
anyways.

### Concentrated liquidity

So, with this in mind, we decide to construct a pool that behaves like a
Uniswap V2 pool as long as it has reserves to do so, but we plan to run out of
them when a certain limit is reached. For instance, when the rate of exchange
of `DAI` to `LUSD` reaches `0.9`.

Our pool will have a “ficticious” liquidity `L` such that a swap that takes
`10 kLUSD` from it will take the price `p` to `0.9`. Our imaginary pool has
imaginary reserves `x` and `y` such that these numbers match, where `X` is the
input token (`DAI`) and `Y` is the output token (`LUSD`).

To help us with this, we'll be counting on equations `x . y = L^2` and
`y / x = p`. Our initial state is then characterized by `x0 . y0 = L^2` and
`y0 / x0 = p0` and, after variations `Δx` and `Δy` on reserves, we arrive to a
final state where `(x0 + Δx)(y0 - Δy) = L^2` and `(y0 - Δy)/(x0 - Δx) = p1`.

These are just the general equations for movements of Uniswap V2 balances. Now,
we shall deduce what ficticious values for those coordinates would be needed so
that, after `1 kLUSD` has been taken from the pool, the price drops from `1` to
`0.9`.

To do this, we simply define `p0 = 1`, `Δy = 1 k`, and `p1 = 0.9`. I'll leave
the intermediate steps out, since this is a simple set of equations. What we do
find after that is that liquidity should be about `195 k`, about `20` times
higher as before. With this new liquidity value, the problematic transaction
above would yield `991 LUSD`, at a much more acceptable rate of `0.99`, with
the same capital.

What happens if people *do* swap until the limiting price is reached? Well,
liquidity has been drained empty, and of course we can't continue providing
liquidity.

Notice that this liquidity provision covers the price range `1` to `0.9`, which
will be used if people buy `LUSD`. We can use the so far unmentioned `DAI` to
cover for precisely the opposite transactions, until the price of `DAI` becomes
`0.9`. When referring to pools, an implicit order is defined, and we speak of
the price as referring to one specific token. Since we started speaking about
buying `LUSD`, we may speak about the converse situation by saying that the
price reaches `1 / 0.9`, which is about a `1.11` price of `LUSD`.

This pool now operates between prices `0.9` and `1.11`, and we can 
visualize it like this:

<img
    src="https://notbru.github.io/posts/uniswap_v3_conceptually/fig02.png"
    width="400"/>

The dot here represents the state of the pool before any transactions. The
dashed lines represent a “collapse to 0” that happens at the borders. We've
confined movement between a set of *ticks*, but in exchange we've gained a
substantial liquidity bump. Our money gets used for swaps at a price that we
know will be needed, and no money is reserved for swaps at prices that we know
will only occur at the collapse of mankind, or worse, at the collapse of
Ethereum.

Now, I find it useful to highlight that providing liquidity to one of the sides
of the current price only requires providing the token that would get taken
from the pool in order to move that way. Intervals in this sense are
*decomposable*, in that you can think of any interval as composed by as many
sub intervals as needed, each providing the required assets so as to cover
price changes from one extremum to the other.

In Uniswap V2, when swapping, there was a connected curve defined by the
constancy of a state function that we called “liquidity”. This is true so far
too, except that this connected curve has been bounded. And we indeed
constructed this curve by thinking of it in terms of a side to the right of
the current price, and a side to the left.

Now, how do we get people to agree which range to provide liquidity on? we just
don't! Now that we know that we can think things in terms of price and
liquidity, we simply let people decide where they want to allocate liquidity
and, since liquidity is linear (i.e., additive) for a given price, overlapping
liquidities simply add on top of each other.

For example, suppose liquidity providers agree that `1` is the preferential
price between `DAI` and `USDT`, but they disagree on the deviations they
expect from this equilibrium point. Some may want to provide liquidity for
deviations of up to `5%`, others to `10%`, maybe some to `15%`. We would then
find that the pool has more liquidity at `1`, but then the segments decrease
until there's no more liquidity. Such a pool would look like this

<img
    src="https://notbru.github.io/posts/uniswap_v3_conceptually/fig03.png"
    width="400"/>

Actual liquidity pools aren't symmetric at all, nor are they centered around 1,
of course. You can check liquidity distribution (in a way more understandable
`(price, liquidity)` graph) for any pool by going to UniV3's [app][uv3app] and,
after having connected your wallet, accessing the “add liquidity” sections.

It is also important to highlight here that the swap's result *doesn't
correspond* to the difference in *virtual* reserves on the plots shown above.
It corresponds to the actual differences in reserves. But you can obtain them
from the plotted curves by adding the swapped amounts for the infinitesimal
displacements along the connected curves, disregarding the jump of liquidity
in doing so.

What you're essentially doing by swapping is changing the price little by
little, consuming the reserves ahead and adding (little more than) the reserves
that are needed behind so that the pool can continue operating in the same
state you found it before the swap.

If you're interested in digging the details, you're now hopefully more prepared
to go into Uniswap's whitepaper or, heck, feel free to check they're code at
GitHub! (it's open source uwu).

Do also feel free to contact me to give me any kind of feedback <3.

Many thanks to Capu also, for giving me the motivation to go out of my way and
make a post about this. He liked the “spiderweb graph” above very much.

[v3swp]: https://uniswap.org/whitepaper-v3.pdf
[trad-to-block]: #from-traditional-exchanges-to-blockchain
[erc20]: https://ethereum.org/en/developers/docs/standards/tokens/erc-20/
[ucpf]: #uniswaps-constant-product-formula
[uv3]: #nobel-concepts-of-uniswap-v3
[uv3app]: https://app.uniswap.org
