import operator
from dataclasses import dataclass
from functools import reduce
from typing import Callable, Generator, Iterator

HEX_TO_BITS = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

FUNC_LOOKUP: dict[int, Callable] = {
    0: lambda *args: reduce(operator.add, args),
    1: lambda *args: reduce(operator.mul, args),
    2: lambda *args: min(args),
    3: lambda *args: max(args),
    5: lambda t1, t2: 1 if t1 > t2 else 0,
    6: lambda t1, t2: 1 if t1 < t2 else 0,
    7: lambda t1, t2: 1 if t1 == t2 else 0
}

def replace_hex_with_bits(text: str) -> str:
    return ''.join(HEX_TO_BITS[b] for b in text)

@dataclass
class Packet:
    version: int
    typeId: int
    subpackets: list['Packet']

    def visit(self) -> Generator['Packet', None, None]:
        yield self
        for p in self.subpackets:
            yield from p.visit()

    def get_value(self) -> int:
        raise NotImplementedError()

def read_bits(text_iter: Iterator, num: int) -> str:
    text = ''
    for _ in range(num):
        text += next(text_iter)
    return text

def read_rest(text_iter: Iterator) -> str:
    value = ""
    try:
        value += next(text_iter)
    except StopIteration:
        pass
    return value

@dataclass
class LiteralValuePacket(Packet):
    value: int

    def get_value(self) -> int:
        return self.value

@dataclass
class OperatorPacket(Packet):
    func: Callable

    def get_value(self) -> int:
        values = [p.get_value() for p in self.subpackets]
        return self.func(*values)

def parse_packet(text_iter: Iterator) -> Packet:
    version = int(read_bits(text_iter, 3), base=2)
    typeId = int(read_bits(text_iter, 3), base=2)
    parser = parse_literal_packet if typeId == 4 else parse_operator_packet
    packet = parser(version, typeId, text_iter)
    return packet

def parse_literal_packet(version: int, typeId: int,
                         text_iter: Iterator) -> LiteralValuePacket:
    number_of_bits = 6
    # get next five bits
    bitstring = ""
    while (bits := read_bits(text_iter, 5)).startswith('1'):
        number_of_bits += 5
        bitstring += bits[1:]

    # add the zero prefixed
    number_of_bits += 5
    bitstring += bits[1:]
    return LiteralValuePacket(version, typeId, [], int(bitstring, base=2))

def parse_operator_packet(version: int, typeId: int,
                         text_iter: Iterator) -> Packet:
    length_type = next(text_iter)
    if length_type == '1':
        number_of_sub_packets = int(read_bits(text_iter, 11), base=2)
        sub_packets = []
        for _ in range(number_of_sub_packets):
            sub_packets.append(parse_packet(text_iter))

    else:
        number_of_bits = int(read_bits(text_iter, 15), base=2)
        sub_packet_bits = read_bits(text_iter, number_of_bits)
        sub_packet_bit_iter = iter(sub_packet_bits)
        sub_packets = []
        try:
            while True:
                sub_packets.append(parse_packet(sub_packet_bit_iter))
        except StopIteration:
            # this is okay, we just have no more bits to read
            pass

    func = FUNC_LOOKUP[typeId]
    return OperatorPacket(version, typeId, sub_packets, func)

def to_packet(text: str) -> Packet:
    bits = replace_hex_with_bits(text)
    text_iter = iter(bits)
    packet =  parse_packet(text_iter)
    zeroes = read_rest(text_iter)
    assert all(z=='0' for z in zeroes)
    return packet

def get_version_numbers(packet: Packet):
    return sum(p.version for p in packet.visit())

with open("input/input16.txt", encoding="utf-8") as f:
    PACKET = to_packet(f.read().strip())
if __name__ == "__main__":
    print(f"All version numbers: {get_version_numbers(PACKET)}")
    print(f"All version numbers: {PACKET.get_value()}")
