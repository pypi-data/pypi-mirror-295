
= TODO

* Support `[*args]
* Support `[**args]
* Guarantee that we avoid name clashes
* Cache the dependency graph
* Cache dependent_dispatch when it represents the same handlers
* Look for Any inside tuples when ordering `[@dependent_check]
* Implement Tensor/Array/Shape/Dtype/etc.
* Support `[|] and `[&] between DependentType and normal types
* Properly identify nested DependentTypes when figuring out if type is dependent
* Optimize the itertools.product in mro
* Context variable to turn off code generation


= DONE

* Custom relative ordering of dependent types
* Codegen for dependent_dispatch
* Fix issue when adapt_function is called on a closure
* Problem when recurse is in closure and recurse(*xyz) causes it to be removed
* Rename dependent_dispatch
* Support Annotated
* Support `[Literal[x1, x2]]
* Support Union of DependentType
* Make sure there is proper ordering between `[Literal[0]] and `object
* Fix `[_make_signature]
* Implement codegen for Or/And
