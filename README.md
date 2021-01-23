# ASSoC Evaluation Board

Small and simple evaluation board for the ASSoC IC.

The IC is accessible through a USB-Serial dongle connected to the computer. The default symbol rate for 25 MHz clock is 11520 Bd (baud rate).

- Board [schematics](board-schematic.pdf)
- Production files [Release-0.1](https://github.com/leoheck/assoc-board/releases/tag/0.1)
- Assembly [Bill of Materials](board-bom.csv)

> This project uses Kicad 5.1.6

The library in this project is a git submodule.
Update/clone the library with the following command:

```
git submodule update --init --recursive
```

# Known issues

The ASSoC IC has some issues related to the interconnection of the power rails and the pads. At this moment it is not known if it works properly. This board will be used to investigate these issues and maybe bring it to life. 

# Pictures

![pcb top view](misc/board-top.png)
![pcb bottom view](misc/board-bottom.png)
