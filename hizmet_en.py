"""Hizmet sayfalarının İngilizce metinleri (/en/).

seo_uret.py'deki HIZMETLER, SAYFALAR ve HUB ile hizmet sayfası şablonundaki sabit metinlerin karşılığı;
sıralama ve yapı Türkçe verilerle aynıdır. Çeviri kuralları: ceviri-rehberi.md.
Başlıklar (h1–h3, kart başlıkları) cümle düzeninde yazılır; büyük harfe çevirmeyi üretici yapar.
Sekme başlıkları (title) bu işlemden geçmediği için Türkçedeki gibi her kelimesi büyük yazılmıştır.
"""

# tr: Türkçe hizmetin slug'ı (eşleştirme anahtarı); slug: /en/ altındaki adres; urun: İngilizce teklif formundaki seçenek değeri
HIZMETLER_EN = [
    dict(tr="elektronik-kart-tasarimi", slug="electronics-pcb-design", ad="Electronics and hardware design", ikon="chip",
         urun="Custom hardware design",
         ozet="From requirements to schematic, from PCB design to prototype: control, power, sensor and communication boards."),
    dict(tr="pcb-uretimi", slug="pcb-manufacturing", ad="PCB manufacturing", ikon="box", urun="PCB manufacturing",
         ozet="From file check to delivery: prototype and small-batch printed circuit board manufacturing."),
    dict(tr="gomulu-yazilim", slug="embedded-software", ad="Embedded software development", ikon="code",
         urun="Embedded software",
         ozet="Embedded software tailored to your hardware and reliable in the field: written from scratch, or your existing software improved."),
    dict(tr="tasarim-incelemesi", slug="design-review", ad="Design review", ikon="eye", urun="Design review",
         ozet="We review your schematic and PCB before they go into production and report errors and risks."),
    dict(tr="prototip-ar-ge", slug="prototyping-rd", ad="Prototyping and R&D", ikon="flask", urun="Custom hardware design",
         ozet="From idea to working prototype and from prototype to production, with a test plan and documentation."),
]

