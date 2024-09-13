

If you want to pass ``step`` and ``epoch`` to ``log_metrics``, you can do something like this:

.. code-block:: python

    gv["?epoch"] >> experiment.set_epoch
    gv["?step"] >> experiment.set_step


    with give.wrap(mode="train"):
        ...
        with give.inherit(step=step, epoch=epoch):
            ...
            give(train_loss)

    @gv.keep("step", "epoch", "train_loss", "test_loss").ksubscribe
    def _(step, epoch, **metrics):
        experiment.log_metrics(metrics, step=step, epoch=epoch)

Explanations:

* :meth:`~giving.core.Giver.inherit` will make sure that ``step`` and ``epoch`` are given alongside every call to ``give`` inside the block.
* :meth:`~giving.obs.ObservableProxy.ksubscribe` will receive the parameters as keyword arguments, which makes things a bit easier.




def norepeat():
    """Skip entries that are the same as the last.

    .. marble::
        :alt: norepeat

        --1--2--2--1--3--3--3--|
        [      norepeat()      ]
        --1--2-----1--3--------|
    """
    return rxop.pipe(
        rxop.start_with(
            object()
        ),  # Point of comparison for the first element in pairwise
        rxop.pairwise(),
        rxop.filter(lambda pair: pair[0] != pair[1]),
        rxop.pluck(1),
    )
