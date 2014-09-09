#!/usr/bin/env python

import logging
l = logging.getLogger("claripy.expression")

from .storable import Storable

class A(object):
    '''
    An A(ST) tracks a tree of operations on arguments.
    '''

    def __init__(self, op, args):
        self._op = op
        self._args = args

    def eval(self, backends, save, model=None):
        args = [ ]
        for a in self._args:
            if isinstance(a, E):
                args.append(a.eval(backends=backends, save=save, model=model))
            elif isinstance(a, A):
                args.append(a.eval(backends, save, model=model))
            else:
                args.append(a)

        for b in backends:
            l.debug("trying evaluation with %s", b)
            try:
                return b.call(self._op, args, model=model)
            except BackendError:
                l.debug("... failed")
                continue

        raise Exception("eval failed with available backends")

    def __repr__(self):
        if '__' in self._op:
            return "%s.%s%s" % (self._args[0], self._op, self._args[1:])
        else:
            return "%s%s" % (self._op, self._args)

class E(Storable):
    '''
    A class to wrap expressions.
    '''
    __slots__ = [ 'length', 'variables', 'symbolic', '_uuid', '_model', '_stored', 'objects' ]

    def __init__(self, claripy, length=None, variables=None, symbolic=None, uuid=None, objects=None, model=None, stored=False):
        Storable.__init__(self, claripy, uuid=uuid)
        have_uuid = uuid is not None
        have_data = not (variables is None and symbolic is None and model is None and length is None)
        self.objects = { }

        if have_uuid and not have_data:
            self._load()
        elif have_data:
            self.variables = variables
            self.symbolic = symbolic
            self.length = length

            self._uuid = uuid
            self._model = model
            self._stored = stored

            if objects is not None:
                self.objects.update(objects)
        else:
            raise ValueError("invalid arguments passed to E()")

    def _load(self):
        e = self._claripy.dl.load_expression(self._uuid)
        self.variables = e.variables
        self.symbolic = e.symbolic

        self._uuid = e._uuid
        self._model = e._model
        self._stored = e._stored

    def __nonzero__(self):
        raise Exception('testing Expressions for truthiness does not do what you want, as these expressions can be symbolic')

    def __repr__(self):
        name = "E"
        if self.symbolic:
            name += "S"
        return name + "(%s)" % self._model

    def _do_op(self, op_name, args):
        return self._claripy._do_op(op_name, (self,) + tuple(args))

    def split(self, split_on):
        if not isinstance(self._model, A):
            return [ self ]

        if self._model._op in split_on:
            l.debug("Trying to split: %r", self._model)
            if all(isinstance(a, E) for a in self._model._args):
                return self._model._args[:]
            else:
                raise Exception('wtf')
        else:
            l.debug("no split for you")
            return [ self ]

    #
    # Storing and loading of expressions
    #

    def store(self):
        self._claripy.dl.store_expression(self)

    def __getstate__(self):
        if self._uuid is not None:
            l.debug("uuid pickle on %s", self)
            return self._uuid
        l.debug("full pickle on %s", self)
        return self._uuid, self._model, self.variables, self.symbolic, self.length

    def __setstate__(self, s):
        if type(s) is str:
            self.__init__([ ], uuid=s)
            return

        uuid, ast, variables, symbolic, length = s
        self.__init__([ ], variables=variables, symbolic=symbolic, ast=ast, uuid=uuid, length=length)

    #
    # BV operations
    #

    def __len__(self):
        if self.length == -1:
            raise TypeError('this expression has no length')
        return self.length
    size = __len__

    def __iter__(self):
        raise Exception("Please don't iterate over Expressions!")

    def simplify(self):
        try:
            return self._claripy.model_backend.simplify_expr(self)
        except BackendError:
            for b in self._claripy.solver_backends:
                try:
                    return b.simplify_expr(self)
                except BackendError:
                    pass

        raise Exception("unable to simplify")

    def chop(self, bits=1):
        s = len(self)
        if s % bits != 0:
            raise ValueError("expression length (%d) should be a multiple of 'bits' (%d)" % (len(self), bits))
        elif s == bits:
            return [ self ]
        else:
            return list(reversed([ self[(n+1)*bits - 1:n*bits] for n in range(0, s / bits) ]))

    def reversed(self, chunk_bits=8):
        '''
        Reverses the expression.
        '''
        s = self.chop(bits=chunk_bits)
        if len(s) == 1:
            return s[0]
        else:
            return self._claripy.Concat(*reversed(s))

    def __getitem__(self, rng):
        if type(rng) is slice:
            return self._claripy.Extract(int(rng.start), int(rng.stop), self)
        else:
            return self._claripy.Extract(int(rng), int(rng), self)

    def zero_extend(self, n):
        return self._claripy.ZeroExt(n, self)

    def sign_extend(self, n):
        return self._claripy.SignExt(n, self)

#
# Wrap stuff
#

def e_operator(cls, op_name):
    def wrapper(self, *args):
        return self._do_op(op_name, args)
    wrapper.__name__ = op_name
    setattr(cls, op_name, wrapper)

#def a_operator(cls, op_name):
#   def do_op(self, *args):
#       return A(op_name, args)
#   wrapper.__name__ = op_name
#   setattr(cls, op_name, wrapper)

def make_methods():
    for operations in [expression_operations, expression_bitwise_operations, expression_arithmetic_operations, expression_comparator_operations]:
        for name in operations:
            e_operator(E, name)

from .backends.backend import BackendError
from .operations import expression_operations, expression_bitwise_operations, expression_arithmetic_operations, expression_comparator_operations
make_methods()