SAYFALAR_EN = {
    "elektronik-kart-tasarimi": dict(
        title="Electronics, Hardware and PCB Design | ModWare Technology",
        desc="Electronics, hardware and PCB design by one team: requirements, schematic, multilayer PCB, prototype, DFM checks, manufacturing files. İzmit, Kocaeli, Türkiye.",
        eyebrow="Service · Hardware and PCB design",
        h1="Electronics, hardware and PCB design",
        lede="We turn your idea into a working circuit board: we define the requirements with you, design the schematic and the multilayer PCB, then test the prototype and prepare it for production. If you already have a schematic, we also take on the PCB design on its own.",
        kapsam_baslik="What boards do we design?",
        kapsam=[
            ("chip", "Microcontroller control boards", "STM32-based control and interface boards: display, encoder, buttons, LEDs and non-volatile event logging."),
            ("bolt", "Power boards", "For 12–48 V DC systems: buck and buck-boost converters, eFuse, reverse-polarity protection and power distribution."),
            ("gauge", "Measurement and sensor boards", "Current, voltage, temperature and pressure measurement; signal conditioning and calibration-friendly design."),
            ("wave", "Communication boards", "RS-485 (Modbus RTU), isolated USB, LoRa, I²C, SPI and UART interfaces."),
            ("layers", "Modular systems", "Carrier board and plug-in module architecture; board-to-board connections and mechanical fit."),
            ("shield", "Field-ready design", "Protection against reverse connection, short circuits, overvoltage and ESD; a layout that considers EMC/EMI from the start."),
        ],
        kapsam2=dict(eyebrow="PCB design", baslik="What do we cover in PCB design?", kartlar=[
            ("layers", "Multilayer boards", "We set the layer count based on what the board needs and plan the stackup and ground planes for signal integrity."),
            ("bolt", "High current and voltage", "Copper pours for power paths, current capacity and voltage clearances per IPC-2221."),
            ("wave", "Noise and EMC", "A layout that keeps switching loops small; separate analog, digital and power areas."),
            ("chip", "Fine-pitch ICs", "QFN and TSSOP packages with 0.5 mm pitch, thermal pads and via placement."),
            ("list", "Manufacturability (DFM)", "Trace widths, spacing and via sizes within manufacturing rules; design rule check (DRC)."),
            ("box", "Mechanical fit", "Enclosure, connector and mounting hole positions; height and interference checks with the 3D model."),
        ]),
        surec_baslik="Four steps from idea to production",
        surec=[
            ("Requirements", "Together we define what the board will do, where it will operate and how many units will be made."),
            ("Schematic and calculations", "Component selection, power and thermal calculations, simulation if needed; we present the schematic for your approval step by step."),
            ("PCB and prototype", "Multilayer PCB layout, manufacturing files and testing of the prototype boards."),
            ("Transition to production", "Cost and sourcing checks, assembly and test documents; a package ready for series production."),
        ],
        teslim=[
            ("doc", "Design files", "Schematic and PCB design files, including the library parts."),
            ("box", "Manufacturing package", "Gerber, drill, bill of materials (BOM) and pick-and-place (CPL) files, plus the assembly drawing."),
            ("list", "Design report", "Calculations, component selection rationale, test plan and open risks."),
        ],
        sss=[
            ("I only have an idea. Can we start?", "Yes. In the discovery phase we put your needs in writing together and derive the technical requirements; the design starts from that document."),
            ("Can you improve our existing board?", "Yes. We review your schematic and PCB and can revise the design, reduce cost, replace parts or add new features."),
            ("Can you do just the PCB design?", "Yes. We review your schematic, report anything missing or risky, then start the PCB layout. We decide the layer count together based on current, noise and cost."),
            ("How long does the design take?", "It depends on the scope. In the quote we break the work into phases and state the duration and deliverables of each phase separately."),
            ("What about files and confidentiality?", "We deliver the schematic and PCB design files together with the manufacturing files. Confidentiality and intellectual property terms are set out in writing at the start of the project."),
        ],
        cta="Let's design your board together.",
    ),
    "pcb-uretimi": dict(
        title="PCB Manufacturing for Prototypes and Small Batches | ModWare",
        desc="PCB manufacturing service from file check to delivery: DFM check, stackup and surface finish selection, prototypes and small batches. İzmit, Kocaeli, Türkiye.",
        eyebrow="Service · PCB manufacturing",
        h1="PCB manufacturing",
        lede="We take care of manufacturing your printed circuit boards, from prototypes to small batches: we check your files, choose the right manufacturing options, follow the process end to end and deliver your boards.",
        kapsam_baslik="What do we handle in manufacturing?",
        kapsam=[
            ("list", "File check (DFM)", "We check your Gerber and drill files and fix any issues before they reach production."),
            ("layers", "The right manufacturing options", "We choose the stackup, copper thickness and surface finish (HASL, ENIG) to suit the job and the budget."),
            ("box", "End-to-end process", "Quote, production tracking and delivery in one place; we are your single point of contact."),
            ("cycle", "From prototype to small batch", "We start with a few prototypes and increase quantities once the design is verified."),
            ("doc", "Easy repeat orders", "We keep the verified files and manufacturing settings and repeat your next order with the same settings."),
            ("chip", "Combined with design", "If we also design the board, the files come out ready for manufacturing; design and manufacturing are handled in one place."),
        ],
        surec_baslik="From files to delivery",
        surec=[
            ("Files", "Send us the files for your own design, or design the board with us."),
            ("Check and quote", "Based on the DFM check and the manufacturing options, we work out cost and lead time."),
            ("Manufacturing", "Once you approve, we start manufacturing and follow the process end to end."),
            ("Delivery", "We deliver your boards and hand over the verified file package for your next order."),
        ],
        teslim=[
            ("box", "Manufactured PCBs", "Printed circuit boards made in the agreed quantity with the agreed options."),
            ("list", "Pre-production check note", "Issues found in the DFM check and the corrections made."),
            ("doc", "Reorder package", "Verified files and manufacturing settings for the next production run."),
        ],
        sss=[
            ("Can I order small quantities?", "Yes. You can start with a few units for prototyping and move to a small batch once the design is verified."),
            ("My design was done elsewhere. Can I order just the manufacturing?", "Yes. We check your files before manufacturing, suggest any corrections needed and take care of the manufacturing."),
            ("Why do surface finish and stackup matter?", "With fine-pitch ICs, a flat surface (ENIG) makes soldering easier; the stackup affects noise and heat. We make the choice together based on the job."),
            ("How long does manufacturing take?", "It depends on quantity and options; our quote states the manufacturing and delivery times separately."),
        ],
        cta="Let's manufacture your PCB together.",
    ),
    "gomulu-yazilim": dict(
        title="Embedded Software Development and STM32 Firmware | ModWare",
        desc="Embedded software for microcontrollers: firmware from scratch or improvements to existing code. STM32, Modbus RTU, RS-485, USB, LoRa. İzmit, Kocaeli, Türkiye.",
        eyebrow="Service · Embedded software",
        h1="Embedded software development",
        lede="We develop embedded software for your microcontroller-based products together with the team that designs the hardware. We write it from scratch for your new product, fix bugs in your existing software and add new features to it.",
        kapsam_baslik="What do we do in embedded software?",
        kapsam=[
            ("chip", "STM32 firmware", "Peripheral drivers, timers, ADC/DAC and low-power modes for STM32 microcontrollers."),
            ("wave", "Communication protocols", "Modbus RTU, RS-485, UART, I²C, SPI, USB and LoRa; connection to PCs, PLCs and SCADA systems."),
            ("shield", "Fault and safety logic", "Watchdog, power-on self-tests, fault logs and safe shutdown scenarios."),
            ("gauge", "Measurement and control", "Sensor reading, filtering, calibration coefficients and closed-loop control."),
            ("eye", "User interface", "On-site monitoring and settings menus with a display, encoder, buttons and LEDs."),
            ("cycle", "Improving existing software", "We fix bugs in your existing software, add new features or port it to new hardware."),
        ],
        surec_baslik="From architecture to delivery",
        surec=[
            ("Architecture", "We define the tasks, timing, communication and fault scenarios."),
            ("Drivers", "Hardware layer and peripherals; basic tests as soon as the board arrives."),
            ("Application", "Application logic, communication and interface; we share interim releases for your approval."),
            ("Testing and delivery", "Scenario tests, flashable firmware and user documentation."),
        ],
        teslim=[
            ("list", "Test results", "Scenario test results and release notes."),
            ("box", "Flashable firmware", "Compiled firmware and instructions for loading it onto the board."),
            ("doc", "Communication documentation", "A user guide and, for example, the Modbus register map."),
        ],
        sss=[
            ("Can we work with you on software only?", "Yes. We can develop software for your existing board or improve the software you already have."),
            ("Which microcontrollers do you work with?", "We mainly work with the STM32 family; depending on the project's needs, we also consider other families."),
            ("Is the source code delivered to us?", "Our standard deliverables are the flashable firmware and user documentation. Source code delivery and license terms are set separately for each project."),
            ("Can it communicate with a PLC or SCADA system?", "Yes. It connects to PLC, SCADA and PC software over industrial protocols such as Modbus RTU (RS-485)."),
        ],
        cta="Let's write the software for your board together.",
    ),
    "tasarim-incelemesi": dict(
        title="Schematic and PCB Design Review, Pre-production Check | ModWare",
        desc="We review your schematic and PCB design before production: a prioritized report on errors, risks, manufacturability and cost. İzmit, Kocaeli, Türkiye.",
        eyebrow="Service · Design review",
        h1="Schematic and PCB design review",
        lede="Before your board goes into production, we review your schematic and PCB design as a second pair of eyes. We deliver the errors, risks and suggested improvements in a prioritized report and support you with the fixes.",
        kapsam_baslik="What do we review?",
        kapsam=[
            ("chip", "Schematic check", "Connection errors, missing pull-up and pull-down resistors, wrong values, pin mismatches and electrical rules."),
            ("bolt", "Power and protection", "Voltage, current and thermal margins; protection against reverse connection, short circuits and overvoltage."),
            ("layers", "PCB layout", "Current paths, ground plane, switching loops, trace widths and voltage clearances."),
            ("list", "Manufacturability (DFM)", "Manufacturing rules, via and pad sizes, surface finish and stackup selection."),
            ("box", "Parts and cost", "Hard-to-find or risky parts, suggested alternates and cost reduction opportunities."),
            ("doc", "File consistency", "Whether the bill of materials, manufacturing files and assembly drawings match the schematic."),
        ],
        surec_baslik="From files to report",
        surec=[
            ("Files", "Send your schematic and PCB files, or PDF and Gerber outputs."),
            ("Scope and quote", "We discuss the board's purpose and your concerns, then set the scope and duration of the review."),
            ("Review", "We review the schematic, PCB and manufacturing files with a checklist and calculations."),
            ("Report and support", "We report the findings in order of importance and go over the fixes together."),
        ],
        teslim=[
            ("list", "Prioritized findings report", "Location, risk and suggested fix for each finding, ordered from critical issues to suggestions."),
            ("doc", "Annotated outputs", "Schematic and PCB images with the problem areas marked."),
            ("eye", "Review meeting", "A short meeting where we go through the report together."),
        ],
        sss=[
            ("Which files do I need to send?", "Schematic and PCB design files are best; otherwise we can also review a PDF of the schematic, the Gerber files and the bill of materials."),
            ("Does the board have to be designed by you?", "No. We review designs by another team or by your own team; if you like, we can also make the fixes."),
            ("How long does a review take?", "It depends on the size of the board and the scope; our quote states the duration and delivery date."),
            ("How do you keep my files confidential?", "We use your files only for the review; if you wish, we sign a non-disclosure agreement before the review."),
        ],
        cta="Let's review your board before it goes into production.",
    ),
    "prototip-ar-ge": dict(
        title="Prototype Development and Electronics R&D | ModWare Technology",
        desc="Electronics R&D from idea to working prototype and on to production: requirements, design, test plan and documentation by one team. İzmit, Kocaeli, Türkiye.",
        eyebrow="Service · R&D",
        h1="Prototype development and electronics R&D",
        lede="We turn a new electronic product idea into a working, manufacturable prototype. We run hardware, embedded software and mechanics in the same team and document every phase with measurable deliverables.",
        kapsam_baslik="What do we take on in R&D?",
        kapsam=[
            ("flask", "Feasibility and proof of concept", "We test whether the idea is technically feasible with a quick proof of concept (POC)."),
            ("list", "Requirements and architecture", "We document what the product will do, its limits and the interfaces between boards."),
            ("chip", "Hardware and software", "Circuit boards, embedded software and, if needed, a PC interface."),
            ("box", "Mechanics and enclosure", "Board placement, enclosure, connectors and thermal management, together with mechanical engineering."),
            ("gauge", "Test plan and verification", "A measurement method and acceptance criterion for each requirement; prototype testing."),
            ("cycle", "Transition to production", "Cost reduction, sourcing, assembly and test documentation."),
        ],
        surec_baslik="Four phases with measurable deliverables",
        surec=[
            ("Discovery and scope", "We clarify needs and success criteria and derive the technical requirements."),
            ("Design and verification", "Schematic, PCB and software architecture; verification through calculations and interim deliveries."),
            ("Prototype and testing", "We build the prototype, measure it against the test plan and improve it."),
            ("Transition to production", "Manufacturability, sourcing and test processes; documentation."),
        ],
        teslim=[
            ("doc", "Requirements and design documents", "Product definition, architecture, calculations and the reasoning behind decisions."),
            ("chip", "Working prototype", "A testable prototype with its hardware and software."),
            ("list", "Test plan and results", "Measurement methods, acceptance criteria and a results report."),
        ],
        sss=[
            ("My idea is not clear yet. Where should I start?", "We start with a discovery meeting and clarify the need, operating conditions and target cost together."),
            ("How many stages does a prototype take?", "Usually a proof of concept followed by one or two prototype revisions; at the end of each stage we report what we learned."),
            ("How do we move to series production?", "Once the prototype is verified, we organize the cost, sourcing and test processes and prepare the manufacturing files and assembly instructions."),
        ],
        cta="Let's turn your idea into a prototype.",
    ),
}

