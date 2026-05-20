Build and export
================

Native builds
-------------

.. code-block:: bash

   archledger build --format markdown
   archledger build --format asciidoc

Converter-backed exports
------------------------

- Markdown source uses ``pandoc`` for HTML, DOCX, RST, Textile, PDF, and AsciiDoc.
- AsciiDoc source uses ``asciidoctor`` for HTML.
- AsciiDoc source uses ``asciidoctor-pdf`` for PDF.
- AsciiDoc source uses Asciidoctor DocBook plus ``pandoc`` for DOCX, Markdown, RST, and Textile.

Source migration
----------------

``convert-sources`` migrates Markdown-source projects to AsciiDoc-source projects.
Write mode is strict by default and requires ``pandoc``:

.. code-block:: bash

   archledger convert-sources --to asciidoc --write

For an explicit temporary mixed-body migration:

.. code-block:: bash

   archledger convert-sources --to asciidoc --write --allow-mixed-body-format
