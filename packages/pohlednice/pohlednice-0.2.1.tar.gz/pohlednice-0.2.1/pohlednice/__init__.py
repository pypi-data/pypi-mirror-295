from struct import Struct as _Struct

class VarInt:
    @classmethod
    def to_bytes(cls, value):
        while True:
            window = value & 0b111_1111
            value = value >> 7

            if value == 0:
                yield window
                break
            else:
                yield window | 0b1000_0000  
            
    @classmethod
    def from_bytes(cls, iterable):
        value = 0

        for index, byte in enumerate(iterable):
            value = (byte & ~0b1000_0000) << (index * 7) | value
            if not byte & 0b1000_0000:
                break

        return value

class U8:
    @classmethod
    def to_bytes(cls, value):
        yield value

    @classmethod
    def from_bytes(cls, iterable):
        return next(iterable)

class U16(VarInt):
    ...

class U32(VarInt):
    ...

class U64(VarInt):
    ...

class U128(VarInt):
    ...
    
class SignedVarInt(VarInt):
    @classmethod
    def to_bytes(cls, value):
        if value < 0:
            _value = ((-value - 1) << 1) | 1
        else:
            _value = value << 1
            
        yield from super().to_bytes(_value)

    @classmethod
    def from_bytes(cls, iterable):
        value = super().from_bytes(iterable)

        is_negative = value & 0x1

        value = value >> 1

        if is_negative:
            return -value - 1
        else:
            return value
            
        
class I8:
    @classmethod
    def to_bytes(cls, value):
        if value < 0:
            yield 0b1000_0000 | -value
        else:
            yield value

    @classmethod
    def from_bytes(cls, iterable):
        byte = next(iterable)
        value = (0b0111_1111 & byte)
        if (0b1000_0000 & byte):
            return -value
        else:
            return value

    
class I16(SignedVarInt):
    ...


class I32(SignedVarInt):
    ...


class I64(SignedVarInt):
    ...


class I128(SignedVarInt):
    ...


class __Float:
    @classmethod
    def to_bytes(cls, value):
        yield from iter(cls._format.pack(value))

    @classmethod
    def from_bytes(cls, iterable):
        buffer_ = b''

        for _ in range(cls._format.size):
            buffer_ += bytes(iterable)

        value, = cls._format.unpack(buffer_)
            
        return value

class F32(__Float):
    _format = _Struct('f')

    
class F64(__Float):
    _format = _Struct('d')

    
class Bool:
    @classmethod
    def to_bytes(cls, value):
        if value:
            yield 1
        else:
            yield 0

    @classmethod
    def from_bytes(cls, iterable):
        match byte := next(iterable):
            case 0:
                return False
            case 1:
                return True
            case _:
                raise ValueError(f'{byte} is not valid for bool type !')


class Option:
    @classmethod
    def __class_getitem__(cls, type_):
        class SpecializedOption(cls):
            type = type_

        return SpecializedOption

    @classmethod
    def to_bytes(cls, value):
        if value is None:
            yield 0
        else:
            yield 1
            yield from cls.type.to_bytes(value)


    @classmethod
    def from_bytes(cls, iterable):
        if Bool.from_bytes(iterable):
            return cls.type.from_bytes(iterable)
        else:
            return None


class Tuple:
    Container = tuple

    @classmethod
    def __class_getitem__(cls, types_):
        if not isinstance(types_, tuple):
            types_ = (types_,)
        
        class SpecializedTuple(cls):
            types = types_

        return SpecializedTuple

    @classmethod
    def to_bytes(cls, value):
        for type_, _value in zip(cls.types, value):
            yield from type_.to_bytes(_value)

    @classmethod
    def from_bytes(cls, iterable):
        return cls.Container(
            type_.from_bytes(iterable)
            for type_
            in cls.types
        )

class Array(Tuple):
    Container = list

    @classmethod
    def __class_getitem__(cls, type_):
        type_, length = type_
        return super().derive(*((type_,) * length))

class Struct:
    def __init__(self, *values):
        for name, value in zip(get_annotations(type(self)).keys(), values):
            setattr(self, name, value)

    @classmethod
    def to_bytes(cls, value):
        for name, type_ in get_annotations(cls).items():
            yield from type_.to_bytes(getattr(value, name))

    @classmethod
    def from_bytes(cls, iterable):
        return cls(*(
            type_.from_bytes(iterable)
            for type_ 
            in get_annotations(cls).values()
        ))

class List:
    @classmethod
    def __class_getitem__(cls, type_):
        class SpecializedList(cls):
            type = type_

        return SpecializedList
    
    @classmethod
    def to_bytes(cls, value):
        yield from VarInt.to_bytes(len(value))
        
        for _value in value:
            yield from cls.type.to_bytes(_value)

    @classmethod
    def from_bytes(cls, iterable):
        length = VarInt.from_bytes(iterable)

        return [cls.type.from_bytes(iterable)
                for _
                in range(length)]


class ByteArray(List):
    type = U8


class String(ByteArray):
    @classmethod
    def to_bytes(cls, value):
        yield from super().to_bytes(value.encode('utf-8'))

    @classmethod
    def from_bytes(cls, iterable):
        return bytes(super().from_bytes(iterable)).decode('utf-8') 
    

class Dict:
    @classmethod
    def __class_getitem__(cls, type_):
        key_, value_ = type_

        class SpecializedDict(cls):
            key = key_
            value = value_

        return SpecializedDict

    @classmethod
    def __type(cls):
        class Item(Tuple):
            types = (cls.key, cls.value)

        class Items(List):
            type = Item

        return Items
    
    @classmethod
    def to_bytes(cls, value):
        yield from cls.__type().to_bytes(list(value.items()))

    @classmethod
    def from_bytes(cls, iterable):
        return dict(cls.__type().from_bytes(iterable))

from inspect import get_annotations

class Variant:
    type = None

    def __init__(self, value=None):
        if value is None and self.type is not None:
            raise ValueError(f"value is None while type is {self.type}")
        
        self.value = value
    
    @classmethod
    def __class_getitem__(cls, key):
        return type(f"{cls.__name__}[{key.__name__}]", 
                    (cls,), 
                    {'type': key})

    def __repr__(self):
        return f"{type(self).__name__}({self.value})"

    @classmethod
    def to_bytes(cls, value):
        yield from VarInt.to_bytes(cls.index)
        
        if cls.type is not None:
            yield from cls.type.to_bytes(value.value)

    @classmethod
    def _from_bytes(cls, iterable):
        if cls.type is None:
            return None
        
        return cls(cls.type.from_bytes(iterable))

class Enum:
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        setattr(cls, 'variant_by_index', {})
        for index, annotation in enumerate(get_annotations(cls).items()):
            key, value = annotation

            if value is not None:
                _type = Variant[value]
                value = type(f"{cls.__name__}.{key}:{_type.__name__}",
                             (_type,),
                             {'index': index})
            else:
                value = type(f'{cls.__name__}.{key}:Variant', 
                             (Variant,), 
                             {'index': index})()

            cls.variant_by_index[index] = value            
            setattr(cls, key, value)

    @classmethod
    def to_bytes(cls, value):
        yield from type(value).to_bytes(value)

    @classmethod
    def from_bytes(cls, iterable):
        index = VarInt.from_bytes(iterable)

        return cls.variant_by_index[index]._from_bytes(iterable)
