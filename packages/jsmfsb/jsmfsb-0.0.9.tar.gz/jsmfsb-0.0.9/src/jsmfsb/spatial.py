# spatial code from chapter 9
# Note that the actual simulation code is in the Spn object in the spn module

import jax
from jax import jit
import jax.numpy as jnp
import jax.lax as jl

def simTs1D(key, x0, t0, tt, dt, stepFun, verb=False):
    """Simulate a model on a regular grid of times, using a function (closure)
    for advancing the state of the model

    This function simulates single realisation of a model on a 1D
    regular spatial grid and regular grid of times using a function
    (closure) for advancing the state of the model, such as created by
    `stepGillespie1D`.

    Parameters
    ----------
    key: JAX random number key
      Initial random number key to seed the simulation.
    x0 : array
      The initial state of the process at time `t0`, a matrix with
      rows corresponding to reacting species and columns
      corresponding to spatial location.
    t0 : float
      The initial time to be associated with the initial state `x0`.
    tt : float
      The terminal time of the simulation.
    dt : float
      The time step of the output. Note that this time step relates
      only to the recorded output, and has no bearing on the
      accuracy of the simulation process.
    stepFun : function
      A function (closure) for advancing the state of the process,
      such as produced by `stepGillespie1D`.
    verb : boolean
      Output progress to the console (this function can be very slow).

    Returns
    -------
    A 3d array representing the simulated process. The dimensions
    are species, space, and time.

    Examples
    --------
    >>> import jsmfsb.models
    >>> import jax
    >>> import jax.numpy as jnp
    >>> lv = jsmfsb.models.lv()
    >>> stepLv1d = lv.stepGillespie1D(jnp.array([0.6,0.6]))
    >>> N = 10
    >>> T = 5
    >>> x0 = jnp.zeros((2,N))
    >>> x0 = x0.at[:,int(N/2)].set(lv.m)
    >>> k0 = jax.random.key(42)
    >>> jsmfsb.simTs1D(k0, x0, 0, T, 1, stepLv1d, True)
    """
    N = int((tt - t0)//dt + 1)
    u, n = x0.shape
    keys = jax.random.split(key, N)
    @jit
    def advance(state, key):
        x, t = state
        if (verb == True):
            jax.debug.print("{t}", t=t)
        x = stepFun(key, x, t, dt)
        t = t + dt
        return (x, t), x
    _, arr = jl.scan(advance, (x0, t0), keys)
    return jnp.moveaxis(arr, 0, 2)
    

def simTs2D(key, x0, t0, tt, dt, stepFun, verb=False):
    """Simulate a model on a regular grid of times, using a function (closure)
    for advancing the state of the model

    This function simulates single realisation of a model on a 2D
    regular spatial grid and regular grid of times using a function
    (closure) for advancing the state of the model, such as created by
    `stepGillespie2D`.

    Parameters
    ----------
    key: JAX random number key
      Random key to seed the simulation.
    x0 : array
      The initial state of the process at time `t0`, a 3d array with
      dimensions corresponding to reacting species and then two
      corresponding to spatial location.
    t0 : float
      The initial time to be associated with the initial state `x0`.
    tt : float
      The terminal time of the simulation.
    dt : float
      The time step of the output. Note that this time step relates
      only to the recorded output, and has no bearing on the
      accuracy of the simulation process.
    stepFun : function
      A function (closure) for advancing the state of the process,
      such as produced by `stepGillespie2D`.
    verb : boolean
      Output progress to the console (this function can be very slow).

    Returns
    -------
    A 4d array representing the simulated process. The dimensions
    are species, two space, and time.

    Examples
    --------
    >>> import jsmfsb.models
    >>> import jax
    >>> import jax.numpy as jnp
    >>> lv = jsmfsb.models.lv()
    >>> stepLv2d = lv.stepGillespie2D(jnp.array([0.6,0.6]))
    >>> M = 10
    >>> N = 15
    >>> T = 5
    >>> x0 = jnp.zeros((2,M,N))
    >>> x0 = x0.at[:,int(M/2),int(N/2)].set(lv.m)
    >>> k0 = jax.random.key(42)
    >>> jsmfsb.simTs2D(k0, x0, 0, T, 1, stepLv2d, True)
    """
    N = int((tt - t0)//dt + 1)
    u, m, n = x0.shape
    keys = jax.random.split(key, N)
    @jit
    def advance(state, key):
        x, t = state
        if (verb == True):
            jax.debug.print("{t}", t=t)
        x = stepFun(key, x, t, dt)
        t = t + dt
        return (x, t), x
    _, arr = jl.scan(advance, (x0, t0), keys)
    return jnp.moveaxis(arr, 0, 3)


# eof


