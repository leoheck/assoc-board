# Kicad Library

This is a library with custom parts (symbols, footprints and 3D models) used in our projects. These parts are usually out of the Kicad Library.

Please, follow the [KLC](http://kicad-pcb.org/libraries/klc/) as close as possible.

This project is currently using Kicad 5.1.6

## Managing the Library

There is a sample project called `board` that can be used as start for a new project and it can also be used to manage the this library.
Just clone this repo, and launch the sample project with:

```
cd board
kicad board.pro
```

## Available Parts

There are be 2 libraries. One for the GAPH made ICs and the second one, to add custom components that are not found on the original Kicad's Library. The custom parts are there to add missing 3D models, or to provide a custom, or easy to use footprint and symbol. 

1. GAPH Chips
2. GAPH Custom Parts

## Using the library

I recomend to clone this library inside your Kicad project renaming it to `library`.
This structure is found in the `board` sample project. This sample project can be used as a template for a new projet too.

