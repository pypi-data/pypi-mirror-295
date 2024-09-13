
Guide
=====

Give's syntax
-------------

There are multiple ways you can use :func:`~giving.api.give`. ``give`` returns None *unless* it is given a single positional argument, in which case it returns the value of that argument.

* **give(key=value)**

  This is the most straightforward way to use ``give``: you write out both the key and the value associated.

  *Returns:* None

* **x = give(value)**

  When no key is given, but the result of ``give`` is assigned to a variable, the key is the name of that variable. In other words, the above is equivalent to ``give(x=value)``.

  *Returns:* The value

* **give(x)**

  When no key is given and the result is *not* assigned to a variable, ``give(x)`` is equivalent to ``give(x=x)``. If the argument is an expression like ``x * x``, the key will be the string ``"x * x"``.

  *Returns:* The value

* **give(x, y, z)**

  Multiple arguments can be given. The above is equivalent to ``give(x=x, y=y, z=z)``.

  *Returns:* None

* **x = value; give()**

  If ``give`` has no arguments at all, it will look at the immediately previous statement and infer what you mean. The above is equivalent to ``x = value; give(x=value)``.

  *Returns:* None


Time and code location
^^^^^^^^^^^^^^^^^^^^^^

* :meth:`give.line(...)<giving.gvr.Giver.line>` emits, in addition to the rest, ``{"$line": location_info}`` where ``location_info`` is a :class:`~giving.gvr.LinePosition` object that corresponds to where ``give.line`` was called.
* :meth:`give.time(...)<giving.gvr.Giver.time>` emits, in addition to the rest, ``{"$time": time.time()}``


Wrapping
^^^^^^^^

Use the :meth:`~giving.gvr.Giver.wrap` method to create blocks in which other context managers can be plugged:


.. code-block:: python

    @contextmanager
    def hello():
        print("hello!")
        yield
        print("bye!")

    with given() as gv:

        gv.wrap("main", hello)

        with give.wrap("main"):
            print(":)")

    # prints:
    # hello!
    # :)
    # bye!


Customization
^^^^^^^^^^^^^

Custom versions of ``give`` can be created with :func:`~giving.gvr.giver`. For example, ``givex = giver("x", y=7); givex(2)`` would emit ``{"x": 2, "y": 7}``. You can also create give/given pairs with :func:`~giving.api.make_give`.


Important methods
-----------------

The important methods listed here are those you should know in order to be immediately productive with Giving. They are available on the ``given()`` object. Unless otherwise specified, assume we are inside a block defined by ``with given() as gv: ...``.

* :func:`~giving.gvn.Given.print` and :func:`~giving.gvn.Given.display`: Print the stuff to the terminal. ``display`` looks nicer, but ``print`` has more flexible formatting.

  .. code-block:: python

      gv.print("x = {x}, y = {y:.2%}")

* :func:`~giving.gvn.Given.accum`: This returns a list to which the stream's dicts will be appended. This allows you to do anything you want that can be done with a list, like reductions or plotting. Giving provides a battery of operators that might do the job better, but if you have trouble with the paradigm or can't be bothered, this is an easy escape hatch.

  .. code-block:: python

      results = gv.accum()
      ...
      print(sum(data["x"] for data in results if "x" in data))

* :meth:`~giving.gvn.Given.values`: Context manager which accumulates all values into a list (``with given().values() as vals: ...`` is essentially the same as ``with given() as gv: vals = gv.accum() ...``).

  .. code-block:: python

      with given()["?x"].values() as results:
          ...

      print(sum(results))

* :func:`~giving.gvn.Given.subscribe` and :func:`~giving.gvn.Given.ksubscribe`: Do stuff with the data as it comes. The difference between ``subscribe`` and ``ksubscribe`` is that the former is called with one argument, which is the next entry in the stream, whereas the latter assumes that all the elements are dicts, and the function is called with ``**kwargs`` syntax.

  .. note::

    ``ksubscribe`` will wrap the function with :func:`~giving.utils.lax_function` so that it has an implicit ``**kwargs`` argument at the end, to make your life easier. That way, any keys that are not useful to your function are simply ignored.

  .. code-block:: python

      # Compare
      @gv.subscribe
      def pr(data):
          print("x = {x}, y = {y}".format(data))

      # to:
      @gv.ksubscribe
      def pr(x, y):
          print(f"x = {x}, y = {y}")

* ``gv[key]``, ``gv["?key"]``: Extracts all the values for a key.

  * Without a leading ``?``, e.g. ``gv["x"]``, every entry *must* have the key.
  * With a leading ``?``, e.g. ``gv["?x"]``, entries that don't have the key are ignored. This is often the more useful syntax.

  .. code-block:: python

    gv["?x"].print()

