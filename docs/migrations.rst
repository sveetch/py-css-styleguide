.. _migrate_intro:

==========
Migrations
==========

From 1.0.0 to 1.1.0
*******************

This is a minor release without incompatible changes, you won't have nothing to do.


From 0.8.x to 1.0.0
*******************

.. Warning::
    Minimal Python version support is ``3.8``. If you are not fulfilling this
    requirement you won't be able to migrate and you should stay with
    ``py-css-styleguide==0.8.3``.

There is the procedure to migrate your manifest keeping the same compiler. If you plan
to migrate also from Libsass compiler to Dart Sass, you will have to read further
section.

#. Upgrade your project to install the new release py-css-styleguide ``1.0.0``;
#. If you were using the :ref:`sassmixins_intro` update it to the last one (you just
   need to overwrite the file in your project);
#. A new meta rule ``styleguide-metas-compiler`` has been introduced to define the
   proper Sass compiler behavior to adopt. Add it at the top of your manifest file
   below the version comment: ::

    .styleguide-metas-compiler {
        --support: "NAME";
    }

   Where ``NAME`` is either ``libsass`` or ``dartsass`` depending the Sass compiler you
   are using. See :ref:`manifest_meta_compiler` for more explanations.
#. All reference must define structure mode variable ``--structure``. Previously the
   mode ``nested`` was the default so all your reference without a structure mode must
   include this: ::

    --structure: "nested";

   Preferably as the first reference variable. You don't need to change references that
   already defined a structure mode.

#. Reference structure ``json`` has been renamed to ``object-complex``, update your
   manifest such as all references with the following line: ::

    --structure: "json";

   Need to be changed to: ::

    --structure: "object-complex";

#. Separator mode ``json-list`` has been renamed to ``object-list``, update your
   manifest such as all references with the following line: ::

    --splitter: "json-list";

   Need to be changed to: ::

    --splitter: "object-list";

#. Finally you need to rebuild the manifest with your Sass compiler (except if you are
   manually writting the CSS manifest);


From Libsass to Dart Sass
-------------------------

All reference using ``--splitter: "object-list"`` need to be updated to use the Dart
Sass syntax on variables, variable value must be double quoted and enclosed content
must be changed to use single quotes only such as: ::

    --items: '["foo", "bar", true, "ping pong"]';

Must become: ::

    --items: "['foo', 'bar', True, 'ping pong']";

.. Note::
    Here we take example of a ``items`` variable but if reference have other variable
    lists, they all need to be updated accordingly.

And all references using ``--structure: "object-complex"`` have to be changed in the
same way. See :ref:`serializer_item_separator_list_dartsass` for explanation.
