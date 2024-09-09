
class time:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} second'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'time({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'time') -> bool:
        if not isinstance(other, time):
            raise TypeError(f'Cannot compare time to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'time') -> bool:
        if not isinstance(other, time):
            raise TypeError(f'Cannot compare time to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'time') -> bool:
        if not isinstance(other, time):
            raise TypeError(f'Cannot compare time to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'time') -> bool:
        if not isinstance(other, time):
            raise TypeError(f'Cannot compare time to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'time') -> 'time':
        if not isinstance(other, time):
            raise TypeError(f'Cannot add time to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return time(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'time') -> 'time':
        if not isinstance(other, time):
            raise TypeError(f'Cannot add time to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'time') -> 'time':
        if not isinstance(other, time):
            raise TypeError(f'Cannot add time to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return time(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'time') -> 'time':
        if not isinstance(other, time):
            raise TypeError(f'Cannot add time to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'time':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply time by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'time':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide time by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'time':
        return time(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'time':
        return time(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'time':
        return time(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'time',
        
    )):
        if isinstance(value, (float, int)):
            return time(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, time):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        else:
            raise TypeError(f'Cannot divide time by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
        'speed',
        'acceleration',
        'power',
        'force',
    )):
        if isinstance(value, (float, int)):
            return time(self.value * value, self.multiplier, self.offset)
        
        elif isinstance(value, speed):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return length(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, acceleration):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return speed(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, power):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return energy(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, force):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return momentum(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        else:
            raise TypeError(f'Cannot multiply time by {type(value)}')

    

    

    def cast_to_other(self, other: 'time'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return time(base_value / multiplier - offset, multiplier, offset)

class length:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} metre'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'length({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'length') -> bool:
        if not isinstance(other, length):
            raise TypeError(f'Cannot compare length to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'length') -> bool:
        if not isinstance(other, length):
            raise TypeError(f'Cannot compare length to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'length') -> bool:
        if not isinstance(other, length):
            raise TypeError(f'Cannot compare length to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'length') -> bool:
        if not isinstance(other, length):
            raise TypeError(f'Cannot compare length to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'length') -> 'length':
        if not isinstance(other, length):
            raise TypeError(f'Cannot add length to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return length(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'length') -> 'length':
        if not isinstance(other, length):
            raise TypeError(f'Cannot add length to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'length') -> 'length':
        if not isinstance(other, length):
            raise TypeError(f'Cannot add length to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return length(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'length') -> 'length':
        if not isinstance(other, length):
            raise TypeError(f'Cannot add length to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'length':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply length by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'length':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide length by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'length':
        return length(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'length':
        return length(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'length':
        return length(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'length',
        
        'speed',
        'time',
    )):
        if isinstance(value, (float, int)):
            return length(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, length):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        elif isinstance(value,speed):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return time(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,time):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return speed(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        else:
            raise TypeError(f'Cannot divide length by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
        'length',
        'force',
    )):
        if isinstance(value, (float, int)):
            return length(self.value * value, self.multiplier, self.offset)
        
        elif isinstance(value, length):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return area(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, force):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return energy(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        else:
            raise TypeError(f'Cannot multiply length by {type(value)}')

    

    
    def square(self):
        v1 = self.cast_to_values(self.multiplier)
        return area(v1.value ** 2, v1.multiplier ** 2)
    

    def cast_to_other(self, other: 'length'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return length(base_value / multiplier - offset, multiplier, offset)

class mass:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} kilogram'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'mass({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'mass') -> bool:
        if not isinstance(other, mass):
            raise TypeError(f'Cannot compare mass to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'mass') -> bool:
        if not isinstance(other, mass):
            raise TypeError(f'Cannot compare mass to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'mass') -> bool:
        if not isinstance(other, mass):
            raise TypeError(f'Cannot compare mass to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'mass') -> bool:
        if not isinstance(other, mass):
            raise TypeError(f'Cannot compare mass to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'mass') -> 'mass':
        if not isinstance(other, mass):
            raise TypeError(f'Cannot add mass to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return mass(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'mass') -> 'mass':
        if not isinstance(other, mass):
            raise TypeError(f'Cannot add mass to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'mass') -> 'mass':
        if not isinstance(other, mass):
            raise TypeError(f'Cannot add mass to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return mass(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'mass') -> 'mass':
        if not isinstance(other, mass):
            raise TypeError(f'Cannot add mass to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'mass':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply mass by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'mass':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide mass by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'mass':
        return mass(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'mass':
        return mass(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'mass':
        return mass(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'mass',
        
    )):
        if isinstance(value, (float, int)):
            return mass(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, mass):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        else:
            raise TypeError(f'Cannot divide mass by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
        'acceleration',
        'speed',
    )):
        if isinstance(value, (float, int)):
            return mass(self.value * value, self.multiplier, self.offset)
        
        elif isinstance(value, acceleration):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return force(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, speed):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return momentum(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        else:
            raise TypeError(f'Cannot multiply mass by {type(value)}')

    

    

    def cast_to_other(self, other: 'mass'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return mass(base_value / multiplier - offset, multiplier, offset)

class temperature:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} Kelvin'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'temperature({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'temperature') -> bool:
        if not isinstance(other, temperature):
            raise TypeError(f'Cannot compare temperature to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'temperature') -> bool:
        if not isinstance(other, temperature):
            raise TypeError(f'Cannot compare temperature to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'temperature') -> bool:
        if not isinstance(other, temperature):
            raise TypeError(f'Cannot compare temperature to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'temperature') -> bool:
        if not isinstance(other, temperature):
            raise TypeError(f'Cannot compare temperature to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'temperature') -> 'temperature':
        if not isinstance(other, temperature):
            raise TypeError(f'Cannot add temperature to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return temperature(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'temperature') -> 'temperature':
        if not isinstance(other, temperature):
            raise TypeError(f'Cannot add temperature to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'temperature') -> 'temperature':
        if not isinstance(other, temperature):
            raise TypeError(f'Cannot add temperature to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return temperature(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'temperature') -> 'temperature':
        if not isinstance(other, temperature):
            raise TypeError(f'Cannot add temperature to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'temperature':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply temperature by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'temperature':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide temperature by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'temperature':
        return temperature(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'temperature':
        return temperature(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'temperature':
        return temperature(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'temperature',
        
    )):
        if isinstance(value, (float, int)):
            return temperature(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, temperature):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        else:
            raise TypeError(f'Cannot divide temperature by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
    )):
        if isinstance(value, (float, int)):
            return temperature(self.value * value, self.multiplier, self.offset)
        
        else:
            raise TypeError(f'Cannot multiply temperature by {type(value)}')

    

    

    def cast_to_other(self, other: 'temperature'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return temperature(base_value / multiplier - offset, multiplier, offset)

class amount:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} things'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'amount({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'amount') -> bool:
        if not isinstance(other, amount):
            raise TypeError(f'Cannot compare amount to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'amount') -> bool:
        if not isinstance(other, amount):
            raise TypeError(f'Cannot compare amount to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'amount') -> bool:
        if not isinstance(other, amount):
            raise TypeError(f'Cannot compare amount to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'amount') -> bool:
        if not isinstance(other, amount):
            raise TypeError(f'Cannot compare amount to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'amount') -> 'amount':
        if not isinstance(other, amount):
            raise TypeError(f'Cannot add amount to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return amount(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'amount') -> 'amount':
        if not isinstance(other, amount):
            raise TypeError(f'Cannot add amount to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'amount') -> 'amount':
        if not isinstance(other, amount):
            raise TypeError(f'Cannot add amount to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return amount(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'amount') -> 'amount':
        if not isinstance(other, amount):
            raise TypeError(f'Cannot add amount to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'amount':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply amount by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'amount':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide amount by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'amount':
        return amount(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'amount':
        return amount(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'amount':
        return amount(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'amount',
        
    )):
        if isinstance(value, (float, int)):
            return amount(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, amount):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        else:
            raise TypeError(f'Cannot divide amount by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
    )):
        if isinstance(value, (float, int)):
            return amount(self.value * value, self.multiplier, self.offset)
        
        else:
            raise TypeError(f'Cannot multiply amount by {type(value)}')

    

    

    def cast_to_other(self, other: 'amount'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return amount(base_value / multiplier - offset, multiplier, offset)

class electric_current:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} Ampere'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'electric_current({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'electric_current') -> bool:
        if not isinstance(other, electric_current):
            raise TypeError(f'Cannot compare electric_current to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'electric_current') -> bool:
        if not isinstance(other, electric_current):
            raise TypeError(f'Cannot compare electric_current to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'electric_current') -> bool:
        if not isinstance(other, electric_current):
            raise TypeError(f'Cannot compare electric_current to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'electric_current') -> bool:
        if not isinstance(other, electric_current):
            raise TypeError(f'Cannot compare electric_current to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'electric_current') -> 'electric_current':
        if not isinstance(other, electric_current):
            raise TypeError(f'Cannot add electric_current to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return electric_current(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'electric_current') -> 'electric_current':
        if not isinstance(other, electric_current):
            raise TypeError(f'Cannot add electric_current to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'electric_current') -> 'electric_current':
        if not isinstance(other, electric_current):
            raise TypeError(f'Cannot add electric_current to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return electric_current(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'electric_current') -> 'electric_current':
        if not isinstance(other, electric_current):
            raise TypeError(f'Cannot add electric_current to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'electric_current':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply electric_current by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'electric_current':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide electric_current by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'electric_current':
        return electric_current(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'electric_current':
        return electric_current(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'electric_current':
        return electric_current(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'electric_current',
        
    )):
        if isinstance(value, (float, int)):
            return electric_current(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, electric_current):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        else:
            raise TypeError(f'Cannot divide electric_current by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
    )):
        if isinstance(value, (float, int)):
            return electric_current(self.value * value, self.multiplier, self.offset)
        
        else:
            raise TypeError(f'Cannot multiply electric_current by {type(value)}')

    

    

    def cast_to_other(self, other: 'electric_current'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return electric_current(base_value / multiplier - offset, multiplier, offset)

class luminous_intensity:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} candela'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'luminous_intensity({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'luminous_intensity') -> bool:
        if not isinstance(other, luminous_intensity):
            raise TypeError(f'Cannot compare luminous_intensity to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'luminous_intensity') -> bool:
        if not isinstance(other, luminous_intensity):
            raise TypeError(f'Cannot compare luminous_intensity to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'luminous_intensity') -> bool:
        if not isinstance(other, luminous_intensity):
            raise TypeError(f'Cannot compare luminous_intensity to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'luminous_intensity') -> bool:
        if not isinstance(other, luminous_intensity):
            raise TypeError(f'Cannot compare luminous_intensity to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'luminous_intensity') -> 'luminous_intensity':
        if not isinstance(other, luminous_intensity):
            raise TypeError(f'Cannot add luminous_intensity to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return luminous_intensity(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'luminous_intensity') -> 'luminous_intensity':
        if not isinstance(other, luminous_intensity):
            raise TypeError(f'Cannot add luminous_intensity to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'luminous_intensity') -> 'luminous_intensity':
        if not isinstance(other, luminous_intensity):
            raise TypeError(f'Cannot add luminous_intensity to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return luminous_intensity(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'luminous_intensity') -> 'luminous_intensity':
        if not isinstance(other, luminous_intensity):
            raise TypeError(f'Cannot add luminous_intensity to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'luminous_intensity':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply luminous_intensity by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'luminous_intensity':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide luminous_intensity by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'luminous_intensity':
        return luminous_intensity(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'luminous_intensity':
        return luminous_intensity(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'luminous_intensity':
        return luminous_intensity(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'luminous_intensity',
        
    )):
        if isinstance(value, (float, int)):
            return luminous_intensity(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, luminous_intensity):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        else:
            raise TypeError(f'Cannot divide luminous_intensity by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
    )):
        if isinstance(value, (float, int)):
            return luminous_intensity(self.value * value, self.multiplier, self.offset)
        
        else:
            raise TypeError(f'Cannot multiply luminous_intensity by {type(value)}')

    

    

    def cast_to_other(self, other: 'luminous_intensity'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return luminous_intensity(base_value / multiplier - offset, multiplier, offset)

class energy:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} Joules'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'energy({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'energy') -> bool:
        if not isinstance(other, energy):
            raise TypeError(f'Cannot compare energy to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'energy') -> bool:
        if not isinstance(other, energy):
            raise TypeError(f'Cannot compare energy to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'energy') -> bool:
        if not isinstance(other, energy):
            raise TypeError(f'Cannot compare energy to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'energy') -> bool:
        if not isinstance(other, energy):
            raise TypeError(f'Cannot compare energy to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'energy') -> 'energy':
        if not isinstance(other, energy):
            raise TypeError(f'Cannot add energy to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return energy(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'energy') -> 'energy':
        if not isinstance(other, energy):
            raise TypeError(f'Cannot add energy to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'energy') -> 'energy':
        if not isinstance(other, energy):
            raise TypeError(f'Cannot add energy to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return energy(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'energy') -> 'energy':
        if not isinstance(other, energy):
            raise TypeError(f'Cannot add energy to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'energy':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply energy by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'energy':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide energy by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'energy':
        return energy(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'energy':
        return energy(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'energy':
        return energy(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'energy',
        
        'force',
        'length',
        'power',
        'time',
        'momentum',
        'speed',
    )):
        if isinstance(value, (float, int)):
            return energy(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, energy):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        elif isinstance(value,force):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return length(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,length):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return force(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,power):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return time(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,time):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return power(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,momentum):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return speed(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,speed):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return momentum(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        else:
            raise TypeError(f'Cannot divide energy by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
    )):
        if isinstance(value, (float, int)):
            return energy(self.value * value, self.multiplier, self.offset)
        
        else:
            raise TypeError(f'Cannot multiply energy by {type(value)}')

    

    

    def cast_to_other(self, other: 'energy'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return energy(base_value / multiplier - offset, multiplier, offset)

class power:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} Watt'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'power({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'power') -> bool:
        if not isinstance(other, power):
            raise TypeError(f'Cannot compare power to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'power') -> bool:
        if not isinstance(other, power):
            raise TypeError(f'Cannot compare power to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'power') -> bool:
        if not isinstance(other, power):
            raise TypeError(f'Cannot compare power to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'power') -> bool:
        if not isinstance(other, power):
            raise TypeError(f'Cannot compare power to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'power') -> 'power':
        if not isinstance(other, power):
            raise TypeError(f'Cannot add power to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return power(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'power') -> 'power':
        if not isinstance(other, power):
            raise TypeError(f'Cannot add power to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'power') -> 'power':
        if not isinstance(other, power):
            raise TypeError(f'Cannot add power to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return power(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'power') -> 'power':
        if not isinstance(other, power):
            raise TypeError(f'Cannot add power to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'power':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply power by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'power':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide power by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'power':
        return power(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'power':
        return power(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'power':
        return power(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'power',
        
        'force',
        'speed',
    )):
        if isinstance(value, (float, int)):
            return power(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, power):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        elif isinstance(value,force):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return speed(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,speed):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return force(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        else:
            raise TypeError(f'Cannot divide power by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
        'time',
    )):
        if isinstance(value, (float, int)):
            return power(self.value * value, self.multiplier, self.offset)
        
        elif isinstance(value, time):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return energy(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        else:
            raise TypeError(f'Cannot multiply power by {type(value)}')

    

    

    def cast_to_other(self, other: 'power'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return power(base_value / multiplier - offset, multiplier, offset)

class speed:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} metre per second'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'speed({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'speed') -> bool:
        if not isinstance(other, speed):
            raise TypeError(f'Cannot compare speed to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'speed') -> bool:
        if not isinstance(other, speed):
            raise TypeError(f'Cannot compare speed to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'speed') -> bool:
        if not isinstance(other, speed):
            raise TypeError(f'Cannot compare speed to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'speed') -> bool:
        if not isinstance(other, speed):
            raise TypeError(f'Cannot compare speed to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'speed') -> 'speed':
        if not isinstance(other, speed):
            raise TypeError(f'Cannot add speed to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return speed(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'speed') -> 'speed':
        if not isinstance(other, speed):
            raise TypeError(f'Cannot add speed to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'speed') -> 'speed':
        if not isinstance(other, speed):
            raise TypeError(f'Cannot add speed to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return speed(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'speed') -> 'speed':
        if not isinstance(other, speed):
            raise TypeError(f'Cannot add speed to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'speed':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply speed by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'speed':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide speed by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'speed':
        return speed(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'speed':
        return speed(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'speed':
        return speed(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'speed',
        
        'acceleration',
        'time',
    )):
        if isinstance(value, (float, int)):
            return speed(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, speed):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        elif isinstance(value,acceleration):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return time(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,time):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return acceleration(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        else:
            raise TypeError(f'Cannot divide speed by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
        'time',
        'momentum',
        'mass',
        'force',
    )):
        if isinstance(value, (float, int)):
            return speed(self.value * value, self.multiplier, self.offset)
        
        elif isinstance(value, time):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return length(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, momentum):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return energy(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, mass):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return momentum(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, force):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return power(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        else:
            raise TypeError(f'Cannot multiply speed by {type(value)}')

    

    

    def cast_to_other(self, other: 'speed'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return speed(base_value / multiplier - offset, multiplier, offset)

class acceleration:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} metre per second^2'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'acceleration({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'acceleration') -> bool:
        if not isinstance(other, acceleration):
            raise TypeError(f'Cannot compare acceleration to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'acceleration') -> bool:
        if not isinstance(other, acceleration):
            raise TypeError(f'Cannot compare acceleration to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'acceleration') -> bool:
        if not isinstance(other, acceleration):
            raise TypeError(f'Cannot compare acceleration to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'acceleration') -> bool:
        if not isinstance(other, acceleration):
            raise TypeError(f'Cannot compare acceleration to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'acceleration') -> 'acceleration':
        if not isinstance(other, acceleration):
            raise TypeError(f'Cannot add acceleration to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return acceleration(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'acceleration') -> 'acceleration':
        if not isinstance(other, acceleration):
            raise TypeError(f'Cannot add acceleration to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'acceleration') -> 'acceleration':
        if not isinstance(other, acceleration):
            raise TypeError(f'Cannot add acceleration to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return acceleration(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'acceleration') -> 'acceleration':
        if not isinstance(other, acceleration):
            raise TypeError(f'Cannot add acceleration to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'acceleration':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply acceleration by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'acceleration':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide acceleration by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'acceleration':
        return acceleration(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'acceleration':
        return acceleration(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'acceleration':
        return acceleration(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'acceleration',
        
    )):
        if isinstance(value, (float, int)):
            return acceleration(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, acceleration):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        else:
            raise TypeError(f'Cannot divide acceleration by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
        'time',
        'mass',
    )):
        if isinstance(value, (float, int)):
            return acceleration(self.value * value, self.multiplier, self.offset)
        
        elif isinstance(value, time):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return speed(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, mass):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return force(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        else:
            raise TypeError(f'Cannot multiply acceleration by {type(value)}')

    

    

    def cast_to_other(self, other: 'acceleration'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return acceleration(base_value / multiplier - offset, multiplier, offset)

class area:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} metre^2'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'area({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'area') -> bool:
        if not isinstance(other, area):
            raise TypeError(f'Cannot compare area to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'area') -> bool:
        if not isinstance(other, area):
            raise TypeError(f'Cannot compare area to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'area') -> bool:
        if not isinstance(other, area):
            raise TypeError(f'Cannot compare area to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'area') -> bool:
        if not isinstance(other, area):
            raise TypeError(f'Cannot compare area to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'area') -> 'area':
        if not isinstance(other, area):
            raise TypeError(f'Cannot add area to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return area(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'area') -> 'area':
        if not isinstance(other, area):
            raise TypeError(f'Cannot add area to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'area') -> 'area':
        if not isinstance(other, area):
            raise TypeError(f'Cannot add area to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return area(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'area') -> 'area':
        if not isinstance(other, area):
            raise TypeError(f'Cannot add area to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'area':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply area by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'area':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide area by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'area':
        return area(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'area':
        return area(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'area':
        return area(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'area',
        
        'length',
    )):
        if isinstance(value, (float, int)):
            return area(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, area):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        elif isinstance(value,length):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return length(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        else:
            raise TypeError(f'Cannot divide area by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
    )):
        if isinstance(value, (float, int)):
            return area(self.value * value, self.multiplier, self.offset)
        
        else:
            raise TypeError(f'Cannot multiply area by {type(value)}')

    
    def sqrt(self):
        v1 = self.cast_to_values(self.multiplier)
        return length(v1.value ** 0.5, v1.multiplier ** 0.5)
    

    

    def cast_to_other(self, other: 'area'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return area(base_value / multiplier - offset, multiplier, offset)

class force:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} Newton'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'force({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'force') -> bool:
        if not isinstance(other, force):
            raise TypeError(f'Cannot compare force to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'force') -> bool:
        if not isinstance(other, force):
            raise TypeError(f'Cannot compare force to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'force') -> bool:
        if not isinstance(other, force):
            raise TypeError(f'Cannot compare force to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'force') -> bool:
        if not isinstance(other, force):
            raise TypeError(f'Cannot compare force to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'force') -> 'force':
        if not isinstance(other, force):
            raise TypeError(f'Cannot add force to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return force(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'force') -> 'force':
        if not isinstance(other, force):
            raise TypeError(f'Cannot add force to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'force') -> 'force':
        if not isinstance(other, force):
            raise TypeError(f'Cannot add force to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return force(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'force') -> 'force':
        if not isinstance(other, force):
            raise TypeError(f'Cannot add force to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'force':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply force by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'force':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide force by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'force':
        return force(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'force':
        return force(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'force':
        return force(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'force',
        
        'mass',
        'acceleration',
    )):
        if isinstance(value, (float, int)):
            return force(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, force):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        elif isinstance(value,mass):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return acceleration(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,acceleration):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return mass(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        else:
            raise TypeError(f'Cannot divide force by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
        'length',
        'time',
        'speed',
    )):
        if isinstance(value, (float, int)):
            return force(self.value * value, self.multiplier, self.offset)
        
        elif isinstance(value, length):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return energy(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, time):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return momentum(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        elif isinstance(value, speed):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return power(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        else:
            raise TypeError(f'Cannot multiply force by {type(value)}')

    

    

    def cast_to_other(self, other: 'force'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return force(base_value / multiplier - offset, multiplier, offset)

class momentum:
    def __init__(
        self,
        value=0.0,
        multiplier=1.0,
        offset=0.0
    ):
        self.value = float(value)
        self.multiplier = float(multiplier)
        self.offset = float(offset)

    def __str__(self):
        return f'{self.cast_to_values().value} kilogram-meter per second'

    def __float__(self):
        return self.cast_to_values().value

    def __repr__(self):
        return f'momentum({self.value}, {self.multiplier}, {self.offset})'

    def __lt__(self, other: 'momentum') -> bool:
        if not isinstance(other, momentum):
            raise TypeError(f'Cannot compare momentum to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value < other.value

    def __le__(self, other: 'momentum') -> bool:
        if not isinstance(other, momentum):
            raise TypeError(f'Cannot compare momentum to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value <= other.value

    def __gt__(self, other: 'momentum') -> bool:
        if not isinstance(other, momentum):
            raise TypeError(f'Cannot compare momentum to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value > other.value

    def __ge__(self, other: 'momentum') -> bool:
        if not isinstance(other, momentum):
            raise TypeError(f'Cannot compare momentum to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return self.value >= other.value

    def __add__(self, other: 'momentum') -> 'momentum':
        if not isinstance(other, momentum):
            raise TypeError(f'Cannot add momentum to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return momentum(self.value + other.value, self.multiplier, self.offset)

    def __iadd__(self, other: 'momentum') -> 'momentum':
        if not isinstance(other, momentum):
            raise TypeError(f'Cannot add momentum to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value += other.value
        return self

    def __sub__(self, other: 'momentum') -> 'momentum':
        if not isinstance(other, momentum):
            raise TypeError(f'Cannot add momentum to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        return momentum(self.value - other.value, self.multiplier, self.offset)

    def __isub__(self, other: 'momentum') -> 'momentum':
        if not isinstance(other, momentum):
            raise TypeError(f'Cannot add momentum to {type(other)}')
        other = other.cast_to_values(self.multiplier, self.offset)
        self.value -= other.value
        return self

    def __imul__(self, other: (float, int)) -> 'momentum':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot multiply momentum by {type(other)}')
        self.value *= other
        return self

    def __idiv__(self, other: (float, int)) -> 'momentum':
        if not isinstance(other, (float, int)):
            raise TypeError(f'Cannot divide momentum by {type(other)}')
        self.value /= other
        return self

    def __neg__(self) -> 'momentum':
        return momentum(-self.value, self.multiplier, self.offset)

    def __pos__(self) -> 'momentum':
        return momentum(+self.value, self.multiplier, self.offset)

    def __abs__(self) -> 'momentum':
        return momentum(abs(self.value), self.multiplier, self.offset)

    def __truediv__(self, value: (
        float,
        int,
        'momentum',
        
        'force',
        'time',
        'mass',
        'speed',
    )):
        if isinstance(value, (float, int)):
            return momentum(self.value / value, self.multiplier, self.offset)
        elif isinstance(value, momentum):
            v1 = self.cast_to_values()
            v2 = value.cast_to_values()
            return v1.value / v2.value
        
        elif isinstance(value,force):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return time(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,time):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return force(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,mass):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return speed(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        elif isinstance(value,speed):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return mass(v1.value / v2.value, v1.multiplier / v2.multiplier)
        
        else:
            raise TypeError(f'Cannot divide momentum by {type(value)}')

    def __mul__(self, value: (
        float,
        int,
        
        'speed',
    )):
        if isinstance(value, (float, int)):
            return momentum(self.value * value, self.multiplier, self.offset)
        
        elif isinstance(value, speed):
            v1 = self.cast_to_values(self.multiplier)
            v2 = value.cast_to_values(value.multiplier)
            return energy(v1.value * v2.value, v1.multiplier * v2.multiplier)
        
        else:
            raise TypeError(f'Cannot multiply momentum by {type(value)}')

    

    

    def cast_to_other(self, other: 'momentum'):
        return self.cast_to_values(other.multiplier, other.offset)

    def cast_to_values(self, multiplier: float = 1.0, offset: float = 0.0):
        base_value = self.value * self.multiplier + self.offset
        return momentum(base_value / multiplier - offset, multiplier, offset)


class literals:


    @staticmethod
    def a(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 31536000000.0, 0.0)

    @staticmethod
    def d(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 86400000.0, 0.0)

    @staticmethod
    def h(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 3600.0, 0.0)

    @staticmethod
    def min(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 60.0, 0.0)

    @staticmethod
    def s(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 1.0, 0.0)

    @staticmethod
    def ms(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 0.001, 0.0)

    @staticmethod
    def us(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 1e-06, 0.0)

    @staticmethod
    def ns(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 1e-09, 0.0)

    @staticmethod
    def ps(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 1e-12, 0.0)

    @staticmethod
    def fs(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 1e-15, 0.0)

    @staticmethod
    def as_(val: (float,int)) -> 'time':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return time(val, 1e-18, 0.0)



    @staticmethod
    def m(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 1.0, 0.0)

    @staticmethod
    def km(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 1000.0, 0.0)

    @staticmethod
    def dm(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 0.1, 0.0)

    @staticmethod
    def cm(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 0.01, 0.0)

    @staticmethod
    def mm(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 0.001, 0.0)

    @staticmethod
    def um(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 1e-06, 0.0)

    @staticmethod
    def nm(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 1e-09, 0.0)

    @staticmethod
    def pm(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 1e-12, 0.0)

    @staticmethod
    def fm(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 1e-15, 0.0)

    @staticmethod
    def am(val: (float,int)) -> 'length':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return length(val, 1e-18, 0.0)



    @staticmethod
    def t(val: (float,int)) -> 'mass':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return mass(val, 1000.0, 0.0)

    @staticmethod
    def kg(val: (float,int)) -> 'mass':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return mass(val, 1.0, 0.0)

    @staticmethod
    def g(val: (float,int)) -> 'mass':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return mass(val, 0.001, 0.0)

    @staticmethod
    def mg(val: (float,int)) -> 'mass':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return mass(val, 1e-06, 0.0)

    @staticmethod
    def ug(val: (float,int)) -> 'mass':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return mass(val, 1e-09, 0.0)

    @staticmethod
    def ng(val: (float,int)) -> 'mass':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return mass(val, 1.0000000000000002e-12, 0.0)

    @staticmethod
    def pg(val: (float,int)) -> 'mass':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return mass(val, 1e-15, 0.0)

    @staticmethod
    def fg(val: (float,int)) -> 'mass':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return mass(val, 1e-18, 0.0)

    @staticmethod
    def ag(val: (float,int)) -> 'mass':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return mass(val, 1.0000000000000001e-21, 0.0)



    @staticmethod
    def K(val: (float,int)) -> 'temperature':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return temperature(val, 1.0, 0.0)

    @staticmethod
    def C(val: (float,int)) -> 'temperature':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return temperature(val, 1.0, 273.15)



    @staticmethod
    def mol(val: (float,int)) -> 'amount':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return amount(val, 6.02214076e+23, 0.0)

    @staticmethod
    def things(val: (float,int)) -> 'amount':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return amount(val, 1.0, 0.0)



    @staticmethod
    def A(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1.0, 0.0)

    @staticmethod
    def PA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1000000000000000.0, 0.0)

    @staticmethod
    def TA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1000000000000.0, 0.0)

    @staticmethod
    def GA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1000000000.0, 0.0)

    @staticmethod
    def MA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1000000.0, 0.0)

    @staticmethod
    def kA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1000.0, 0.0)

    @staticmethod
    def mA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 0.001, 0.0)

    @staticmethod
    def uA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1e-06, 0.0)

    @staticmethod
    def nA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1e-09, 0.0)

    @staticmethod
    def pA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1e-12, 0.0)

    @staticmethod
    def fA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1e-15, 0.0)

    @staticmethod
    def aA(val: (float,int)) -> 'electric_current':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return electric_current(val, 1e-18, 0.0)



    @staticmethod
    def cd(val: (float,int)) -> 'luminous_intensity':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return luminous_intensity(val, 1.0, 0.0)



    @staticmethod
    def J(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.0, 0.0)

    @staticmethod
    def Nm(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.0, 0.0)

    @staticmethod
    def eV(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.602176634e-19, 0.0)

    @staticmethod
    def Wh(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 3600.0, 0.0)

    @staticmethod
    def Ws(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.0, 0.0)

    @staticmethod
    def PJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1000000000000000.0, 0.0)

    @staticmethod
    def TJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1000000000000.0, 0.0)

    @staticmethod
    def GJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1000000000.0, 0.0)

    @staticmethod
    def MJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1000000.0, 0.0)

    @staticmethod
    def kJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1000.0, 0.0)

    @staticmethod
    def mJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 0.001, 0.0)

    @staticmethod
    def uJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1e-06, 0.0)

    @staticmethod
    def nJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1e-09, 0.0)

    @staticmethod
    def pJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1e-12, 0.0)

    @staticmethod
    def fJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1e-15, 0.0)

    @staticmethod
    def aJ(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1e-18, 0.0)

    @staticmethod
    def GNm(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1000000000.0, 0.0)

    @staticmethod
    def MNm(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1000000.0, 0.0)

    @staticmethod
    def kNm(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1000.0, 0.0)

    @staticmethod
    def mNm(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 0.001, 0.0)

    @staticmethod
    def uNm(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1e-06, 0.0)

    @staticmethod
    def PeV(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 0.0001602176634, 0.0)

    @staticmethod
    def TeV(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.602176634e-07, 0.0)

    @staticmethod
    def GeV(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.6021766339999998e-10, 0.0)

    @staticmethod
    def MeV(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.6021766339999998e-13, 0.0)

    @staticmethod
    def keV(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.602176634e-16, 0.0)

    @staticmethod
    def meV(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.6021766339999998e-22, 0.0)

    @staticmethod
    def ueV(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 1.602176634e-25, 0.0)

    @staticmethod
    def PWh(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 3.6e+18, 0.0)

    @staticmethod
    def TWh(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 3600000000000000.0, 0.0)

    @staticmethod
    def GWh(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 3600000000000.0, 0.0)

    @staticmethod
    def MWh(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 3600000000.0, 0.0)

    @staticmethod
    def kWh(val: (float,int)) -> 'energy':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return energy(val, 3600000.0, 0.0)



    @staticmethod
    def W(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1.0, 0.0)

    @staticmethod
    def PW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1000000000000000.0, 0.0)

    @staticmethod
    def TW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1000000000000.0, 0.0)

    @staticmethod
    def GW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1000000000.0, 0.0)

    @staticmethod
    def MW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1000000.0, 0.0)

    @staticmethod
    def kW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1000.0, 0.0)

    @staticmethod
    def mW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 0.001, 0.0)

    @staticmethod
    def uW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1e-06, 0.0)

    @staticmethod
    def nW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1e-09, 0.0)

    @staticmethod
    def pW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1e-12, 0.0)

    @staticmethod
    def fW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1e-15, 0.0)

    @staticmethod
    def aW(val: (float,int)) -> 'power':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return power(val, 1e-18, 0.0)



    @staticmethod
    def mps(val: (float,int)) -> 'speed':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return speed(val, 1.0, 0.0)

    @staticmethod
    def kmph(val: (float,int)) -> 'speed':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return speed(val, 0.2777777777777778, 0.0)



    @staticmethod
    def mps2(val: (float,int)) -> 'acceleration':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return acceleration(val, 1.0, 0.0)

    @staticmethod
    def G(val: (float,int)) -> 'acceleration':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return acceleration(val, 9.80665, 0.0)



    @staticmethod
    def m2(val: (float,int)) -> 'area':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return area(val, 1.0, 0.0)

    @staticmethod
    def are(val: (float,int)) -> 'area':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return area(val, 100.0, 0.0)

    @staticmethod
    def hectare(val: (float,int)) -> 'area':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return area(val, 10000.0, 0.0)

    @staticmethod
    def km2(val: (float,int)) -> 'area':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return area(val, 1000000.0, 0.0)

    @staticmethod
    def mm2(val: (float,int)) -> 'area':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return area(val, 1e-06, 0.0)

    @staticmethod
    def um2(val: (float,int)) -> 'area':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return area(val, 1e-12, 0.0)

    @staticmethod
    def nm2(val: (float,int)) -> 'area':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return area(val, 1e-18, 0.0)



    @staticmethod
    def N(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1.0, 0.0)

    @staticmethod
    def PN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1000000000000000.0, 0.0)

    @staticmethod
    def TN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1000000000000.0, 0.0)

    @staticmethod
    def GN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1000000000.0, 0.0)

    @staticmethod
    def MN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1000000.0, 0.0)

    @staticmethod
    def kN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1000.0, 0.0)

    @staticmethod
    def mN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 0.001, 0.0)

    @staticmethod
    def uN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1e-06, 0.0)

    @staticmethod
    def nN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1e-09, 0.0)

    @staticmethod
    def pN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1e-12, 0.0)

    @staticmethod
    def fN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1e-15, 0.0)

    @staticmethod
    def aN(val: (float,int)) -> 'force':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return force(val, 1e-18, 0.0)



    @staticmethod
    def kgmps(val: (float,int)) -> 'momentum':
        if not isinstance(val, (int, float)):
            raise TypeError("val must be a number")
        return momentum(val, 1.0, 0.0)



    