HUB_EN = dict(
    title="Services: Electronics Design, PCB and Embedded Software | ModWare",
    desc="Electronics and PCB design, PCB manufacturing, embedded software, design review, prototyping and R&D. From İzmit, Kocaeli, for clients in Türkiye and abroad.",
    eyebrow="Services",
    h1="From electronics design to production",
    lede="We bring every step an electronic product needs together in one team. Choose the service closest to your needs, or tell us about your project directly.",
)

# Hizmet sayfası şablonundaki ve hizmetler sayfasındaki (hub_sayfasi) sabit metinler; anahtar Türkçe metnin kendisidir
METIN_EN = {
    "Kapsam": "Scope",
    "Süreç": "Process",
    "Teslimatlar": "Deliverables",
    "Projenin sonunda elinizde olanlar": "What you get at the end of the project",
    "Örnek": "Example",
    "Ürünleri inceleyin": "Explore products",
    "Sık sorulanlar": "FAQ",
    "Merak edilenler": "Common questions",
    "Diğer hizmetler": "Other services",
    "Tek ekipte, uçtan uca": "One team, end to end",
    "Hizmeti inceleyin": "Learn more",
    "Projenizi kısaca anlatın; kapsam, süre ve tahmini bütçeyle dönelim.":
        "Tell us briefly about your project; we'll get back to you with the scope, timeline and an estimated budget.",
    "Teklif Al": "Get a Quote",
    "Tüm hizmetler": "All services",
    "Ne yapıyoruz?": "What we do",
    "Hizmetlerimiz": "Our services",
    "Fikirden üretime tek ekip": "One team from idea to production",
    "Projenizi birlikte geliştirelim.": "Let's develop your project together.",
    # hub_sayfasi() süreç adımları
    "Keşif ve kapsam": "Discovery and scope",
    "İhtiyaçları ve başarı kriterlerini netleştirir, teknik gereksinimleri çıkarırız.":
        "We clarify needs and success criteria and derive the technical requirements.",
    "Tasarım ve doğrulama": "Design and verification",
    "Şematik, PCB ve yazılım mimarisi; hesap ve ara teslimlerle doğrulama.":
        "Schematic, PCB and software architecture; verification through calculations and interim deliveries.",
    "Prototip ve test": "Prototype and testing",
    "Prototipi üretir, ölçer ve iyileştiririz.": "We build the prototype, measure it and improve it.",
    "Üretime geçiş": "Transition to production",
    "PCB üretimi, tedarik ve dokümantasyon.": "PCB manufacturing, sourcing and documentation.",
}
