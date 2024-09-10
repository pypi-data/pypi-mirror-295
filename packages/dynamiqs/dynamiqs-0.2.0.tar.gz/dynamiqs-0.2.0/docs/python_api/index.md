# Python API

The **dynamiqs** Python API features two main types of functions: solvers of differential equations describing quantum systems, and various utility functions to ease the creation and manipulation of quantum states and operators.

## Quantum solvers

::: dynamiqs.integrators
    options:
        table: true
        members:
        - sesolve
        - mesolve
        - smesolve
        - sepropagator
        - mepropagator

## Core

### Time-dependent arrays

::: dynamiqs.time_array
    options:
        table: true
        members:
        - TimeArray
        - constant
        - pwc
        - modulated
        - timecallable

### Solvers (dq.solver)

::: dynamiqs.solver
    options:
        table: true
        members:
        - Tsit5
        - Dopri5
        - Dopri8
        - Kvaerno3
        - Kvaerno5
        - Euler
        - Rouchon1
        - Rouchon2
        - Expm

### Gradients (dq.gradient)

::: dynamiqs.gradient
    options:
        table: true

### Options

::: dynamiqs.options
    options:
        table: true

### Results

::: dynamiqs.result
    options:
        table: true

## Utilities

### Operators

::: dynamiqs.utils.operators
    options:
        table: true

### States

::: dynamiqs.utils.states
    options:
        table: true

### Quantum utilities

::: dynamiqs.utils.quantum_utils
    options:
        table: true

### JAX-related utilities

::: dynamiqs.utils.jax_utils
    options:
        table: true

### Vectorization

::: dynamiqs.utils.vectorization
    options:
        table: true

### Quantum optimal control

::: dynamiqs.utils.optimal_control
    options:
        table: true

### Random arrays (dq.random)

::: dynamiqs.random
    options:
        table: true

### Plotting (dq.plot)

::: dynamiqs.plot
    options:
        table: true
        members:
        - wigner
        - wigner_mosaic
        - wigner_gif
        - pwc_pulse
        - fock
        - fock_evolution
        - hinton
        - gifit
        - grid
        - mplstyle
