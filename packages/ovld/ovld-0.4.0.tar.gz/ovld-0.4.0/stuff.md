
In order to determine which of its methods to call on a list of arguments, `ovld` proceeds as follows:

1. The matching method with highest user-defined **priority** is called first.
2. In case of equal user-defined priority, the more **specific** method is called. In order of specificity, if `Cat` subclass of `Mammal` subclass of `Animal`, and `Meower` and `Woofer` are protocols:
   * Single argument: `Cat > Mammal > Animal`
   * Multiple arguments: `(Cat, Cat) > (Cat, Mammal) > (Animal, Mammal)`
   * Multiple arguments: `(Cat, Mammal) <> (Animal, Cat)` (one argument more specific, the other less specific: unordered!)
   * `Cat > Meower`, but `Meower <> Woofer` (protocols are unordered)
   * If matching methods are unordered, an error will be raised
3. If a method calls the special function `call_next`, they will call the next method in the list.



## Ambiguous calls

The following definitions will cause a TypeError at runtime when called with two ints, because it is unclear which function is the right match:

```python
@ovld
def ambig(x: int, y: object):
    print("io")

@ovld
def ambig(x: object, y: int):
    print("oi")

ambig(8, 8)  # ???
```

You may define an additional function with signature (int, int) to disambiguate, or define one of them with a higher priority:

```python
@ovld
def ambig(x: int, y: int):
    print("ii")
```

Other ambiguity situations are:

* If multiple Protocols match the same type (and there is nothing more specific)
* If multiple Dependent match
* Multiple inheritance: a class that inherits from X and Y will ambiguously match rules for X and Y. Yes, Python's full mro order says X comes before Y, but `ovld` does not use it. This may change in the future or if this causes legitimate issues.
