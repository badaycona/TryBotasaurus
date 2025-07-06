class HardWareComponent:
    def __init__(self, name=None, cost=None):
        self.name = name if name else 'Unknown'
        self.cost = cost if cost is not None else 0

class CPU(HardWareComponent):
    def __init__(self, name=None, core_count=None, socket=None, tdp=None, core_clock=None, boost_clock=None, graphics=None, smt=None, price=None):
        super().__init__(name, price)
        self.core_count = core_count if core_count is not None else 0
        self.core_clock = core_clock if core_clock is not None else 0
        self.boost_clock = boost_clock if boost_clock is not None else 0
        self.socket = socket if socket else 'Unknown'
        self.tdp = tdp if tdp is not None else 0
        self.graphics = graphics if graphics else 'Unknown'
        self.smt = smt if smt else 'Unknown'
    def __str__(self):
        return f'CPU(name={self.name}, cores={self.core_count}, clock={self.core_clock}, socket={self.socket}, tdp={self.tdp})'

class GPU(HardWareComponent):
    def __init__(self, name=None, memory=None, chipset=None, tdp=None, core_clock=None, boost_clock=None, length=None, color=None, price=None):
        super().__init__(name, price)
        self.vram = memory if memory is not None else 0
        self.chipset = chipset if chipset else 'Unknown'
        self.tdp = tdp if tdp is not None else 0
        self.core_clock = core_clock if core_clock is not None else 0
        self.boost_clock = boost_clock if boost_clock is not None else 0
        self.length = length if length is not None else 0
        self.color = color if color else 'Unknown'
        self.price = price if price is not None else 0

    def __str__(self):
        return f'GPU(model={self.name}, vram={self.vram}, chip_set={self.chipset}, tdp={self.tdp}, core_clock={self.core_clock}, boost_clock={self.boost_clock}, length={self.length}, color={self.color})'

class RAM:
    def __init__(self, name=None, capacity=None, speed=None, ram_type=None, color=None, price=None, modules=None, price_per_gb=None, first_word_latency=None, cas_latency=None):
        self.name = name if name else 'Unknown'
        self.capacity = capacity if capacity is not None else 0
        self.ram_type = ram_type if ram_type else 'Unknown'
        self.speed = speed if speed is not None else 0
        self.cost = price if price is not None else 0
        self.modules = modules if modules is not None else 1
        self.color = color if color else 'Unknown'
        self.price_per_gb = price_per_gb if price_per_gb is not None else 0
        self.first_word_latency = first_word_latency if first_word_latency is not None else 0
        self.cas_latency = cas_latency if cas_latency is not None else 0

    def __str__(self):
        return f'RAM(name={self.name}, capacity={self.capacity}, ram_type={self.ram_type}, speed={self.speed}, cost={self.cost})'

class Mainboard:
    def __init__(self, name=None, socket=None, form_factor=None, chipset=None, ram_type=None, pcie_version=None, max_memory=None, memory_slots=None, color=None, price=None):
        self.name = name if name else 'Unknown'
        self.socket = socket if socket else 'Unknown'
        self.form_factor = form_factor if form_factor else 'Unknown'
        self.chipset = chipset if chipset else 'Unknown'
        self.ram_type = ram_type if ram_type else 'Unknown'
        self.max_memory = max_memory if max_memory is not None else 0
        self.memory_slots = memory_slots if memory_slots is not None else 0
        self.pcie_version = pcie_version if pcie_version else 'Unknown'
        self.color = color if color else 'Unknown'
        self.price = price if price is not None else 0
    def __str__(self):
        return f'Mainboard(name={self.name}, socket={self.socket}, form_factor={self.form_factor}, chipset={self.chipset}, ram_type={self.ram_type}, max_memory={self.max_memory}, memory_slots={self.memory_slots}, pcie_version={self.pcie_version}, color={self.color}, price={self.price})'

class PSU:
    def __init__(self, name=None, wattage=None, efficiency=None, color=None, price=None, type=None, modular=None):
        self.name = name if name else 'Unknown'
        self.wattage = wattage if wattage is not None else 0
        self.efficiency = efficiency if efficiency else 'Unknown'
        self.color = color if color else 'Unknown'
        self.price = price if price is not None else 0
        self.type = type if type else 'Unknown'
        self.modular = modular if modular is not None else False
    def __str__(self):
        return f'PSU(name={self.name}, wattage={self.wattage}, efficiency={self.efficiency}, color={self.color}, price={self.price}, type={self.type}, modular={self.modular})'

class OS:
    def __init__(self, name=None, price=None, mode=None, max_memory=None):
        self.name = name if name else 'Unknown'
        self.price = price if price is not None else 0
        self.mode = mode if mode else 'Unknown'
        self.max_memory = max_memory if max_memory is not None else 0
    def __str__(self):
        return f'OS(name={self.name}, price={self.price}, mode={self.mode}, max_memory={self.max_memory})'