* :func:`~giving.operators.where`, :func:`~giving.operators.where_any`, :func:`~giving.operators.keep`: These operators filter entries depending on the keys they have and their values.

  * ``where`` returns entries where all keys are present, and conditions are met
  * ``where_any`` returns entries where any key is present (does not support conditions)
  * ``keep``  returns entries where any key is present *and* drops all other keys; no conditions, but it can remap key names

  .. code-block:: python

    gv.where("x", "y", z=True).print()


Selected operators
------------------

Here is a classification of available operators.

Filtering
^^^^^^^^^

* :func:`~giving.operators.filter`: filter with a function
* :func:`~giving.operators.kfilter`: filter with a function (keyword arguments)
* :func:`~giving.operators.where`: filter based on keys and simple conditions
* :func:`~giving.operators.where_any`: filter based on keys
* :func:`~giving.operators.keep`: filter based on keys (+drop the rest)
* :func:`~giving.operators.distinct`: only emit distinct elements
* :func:`~giving.operators.norepeat`: only emit distinct consecutive elements
* :func:`~giving.operators.first`: only emit the first element
* :func:`~giving.operators.last`: only emit the last element
* :func:`~giving.operators.take`: only emit the first n elements
* :func:`~giving.operators.take_last`: only emit the last n elements
* :func:`~giving.operators.skip`: suppress the first n elements
* :func:`~giving.operators.skip_last`: suppress the last n elements

Mapping
^^^^^^^

* :func:`~giving.operators.map`: map with a function
* :func:`~giving.operators.kmap`: map with a function (keyword arguments)
* :func:`~giving.operators.augment`: add extra keys using a mapping function
* :func:`~giving.operators.getitem`: extract value for a specific key
* :func:`~giving.operators.sole`: extract value from dict of length 1
* :func:`~giving.operators.as_`: wrap as a dict

Reduction
^^^^^^^^^

* :func:`~giving.operators.reduce`: reduce with a function
* :func:`~giving.operators.scan`: emit a result at each reduction step
* :func:`~giving.operators.roll`: reduce using overlapping windows
* :func:`~giving.operators.kmerge`: merge all dictionaries in the stream
* :func:`~giving.operators.kscan`: incremental version of ``kmerge``

Arithmetic reductions
^^^^^^^^^^^^^^^^^^^^^

Most of these reductions can be called with the ``scan`` argument set to ``True`` to use ``scan`` instead of ``reduce``. ``scan`` can also be set to an integer, in which case ``roll`` is used.

* :func:`~giving.operators.average`
* :func:`~giving.operators.average_and_variance`
* :func:`~giving.operators.count`
* :func:`~giving.operators.max`
* :func:`~giving.operators.min`
* :func:`~giving.operators.sum`
* :func:`~giving.operators.variance`

Wrapping
^^^^^^^^

* :meth:`give.wrap()<giving.gvr.Giver.wrap>`: give a special key at the beginning and end of a block
* :meth:`give.wrap_inherit()<giving.gvr.Giver.wrap_inherit>`: give a special key at the beginning and end of a block
* :meth:`give.inherit()<giving.gvr.Giver.inherit>`: add default key/values for every give() in the block
* :func:`given.wrap()<giving.gvn.Given.wrap>`: plug a context manager at the location of a ``give.wrap``
* :func:`given.kwrap()<giving.gvn.Given.kwrap>`: same as wrap, but pass kwargs

Timing
^^^^^^

* :func:`~giving.operators.debounce`: suppress events that are too close in time
* :func:`~giving.operators.sample`: sample an element every n seconds
* :func:`~giving.operators.throttle`: emit at most once every n seconds

Debugging
^^^^^^^^^

* :func:`~giving.gvn.Given.breakpoint`: set a breakpoint whenever data comes in. Use this with filters.
* :func:`~giving.operators.tag`: assigns a special word to every entry. Use with ``breakword``.
* :func:`~giving.gvn.Given.breakword`: set a breakpoint on a specific word set by ``tag``, using the ``BREAKWORD`` environment variable.
* :func:`~giving.gvn.Given.print`: print out the stream.
* :func:`~giving.gvn.Given.display`: print out the stream (pretty).
* :func:`~giving.gvn.Given.accum`: accumulate into a list.
* :func:`~giving.gvn.Given.values`: accumulate into a list (context manager).
* :func:`~giving.gvn.Given.subscribe`: run a task on every element.
* :func:`~giving.gvn.Given.ksubscribe`: run a task on every element (keyword arguments).
