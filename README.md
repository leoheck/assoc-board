# ASSoC Evaluation Board

Small and simple evaluation board for the ASSoC IC

The IC is acessible through a usb-serial dongle connected to the computer. The default symbol rate for 25 MHz clock is 11520 Bd (baud rate).

- Board (schematics)[board-schematic.pdf]
- Production files (Realease-0.1)[https://github.com/leoheck/assoc-board/releases/tag/0.1]
- Assembly (Bill of Materials)[board-bom.csv]

> This project uses Kicad 5.1.6

The library in this project is a git submodule.
Update/clone the library with the following command:

```
git submodule update --init --recursive
```

# Pictures

![pcb top view](misc/board-top.png)
![pcb bottom view](misc/board-bottom.png)
