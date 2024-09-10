|               Generalized Trigonometry               |
| :--------------------------------------------------: |
| By Katherine Rose, Alexander Joseph and Joshua Piety |

<!--Add whitepaper link here when that is finished-->

# Generalized Trigonometry

Generalized Trigonometry is a python extension that provides trigonometric functions for systems other than a circle. For example, the following function draws a square:

<img src="https://latex.codecogs.com/gif.image?\inline&space;\large&space;\dpi{150}\bg{white}\text{square}(t)=\begin{cases}x=\text{cospoly}_4(t)\\y=\text{sinpoly}_4(t)\end{cases}" alt="A parametric equation square of t where x is equal to polygonal cosine 4 of t and y is equal to polygonal sine 4 of t"/>

## Functions

```py
import gentrig as gt
```

### Parabolic

```py
gt.sinp(x)
gt.cosp(x)
gt.tanp(x)
gt.cscp(x)
gt.secp(x)
gt.cotp(x)
```

Self-explanatory: Parabolic trig is similar to hyperbolic trig, but applied to a parabola instead of a hyperbola.

### Linear

```py
gt.sinl(x)
gt.cosl(x)
gt.tanl(x)
gt.cscl(x)
gt.secl(x)
gt.cotl(x)
```

Trigonometry applied to a line. This is actually equivalent to polygonal trig with 2 sides. For example:

<img src="https://latex.codecogs.com/gif.image?\inline&space;\large&space;\dpi{150}\bg{white}\text{sinl}(x)=\text{sinpoly}_2(x)" alt="linear sine of x is equal to polygonal sine 2 of x" />

However, due to implementation details the `sinl(x)` function in this library is much faster than `sinpoly(x,2)`.

### Polygonal

```py
# Where n is the number of sides
gt.sinpoly(x,n)
gt.cospoly(x,n)
gt.tanpoly(x,n)
gt.cscpoly(x,n)
gt.secpoly(x,n)
gt.cotpoly(x,n)
```

Polygonal trig is fun! You can draw regular polygons of "radius" 1 (unit polygons, perhaps) with arbitrary numbers of sides using just `sinpoly` and `cospoly`! The library won't stop you from using `sinpoly(x,n)` with when `n` is less than one or not an integer, but behavior in those cases is undefined. It's also worth noting that as n approaches infinity `sinpoly(x,n)` approaches `sin(x)`, which is pretty intuitive if you think of a circle as an infinite-sided polygon. You can plot this to get a unit polygon with n sides:

<img src="https://latex.codecogs.com/gif.image?\inline&space;\large&space;\dpi{150}\bg{white}\begin{cases}x=\text{cospoly}_n(t)\\y=\text{sinpoly}_n(t)\end{cases}" alt="A parametric equation where x is equal to polygonal cosine n of t and y is equal to polygonal sine n of t"/>

## Installing `gentrig`...

### From PyPI

`gentrig` has been released on PyPI! You can install it with `pip install gentrig` and use it like any other python library!

### From source

1. Clone this repo: `git clone https://github.com/KiARC/gentrig.git`
2. Move into the repository's directory: `cd gentrig`
3. Build and install with `pip`: `pip install .`

`gentrig` can now be imported within whichever environment's `pip` was used to install it.
