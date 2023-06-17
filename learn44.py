class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class VoltageResistor(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


class BoundedResistance(VoltageResistor):
    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f'ohms must be > 0; got {ohms}')
        else:
            self._ohms = ohms


r1 = VoltageResistor(1e3)
print(f'Before: {r1.current:.2f} amps')
r1.voltage = 10
print(f'After: {r1.current:.2f} amps')


r3 = BoundedResistance(-5)
r3.ohms = 10
