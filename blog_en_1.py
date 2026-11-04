"""modwaretechnology.com English blog articles, batch 1 (translated from blog_yazilar.py).

Body markup is the same as in blog_yazilar.py:
  ## Heading        -> h2 (goes into the table of contents)
  ### Heading       -> h3
  - item           -> bulleted list
  1. item          -> numbered list
  > text           -> callout box
  | a | b |        -> table (first row is the header, second row is |---|)
  ```c ... ```     -> code block
  **bold**, `code`, [text](/en/path.html)
Each entry has the same keys as its Turkish counterpart plus `tr` (the Turkish slug).
`ilgili` and `diger` stay as Turkish identifiers; the generator maps them to the EN pages.
Internal links are root-absolute under /en/ and end in .html (the generator turns them into clean URLs).
Headings are written in sentence case; the generator converts them to Title Case.
"""

YAZILAR_EN = [
    dict(
        tr="elektronik-kart-tasarim-sureci",
        slug="electronics-design-process",
        baslik="The electronics design process: from idea to mass production, step by step",
        title="Electronics Design Process: Idea to Mass Production | ModWare",
        kategori="Electronics design",
        ikon="chip",
        desc="How is an electronic board designed? Every step from requirements and schematic to PCB layout, prototype testing and mass production, and what to watch for.",
        ozet="From requirements to schematic, from PCB to prototype and mass production: the steps an electronic board goes through and what to watch for at each one.",
        lede="Getting an electronic board from an idea on the table to mass production takes a few clear steps. Knowing what each step solves has a direct impact on both the timeline and the cost of the project.",
        ilgili=["elektronik-kart-tasarimi", "prototip-ar-ge", "pcb-uretimi"],
        diger=["pcb-uretimi-icin-gerekli-dosyalar", "pcb-tasarim-incelemesi-sik-yapilan-hatalar", "prototip-pcb-maliyetini-dusurme"],
        cta="Let's design your board together.",
        urun="Custom hardware design",
        govde="""
Electronic board design is often summed up as "draw the schematic, draw the PCB, get it made." In practice, whether the board runs reliably in the field depends on decisions made before the schematic is even started. Below, we describe the steps a board goes through from idea to mass production, along with the points that are often overlooked at each step.

> **In short:** Requirements → architecture and component selection → schematic and calculations → PCB layout → manufacturing files and prototype → testing and verification → transition to mass production. Putting a checkpoint at the end of each step lets you catch errors while they are still cheapest to fix.

## 1. Put the requirements in writing

This is the cheapest and most effective step in the design. It must be clear not only what the board will do, but also where and under what conditions it will operate. A short requirements document should answer at least the following questions:

- **Function:** What will the board measure, what will it drive, and what decisions will it make?
- **Power supply:** What is the input voltage, and how much can it fluctuate; is it a battery or an adapter? In 12, 24 or 48 V systems, sudden voltage spikes must also be taken into account.
- **Interfaces:** RS-485, CAN, USB, Ethernet or wireless communication; sensor and actuator connections.
- **Environment:** Operating temperature, humidity, dust and vibration. An industrial control panel and an office environment do not call for the same design.
- **Mechanical:** Board dimensions, enclosure, connector positions and mounting holes.
- **Quantity and target cost:** 10 units and 10,000 units call for different component and manufacturing decisions.
- **Regulations:** EMC and safety requirements for CE marking; the rules of the market where the product will be sold.

This document also prevents the "let's add this feature too" kind of scope creep later on. When a new request comes in, its impact is assessed against the document.

## 2. Architecture and component selection

Once the requirements are clear, the block diagram of the board is drawn: power stage, microcontroller, sensor inputs, driver outputs and communication interfaces. The decisions made at this stage largely determine the board's cost and supply risk.

- **Microcontroller:** The required peripherals (ADC, timers, UART, CAN), memory and software ecosystem are evaluated together. Broad families such as STM32 make it easier to move to a more powerful or a cheaper model later on.
- **Power architecture:** A linear regulator (LDO) is simple and quiet, but if the difference between input and output is large, so is the power turned into heat. With 24 V in, 3.3 V out and a 100 mA load, an LDO produces about 2 W of heat; here a switching (buck) converter is the better choice.
- **Availability:** Parts that are end-of-life (EOL) or not recommended for new designs (NRND) are avoided. Equivalent alternatives for critical parts are identified from the start.

## 3. Schematic design and calculations

The schematic is the electrical definition of the board. A good schematic carries not only the correct connections but also the reasoning behind the design decisions.

- Inductor, capacitor and feedback values for the regulators are calculated using the manufacturer's formulas.
- Protection against reverse connection, overvoltage and short circuits (reverse-polarity protection, a TVS diode, a fuse or an electronic fuse) is added.
- Every supply pin gets a decoupling capacitor; the required resistors are added to the I²C lines and to the reset and boot pins.
- The programming and debug connector (for example, SWD for STM32) and the test points must not be forgotten.

Once the schematic is finished, having a second pair of eyes review it before moving on to the PCB is the cheapest form of debugging. On this topic, you can also read our article on [the most common mistakes found in a pre-production design review](/en/blog/pcb-design-review-common-mistakes.html).

## 4. PCB placement and routing

Order matters in PCB design: placement first, then routing. Connectors and mounting holes are locked in position according to the mechanical drawing; then the power stage, the microcontroller and the sensitive analog sections are placed.

- **Layer stackup:** The layer count is chosen based on circuit density, current and noise requirements. A continuous ground plane improves both signal quality and EMC performance.
- **Current-carrying traces:** Trace widths are calculated from the current they will carry and the allowed temperature rise. IPC-2152 is the standard used for this calculation.
- **Noise:** The current loops of the switching power stage are kept small, and sensitive signals are kept away from this area. For details, see our article on [EMC rules in PCB design](/en/blog/pcb-emc-design-rules.html).
- **Checks:** The design rule check (DRC) is run against the manufacturer's capabilities, and the 3D model is used to check for enclosure and connector clashes.

## 5. Manufacturing files and prototype

Having the PCB made requires standard manufacturing outputs, not the design tool's native file: Gerber files, the drill file, the bill of materials (BOM) and the pick-and-place file for assembly. We explain what each file is for in detail in our article on [the files required for PCB manufacturing](/en/blog/pcb-manufacturing-files.html).

The first prototype batch is usually 5–10 boards. That is enough to use several boards in different tests and to keep work going if a board gets damaged.

## 6. Testing and verification

When the prototype arrives, the first job is to bring the board up in a controlled way:

1. Power is applied from a current-limited power supply, and the current drawn at first power-up is monitored.
2. All voltage rails are measured; the regulator outputs and their ripple are checked.
3. The microcontroller is programmed and the peripherals are tested one by one.
4. Functional tests are run against the items in the requirements document, and the results are recorded.
5. Temperature, long-term operation and, if needed, EMC pre-compliance tests are carried out.

It is normal for the first prototype to need a few minor fixes. The goal is to close them out in the second revision and move into mass production with a clean design.

## 7. Moving to mass production

A board that works as a prototype must also be manufacturable without problems in mass production. At this stage:

- Manufacturability (DFM) and testability (DFT) are reviewed one last time.
- A test procedure is prepared for production testing, along with a test fixture if needed.
- The bill of materials is streamlined for cost and supply.
- Assembly drawings, firmware programming instructions and revision records are completed.

A small pre-series run (pilot production) is the safest way to spot issues in the process before a large order.

## What determines the timeline and cost?

| Factor | Impact |
|---|---|
| Clarity of requirements | Ambiguity increases the number of revisions and lengthens the timeline. |
| Board complexity | Part count, layer count and layout time go up. |
| Prototype rounds | Each additional revision means extra manufacturing and test time. |
| Certification | EMC and safety testing require separate planning. |
| Component sourcing | Parts with long lead times drive the schedule. |

## Conclusion

A good electronic board is the sum of clear requirements, the right component selection, careful layout and planned testing. Skipping these steps may seem to save time in the short term, but it usually comes back as an extra prototype round.

At ModWare Technology, we run the [electronics and PCB design](/en/electronics-pcb-design.html), [prototyping and R&D](/en/prototyping-rd.html) and [PCB manufacturing](/en/pcb-manufacturing.html) stages within a single team. Tell us where your project stands, and let's map out the right roadmap for you together.
""",
    ),
    dict(
        tr="pcb-uretimi-icin-gerekli-dosyalar",
        slug="pcb-manufacturing-files",
        baslik="Which files do you need for PCB manufacturing? Gerber, drill, BOM and pick-and-place files",
        title="Files Needed for PCB Manufacturing: Gerber, BOM, CPL | ModWare",
        kategori="PCB manufacturing",
        ikon="box",
        desc="Which files do you need for PCB manufacturing and assembly? What the Gerber layers, drill file, BOM and pick-and-place (CPL) file contain, and common mistakes.",
        ozet="Gerber layers, drill file, BOM and pick-and-place file: what needs to be prepared before sending a PCB to manufacturing, and common mistakes.",
        lede="Sending a PCB to manufacturing requires standard outputs that manufacturers can read, not the design tool's native file. A missing or incorrect file can turn into a delay lasting weeks.",
        ilgili=["pcb-uretimi", "tasarim-incelemesi", "elektronik-kart-tasarimi"],
        diger=["prototip-pcb-maliyetini-dusurme", "pcb-tasarim-incelemesi-sik-yapilan-hatalar", "elektronik-kart-tasarim-sureci"],
        cta="Let's manufacture your PCBs together.",
        urun="PCB manufacturing",
        govde="""
When the PCB design is finished, the board still exists only on the computer. For manufacturing, the design has to be converted into a set of files that production machines can understand. This set falls into two groups: what is needed to manufacture the bare board, and what is needed to place the components on the board (assembly).

> **In short:** The bare board needs Gerber files, a drill file and fabrication notes; assembly needs a bill of materials (BOM), a pick-and-place file (CPL) and an assembly drawing.

## Gerber files

Gerber is the common language of the PCB industry. Each layer is a separate file that describes what the board will look like on that layer. The formats in use today are Extended Gerber (RS-274X) and Gerber X2, which carries the layer information inside the file itself.

| Layer | What is it for? |
|---|---|
| Top and bottom copper | Traces, pads and copper pours |
| Inner copper layers | Inner signal and plane layers on multilayer boards |
| Solder mask | Where the protective coating over the board is left open (pads) |
| Silkscreen | Reference designators, logos and markings |
| Solder paste | Openings of the stencil used in assembly |
| Board outline | The boundary the board is cut along, internal cutouts and slots |

Before sending the files, opening them in a Gerber viewer and checking that all layers are present and correctly aligned catches the most common mistakes up front.

## Drill file

The positions and diameters of the holes are not in the Gerber files; they are usually in a separate drill file in Excellon format.

- **Plated (PTH) and non-plated (NPTH) holes** are usually supplied in separate files. Mounting holes and the holes for some connector pins should be non-plated.
- **Units and number format** (mm or inch, number of decimal places) must match the Gerber files; otherwise the holes end up in the wrong place.
- **Slots** must be clearly defined in the drill file or on the outline layer.

## Fabrication notes

Some information cannot be read from the Gerber files and has to be specified separately. A short fabrication note should include:

- Board thickness (standard 1.6 mm) and material (FR-4, high-Tg if needed)
- Copper thickness (e.g., 35 µm / 1 oz) and layer stackup
- Surface finish (HASL, lead-free HASL or ENIG)
- Solder mask and silkscreen colors
- Special requests such as impedance control, panelization or custom tolerances

## Bill of materials (BOM)

If the board is going to assembly, the most critical file is the bill of materials. A good BOM fully defines a single part on each line:

| Column | Example |
|---|---|
| Reference designators | R1, R4, R7 |
| Quantity | 3 |
| Value | 10 kΩ, 1% |
| Package | 0603 |
| Manufacturer | Yageo |
| Manufacturer part number (MPN) | RC0603FR-0710KL |
| Note | Alternates allowed, do-not-populate (DNP) flag |

A BOM without manufacturer part numbers is left with vague lines such as "10 µF capacitor"; this can lead to parts being bought with the wrong voltage rating or made of the wrong material.

## Pick-and-place file (CPL)

Also known as the position or centroid file, this file gives the location and orientation of every part on the board: reference designator, X and Y coordinates, rotation angle and which side of the board the part is on.

Design tools and pick-and-place machines may use different references for the rotation angle. This is the most common reason polarized parts such as diodes, ICs and electrolytic capacitors are placed backwards. Checking the placement preview prepared by the manufacturer before assembly greatly reduces this risk.

## Assembly drawing and other files

- **Assembly drawing:** A PDF showing component placement and orientation marks; used for manual work and for inspection.
- **Netlist (IPC-D-356):** Helps the manufacturer put the boards through electrical testing.
- **3D model (STEP):** For enclosure and mechanical fit checks.

## Common mistakes

- A missing board outline, or an outline drawn differently on different layers
- Forgetting the solder paste layer
- A drill file in different units from the Gerber files
- BOM reference designators that don't match the PCB, and do-not-populate parts that are not marked
- Wrong rotation angles for polarized parts in the pick-and-place file
- Silkscreen overlapping the pads
- Mixing up files from old and new revisions

## Checklist before you send the files

1. Open all Gerber layers in a viewer; check the layer count and alignment.
2. Verify that the drill file is aligned with the Gerber files and uses the same units.
3. Write the board thickness, copper thickness, surface finish and colors in the fabrication notes.
4. Check that every reference designator in the BOM has a counterpart on the PCB and that every line has a manufacturer part number.
5. In the preview, check the rotation of polarized parts from the pick-and-place file.
6. Add a revision code to the file names and send them all in a single archive.

## Conclusion

A correctly prepared file set is a prerequisite for manufacturing to run quickly and without surprises. In our [PCB manufacturing](/en/pcb-manufacturing.html) service, we check your files before production, determine the right manufacturing options and follow the process through to delivery. If you would also like your design reviewed, take a look at our [design review](/en/design-review.html) service.
""",
    ),
    dict(
        tr="pcb-tasariminda-emc-kurallari",
        slug="pcb-emc-design-rules",
        baslik="EMC in PCB design: 10 rules for preventing noise from the start",
        title="EMC in PCB Design: 10 Rules to Prevent Noise | ModWare",
        kategori="PCB design",
        ikon="wave",
        desc="Passing EMC testing starts on day one of the design: 10 rules for ground planes, current loops, decoupling, switching power stages and connector filtering.",
        ozet="Ground plane, current loops, decoupling, the switching power stage and connector filtering: 10 rules that prevent EMC problems from the start.",
        lede="EMC problems are usually discovered in the test lab, but their causes almost always lie in the initial PCB layout. A board set up correctly from the start costs far less than ferrites and shields added later.",
        ilgili=["elektronik-kart-tasarimi", "tasarim-incelemesi", "prototip-ar-ge"],
        diger=["pcb-tasarim-incelemesi-sik-yapilan-hatalar", "elektronik-kart-tasarim-sureci", "stm32-modbus-rtu-rs485"],
        cta="Let's review your board before it goes to production.",
        urun="Design review",
        govde="""
Electromagnetic compatibility (EMC) means that a device does not emit electromagnetic noise into its surroundings above acceptable limits (emissions) and that it can operate without being affected by the noise around it (immunity). For electronic products sold on the European market, it is part of CE marking and is tested under the EMC Directive.

Fixing EMC after the fact is expensive: it takes extra filters, ferrites, shields and often a new PCB revision. Yet most of the noise can be prevented from the start by following a few basic rules during layout.

> **In short:** Think about the current's return path, keep current loops small, don't split the ground plane, filter noise at its source; and think of the board edges and cables as antennas.

## 1. Every signal has a return path

Current always flows in a loop: wherever it goes, it somehow finds its way back to its source. At high frequencies, the return current flows in the reference plane directly beneath the signal trace, following the path of lowest impedance. That is why there must be a continuous ground plane under fast signals. A slot or void in the plane forces the return current to take a detour; the loop grows and emissions increase.

## 2. Keep current loops small

The noise a loop radiates increases with the loop area and with how fast the current changes. Placing the source and the load close together and keeping the signal path and the return path close to each other reduces the loop area. This rule reduces both emissions and noise pickup from outside.

## 3. Minimize the "hot loop" in the switching power stage

In switching regulators such as a buck converter, the most critical area is the loop between the input capacitor and the switching devices. The current in this loop changes very quickly, making it one of the strongest noise sources on the board.

- Place the input capacitors right next to the switching devices, with the shortest possible connections.
- Make the copper area of the switch node (SW) large enough to carry the current, but no larger than necessary.
- Route the feedback trace away from the inductor and the switch node.
- Start from the example layout recommended by the regulator manufacturer; these recommendations are usually layouts that have been measured and proven.

## 4. Place decoupling capacitors correctly

Decoupling capacitors supply the instantaneous current demand of ICs locally. To be effective, they must be placed as close as possible to the supply pin, and their ground connection must go directly to the ground plane through a short via. A long, thin connection narrows the frequency range over which the capacitor is effective. Typically, a 100 nF capacitor is used on each supply pin, plus one or more larger-value capacitors on each supply rail.

## 5. Choose the layer stackup with EMC in mind

As the layer count goes up, it becomes easier to place a reference plane right next to each signal layer. On a four-layer board, a stackup of signal, ground, power and signal layers is a common and solid starting point. On two-layer boards, one side should be devoted to a ground pour that is as continuous as possible, and traces should be planned so that they don't break up this plane. The right layer count is determined by weighing circuit density, speed and cost together.

## 6. Cables are antennas: filter at the connectors

Every cable leaving the board is an antenna that can both radiate and pick up noise. Noise has to be stopped before it reaches the cable connector:

- Add a ferrite, an RC filter or a common-mode choke to communication and power lines at the connector entry.
- For ESD and voltage transients, place TVS diodes right next to the connector, with a short ground connection.
- Keep fast signals and clock lines away from connectors and the board edge.

## 7. Slow down clocks and fast signals

The frequency content of the noise is determined more by the edge rate than by the signal frequency. Edges that are faster than necessary generate high-frequency harmonics.

- Place the crystal right next to the microcontroller, keep its traces short and don't route other signals underneath it.
- Soften the edges by adding 22–33 Ω series resistors to fast outputs.
- Keep the pin speed on the microcontroller (the GPIO speed setting on STM32) at the lowest setting that does the job.

## 8. Separate analog and digital sections by placement

Splitting the ground plane into analog and digital sections often creates new return-path problems instead of solving the problem. The safer approach is to use a single, continuous ground plane and separate the sections by placement: group sensitive analog circuits in one area and noisy digital and power circuits in another, and don't route fast signals between them.

## 9. Remove floating copper and stitch grounds together

Floating copper islands that are not connected to ground can act as antennas; they should either be removed or connected to ground. Ground areas on different layers should be tied together with closely spaced vias, especially along the board edges and near the points where fast signals change layers.

## 10. Measure early: pre-compliance testing

Simple measurements made before lab testing greatly reduce surprises. Noise sources on the board can be located with near-field probes and a spectrum analyzer, while noise radiated from cables can be measured with a common-mode current probe. A problem found at the prototype stage is much cheaper to fix than one found at the product stage.

## EMC checklist

- Is there a continuous reference plane under fast signals?
- Is the input loop of the switching power stage as small as possible?
- Are the decoupling capacitors close to the pins and connected directly to the plane?
- Do the connectors have filtering and ESD protection?
- Are the crystal and clock lines short and well protected?
- Are there any floating copper areas or split planes?

## Conclusion

EMC is not a feature added at the end of the design; it is the result of decisions made from the first day of layout. These rules won't solve every problem on their own, but they prevent most problems before you ever get to the lab.

In our [electronics and PCB design](/en/electronics-pcb-design.html) projects, we treat EMC as part of the layout from the very beginning. If you already have a finished design, we can go over the risks together in a [design review](/en/design-review.html) before it goes to production.
""",
    ),
]
