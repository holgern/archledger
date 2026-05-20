Source tracking
===============

Snapshots
---------

``snapshot`` stores a baseline of the tracked workspace files:

.. code-block:: bash

   archledger --json snapshot --reason after-archledger-update

Changes
-------

``changed`` compares the current workspace against the stored baseline:

.. code-block:: bash

   archledger --json changed
   archledger --json changed --include-draft

If ``[tracking].enabled = false``, both commands fail explicitly instead of
creating or reading misleading tracking state.
