"""English versions of three modwaretechnology.com blog articles (EN site, /en/blog/).

Each entry mirrors its Turkish entry in blog_yazilar.py: same keys and the same body markup
(see that module's docstring), plus `tr`, the Turkish slug. `ilgili` and `diger` keep the
Turkish identifiers; the generator maps them. Internal links are root-absolute /en/... paths
ending in .html (see ceviri-rehberi.md). Headings are in sentence case; the generator
converts them to Title Case.
"""

YAZILAR_EN = [
    dict(
        tr="stm32-modbus-rtu-rs485",
        slug="stm32-modbus-rtu-rs485",
        baslik="Modbus RTU (RS-485) with STM32: what to watch for in hardware and firmware",
        title="Modbus RTU and RS-485 with STM32: What to Watch For | ModWare",
        kategori="Embedded software",
        ikon="code",
        desc="Modbus RTU with STM32: RS-485 transceiver choice, termination and biasing, direction control, the 3.5-character gap, CRC calculation and common field issues.",
        ozet="RS-485 transceiver selection, termination, direction control, frame timing and CRC: a checklist for Modbus RTU on STM32 that works reliably in the field.",
        lede="Modbus RTU is still one of the most widely used fieldbus protocols in industry. It looks simple on paper, but a device that works reliably in the field depends on getting a few critical details right in both hardware and firmware.",
        ilgili=["gomulu-yazilim", "elektronik-kart-tasarimi"],
        diger=["pcb-tasariminda-emc-kurallari", "elektronik-kart-tasarim-sureci", "pcb-tasarim-incelemesi-sik-yapilan-hatalar"],
        cta="Let's write your board's firmware together.",
        urun="Embedded software",
        govde="""
Modbus RTU is a simple serial communication protocol widely used to exchange data between PLCs, drives, energy analyzers and sensors. The physical layer is usually RS-485. A bus has one client (formerly called the master) and server devices (formerly called slaves) with addresses from 1 to 247; the client queries and the server responds.

Because the protocol is simple, it is easy to assume it will "just work"; yet most problems in the field come from hardware details and timing. Below, we have grouped what to watch for when designing an STM32-based device under two headings: hardware and firmware.

> **In short:** Terminate both ends of the bus, bias the bus at a single point, release the driver only after the last bit has been sent, separate frames with a 3.5-character silent interval and append the CRC in the correct byte order.

## Hardware: the RS-485 side

### Transceiver selection

- Since the STM32 runs from 3.3 V, an RS-485 transceiver powered from 3.3 V removes the need for level shifting.
- Transceivers with a **fail-safe** receiver keep it from outputting random characters when the bus is idle or disconnected.
- The **unit load** rating determines how many devices can be connected to the bus. The standard specifies 32 unit loads per bus; with 1/8 unit-load transceivers, many more devices can share the same bus.
- On long cable runs, **slew-rate-limited** transceivers reduce reflections and radiated noise.

### Termination and biasing

- **Termination:** A resistor close to the cable's characteristic impedance (typically 120 Ω) goes only at the two physical ends of the bus. Fitting a termination resistor on every device overloads the bus. Making termination selectable on the board with a jumper or a switch is a big help in the field.
- **Biasing:** When the bus is idle, there must be a defined voltage difference between A and B. To achieve this, A is pulled up to the supply and B is pulled down to ground through resistors at one point on the bus. Fail-safe transceivers reduce this need, but do not always eliminate it completely.

### Protection and isolation

Field cables are long and exposed to external disturbances. The bus is protected with TVS diodes (asymmetric types that suit the RS-485 common-mode range of −7 V to +12 V) and, where needed, series resistors or PTC fuses. In industrial environments where there may be a ground potential difference between devices, isolating the bus with a digital isolator and an isolated DC-DC converter is the safest solution.

### Cabling

- Use twisted-pair cable; with shielded cable, ground the shield at a single point.
- Connect devices in a daisy chain; avoid star topologies and long stubs.
- Run a common reference (GND) conductor alongside A and B.

## Firmware: the STM32 side

### Direction control (DE/RE)

RS-485 is half-duplex: only one device talks at a time. The driver is enabled (DE) before transmitting and released once transmission is complete. The most common mistake is releasing the driver while the last byte is still being sent; the end of that byte is then corrupted and the other side sees a CRC error.

- Release the driver when the USART's **transmission complete (TC)** flag is set. The transmit buffer empty (TXE) flag is set while the last byte is still on the bus.
- The USART peripherals of many newer series, such as the STM32F0, F3, G0, G4, L4 and H7, have a hardware **driver enable (DE)** output. This makes direction control independent of software timing; check the reference manual for the series you are using.

### Character format

The default character format in the Modbus specification is 8 data bits, even parity and 1 stop bit (8E1). If no parity is used, 2 stop bits are specified (8N2). Devices using 8N1 are also common in the field; what matters is that all devices on the bus use the same setting. Making this setting adjustable from the device menu or the configuration software is very useful in the field.

### Frame timing

In Modbus RTU, frames must be separated by at least **3.5 character times** of silence (the inter-frame gap, t3.5), and the gap between characters within a frame must not exceed **1.5 character times** (t1.5). For an 11-bit character (start bit, 8 data bits, parity bit and stop bit), one character time is 11 / baud rate:

| Baud rate | 1 character | 3.5 characters |
|---|---|---|
| 9600 | ≈ 1.15 ms | ≈ 4.0 ms |
| 19200 | ≈ 0.57 ms | ≈ 2.0 ms |
| 38400 and above | ≈ 0.29 ms or less | 1.75 ms (recommended fixed value) |

For baud rates above 19200, the specification recommends fixed values of 750 µs for 1.5 characters and 1.75 ms for 3.5 characters.

### Detecting the end of a frame

An efficient approach on the STM32 is to receive into a buffer with DMA and detect the end of the frame separately:

- The **idle line (IDLE) interrupt** is a common and practical method; however, it fires after a gap of about one character time and does not guarantee 3.5 characters.
- For full compliance with the specification, the 3.5-character silence is measured with a **timer (TIM)** that is restarted on every received byte.
- The **receiver timeout** feature of the USART peripherals in some STM32 series lets the hardware count this interval in bit times.

### CRC calculation

Every frame ends with a 16-bit CRC. The Modbus CRC is calculated with an initial value of 0xFFFF and the polynomial 0xA001 (0x8005 bit-reversed); the **low byte goes first** in the frame. A simple C implementation:

```c
uint16_t modbus_crc16(const uint8_t *buf, uint16_t len)
{
    uint16_t crc = 0xFFFF;
    for (uint16_t i = 0; i < len; i++) {
        crc ^= buf[i];
        for (uint8_t b = 0; b < 8; b++)
            crc = (crc & 1u) ? (uint16_t)((crc >> 1) ^ 0xA001u) : (uint16_t)(crc >> 1);
    }
    return crc; /* the low byte goes into the frame first, then the high byte */
}
```

At high baud rates or under heavy load, a table-driven implementation is faster. The hardware CRC unit in some STM32 series can also be used once its polynomial and bit order are configured.

### Function codes and the register map

The most commonly used function codes:

| Code | Function |
|---|---|
| 03 | Read Holding Registers |
| 04 | Read Input Registers |
| 06 | Write Single Register |
| 16 (0x10) | Write Multiple Registers |

When an unsupported request arrives, the device should return an exception code with the most significant bit of the function code set (code + 0x80): 01 Illegal Function, 02 Illegal Data Address, 03 Illegal Data Value. Documenting two points in the register map prevents most of the confusion in the field: whether addresses start at 0 or 1 (e.g., the 40001 notation) and in which order 32-bit values are written to the two registers.

## Common problems in the field

- **A and B swapped:** Manufacturers may use the A/B and +/− labels differently; this is the first thing to check.
- **Missing or excess termination:** Signal reflections and random errors.
- **No biasing:** The receiver sees random characters while the bus is idle.
- **Driver released too early:** The last byte is corrupted, causing a CRC error.
- **Parity and baud rate mismatch:** The device does not respond at all.
- **Response timeout too short:** The client sends a new request without waiting for the server's response.
- **Ground potential difference:** On long runs without isolation, errors and even hardware failures.

## Testing tips

During development, the fastest method is to test the device end to end with a USB–RS485 converter and Modbus client software running on a PC. A logic analyzer's Modbus decoder lets you see the frames and their timing, while looking at the A–B differential voltage on an oscilloscope reveals termination and reflection problems.

## Conclusion

A robust Modbus RTU device is the combination of correctly selected and protected RS-485 hardware, correct direction control, specification-compliant timing and a well-documented register map.

As part of our [embedded software development](/en/embedded-software.html) service, we develop Modbus RTU and RS-485 communication for STM32-based devices together with the team that designs the hardware. If you need a communication board, take a look at our [electronics and PCB design](/en/electronics-pcb-design.html) page as well.
""",
    ),
    dict(
        tr="pcb-tasarim-incelemesi-sik-yapilan-hatalar",
        slug="pcb-design-review-common-mistakes",
        baslik="Pre-production design review: the 15 most common mistakes",
        title="PCB Design Review: The 15 Most Common Mistakes | ModWare",
        kategori="Design review",
        ikon="eye",
        desc="What should you check before a PCB goes to production? The 15 most common mistakes in schematics, footprints, layout, manufacturability and files, with fixes.",
        ozet="From schematic to footprints, from layout to manufacturing files: 15 common mistakes to catch before you send a board to production.",
        lede="Sending a PCB to production is easy; remaking a faulty board costs both money and time. A systematic review before production catches most mistakes while they are still cheap to fix.",
        ilgili=["tasarim-incelemesi", "elektronik-kart-tasarimi", "pcb-uretimi"],
        diger=["pcb-uretimi-icin-gerekli-dosyalar", "pcb-tasariminda-emc-kurallari", "prototip-pcb-maliyetini-dusurme"],
        cta="Let's review your board before it goes to production.",
        urun="Design review",
        govde="""
The electrical rules check (ERC) and design rule check (DRC) in design tools are important, but they only check the rules they have been given. A poorly chosen part, a connector with a mirrored pinout or an undersized cooling area can pass these checks without a single error. That is why, before production, a board should be reviewed against a checklist and, if possible, by a second reviewer who did not do the design.

Below, we have grouped the 15 mistakes we come across most often in pre-production reviews under four headings.

> **In short:** Check the schematic first, then the footprints and the layout, then manufacturability and, last of all, the manufacturing files. Record every finding with its severity.

## Schematic

### 1. Missing or incorrect pull-up/pull-down resistors

Pull-up resistors on I²C lines, the reset pin and the pins that set the microcontroller's boot mode (such as BOOT0 on the STM32) are the most frequently forgotten connections. A pin left floating makes the board work sometimes and fail at other times.

### 2. Regulator calculation errors

A wrong resistor value in the feedback divider throws off the output voltage, and a wrong choice of inductor or output capacitor compromises the regulator's stability. Every value should be verified, one by one, against the manufacturer's formulas and recommendations.

### 3. Skipping the thermal calculation

In a linear regulator, the input–output voltage difference multiplied by the current turns into heat. Going from 24 V to 3.3 V at 100 mA means about 2 W; a small package cannot get rid of that much heat. Losses and temperature rise should be calculated for every power component.

### 4. Missing protection circuits

Reverse-connected supplies, voltage transients coming in over the cables and electrostatic discharge (ESD) are the main causes of failures in the field. Reverse-polarity protection, TVS diodes and a fuse or an eFuse are hard to add later, so they should be considered from the start.

### 5. Pin assignment conflicts

A microcontroller pin can have more than one function. Assigning a UART and a timer channel to the same pin, or picking a package in which the peripheral you need is not available, is only noticed once the firmware is being written. The pin assignment should be verified with the manufacturer's configuration tool.

## Footprints and layout

### 6. Footprint does not match the package

Packages with the same name can come in different variants: narrow and wide SOIC, QFNs in different sizes, or SOT-23 versions with different pin orders. Every footprint should be checked against the dimensions in the datasheet of the part you will actually buy.

### 7. Missing pin 1 and polarity markings

On diodes, LEDs, electrolytic capacitors and ICs, the orientation mark should be clearly visible on the silkscreen. These marks prevent reversed mounting both in assembly and during manual inspection.

### 8. Mirrored connector pinouts

Connector datasheets may give the pin numbers as seen from the top or from the bottom. A mirrored pin order between two mating boards or in a cable is a common and costly mistake.

### 9. Decoupling capacitors placed too far away

Decoupling capacitors placed far from the pins or connected through long traces cannot do their job. Each capacitor should be as close as possible to the pin it supplies.

### 10. Mechanical fit not checked

Mounting holes, height limits inside the enclosure and the alignment of connectors with the enclosure openings should be checked with a 3D model. A mechanical mismatch makes an electrically flawless board unusable.

## Manufacturability (DFM)

### 11. Values outside manufacturing capabilities

Very thin traces, very tight clearances or very small holes cannot be made by every manufacturer, or they add extra cost. Design rules should be set to match the capabilities of the manufacturer that will build the board.

### 12. Silkscreen on pads and illegible text

Silkscreen that runs onto pads interferes with soldering, and text that is too small cannot be printed. Reference designators should be a legible size and kept clear of pads.

### 13. Overlooked assembly requirements

Automated assembly needs fiducial marks, enough clearance from the board edge and, if required, panel rails. Parts too close to the edge can be damaged during depaneling.

### 14. No access for testing and programming

Without a programming connector (e.g., SWD) and test points on important signals, debugging and production testing become very difficult once the board has been built.

## Manufacturing files

### 15. Inconsistencies between files

Reference designators in the bill of materials (BOM) that do not match the PCB, unmarked do-not-place (DNP) parts, wrong rotations in the pick-and-place file (CPL) and files from different revisions getting mixed up will lead to a faulty build even for a correctly designed board. We explain which files are needed in our article on the [files required for PCB manufacturing](/en/blog/pcb-manufacturing-files.html).

## How should the review be done?

1. Run the review against a checklist and in a fixed order: schematic, footprints, layout, manufacturability, files.
2. Record every finding and give it a severity: blocks production, must be fixed, suggested improvement.
3. After the fixes, recheck not only what changed but also the areas those changes may affect.
4. If possible, have someone who did not do the design carry out the review; designers find it hard to see their own assumptions.

## Conclusion

A pre-production review costs a small fraction of a prototype round and often makes that round unnecessary altogether.

With our [design review](/en/design-review.html) service, we review your schematic and PCB files before they go to production and report our findings in order of severity. If you would like your board designed from scratch, take a look at our [electronics and PCB design](/en/electronics-pcb-design.html) page.
""",
    ),
    dict(
        tr="prototip-pcb-maliyetini-dusurme",
        slug="reduce-prototype-pcb-cost",
        baslik="9 ways to reduce prototype PCB costs",
        title="9 Ways to Reduce Prototype PCB Costs | ModWare",
        kategori="PCB manufacturing",
        ikon="layers",
        desc="What drives prototype PCB cost? How to shrink the budget through standard specs, layer count, board size, surface finish, the BOM and fewer revisions.",
        ozet="Standard manufacturing specs, board size, surface finish, the bill of materials and the number of revisions: practical ways to shrink your prototype budget.",
        lede="At the prototype stage, what strains the budget is usually not a single line item but the sum of many small decisions. With a few right decisions at the start of the design, you can manufacture the same board at a noticeably lower cost and in less time.",
        ilgili=["pcb-uretimi", "tasarim-incelemesi", "prototip-ar-ge"],
        diger=["pcb-uretimi-icin-gerekli-dosyalar", "pcb-tasarim-incelemesi-sik-yapilan-hatalar", "elektronik-kart-tasarim-sureci"],
        cta="Let's manufacture your PCBs together.",
        urun="PCB manufacturing",
        govde="""
The price of a PCB is a combination of board area, layer count, material, manufacturing tolerances, surface finish, special processes, quantity and lead time. If the board is also going to assembly, the part count, part availability and the complexity of the assembly come into play as well. The points below summarize the most effective ways to reduce cost without compromising quality or reliability.

> **In short:** Stick to standard manufacturing specs, use special processes only when they are truly needed, simplify the bill of materials (BOM) and, above all, reduce the number of revisions.

## 1. Stick to standard manufacturing specs

Manufacturers treat certain values as standard and offer their best prices for them: 1.6 mm FR-4, 35 µm (1 oz) copper, green solder mask, white silkscreen, and trace widths, clearances and hole diameters within the manufacturer's standard capabilities. Going beyond these values increases both price and lead time. Unless you really need them, choose standard values over very thin traces and small vias.

## 2. Choose the layer count to fit the need

The unit price rises with the layer count, but fewer layers are not always cheaper. Trying to fit a dense circuit onto fewer layers can make the board larger, cause EMC problems and require an extra prototype round. The right choice is made by looking at the total cost together with the circuit density and the current and noise requirements.

## 3. Shrink the board and use the panel efficiently

Price depends largely on board area. Removing unnecessary empty space and using rectangular outlines reduces the area. Several small boards can be manufactured on the same panel, and handling the boards as a panel also speeds up assembly.

## 4. Choose the surface finish for the job

HASL is usually the most economical option. For fine-pitch ICs and packages that need a flat surface, such as QFN and BGA, ENIG costs more but reduces soldering defects. Choosing the finish based on what the board really needs protects you from both unnecessary cost and assembly defects.

## 5. Avoid special processes unless needed

Processes such as blind and buried vias, via-in-pad filling, controlled impedance, castellated (half-hole) edges and heavy copper increase cost significantly. Some designs genuinely need them; where they are not needed, they only drive up the price.

## 6. Simplify the bill of materials

In prototype assembly, cost is often driven less by the number of parts than by the number of **unique part types**. For example, using a single value instead of 10 kΩ, 9.1 kΩ and 11 kΩ wherever the circuit allows reduces the number of lines in the BOM.

- Prefer common parts that are in stock at more than one distributor.
- Avoid parts that are discontinued or have long lead times.
- Try to stick to a single package size for passive parts (e.g., 0603).

## 7. Place parts on one side if possible

Spreading parts over both sides means a second pass in assembly, an extra stencil and extra work. If space allows, keeping the SMD parts on one side of the board lowers the assembly cost.

## 8. Plan quantity and lead time

The unit price drops as the quantity goes up; for a first prototype, 5–10 pieces is often the most balanced choice. Express manufacturing, on the other hand, adds a significant extra cost. Planning the schedule from the start prevents rushed and expensive orders.

## 9. Reduce the number of revisions

The most expensive prototype is the one that has to be built again. Every new round means boards, parts, assembly, shipping and, most importantly, time. Running a [design review](/en/design-review.html) before production, adding test points and a programming connector, and providing footprints that can be left unpopulated wherever tuning may be needed often make the next round unnecessary.

## How does each decision affect cost?

| Decision | Effect on cost | When should you choose it? |
|---|---|---|
| Standard thickness and copper | Low cost, short lead time | Always, unless there is a special requirement |
| More layers | Higher unit price | Dense circuits, high-speed signals, EMC requirements |
| ENIG finish | Moderate increase | Fine-pitch packages and packages that need a flat surface |
| Via-in-pad, blind vias | Significant increase | Very dense, fine-pitch designs |
| Single-sided assembly | Savings in assembly | When space allows |
| Express manufacturing | Significant increase | Genuinely urgent cases |

## Conclusion

The most effective way to reduce prototype cost is not to blindly pick the cheapest options, but to avoid unnecessary special processes and reduce the number of revisions. The right decisions make both today's prototype and tomorrow's volume production cheaper.

With our [PCB manufacturing](/en/pcb-manufacturing.html) service, we check your files before production and work with you to choose the manufacturing options that suit the job and the budget. If you would like to plan your product from the idea stage onward, take a look at our [prototyping and R&D](/en/prototyping-rd.html) page.
""",
    ),
]
