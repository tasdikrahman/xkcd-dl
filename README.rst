XKCD-Archiver-cli
=================

``xkcd-cli`` is inspired by an awesome package called ``youtube-dl``
https://github.com/rg3/youtube-dl/ written by `Daniel
Bolton <https://github.com/rg3>`__\ (Much respect!)

Now I don't know about you, but I just love reading ``xkcd``'s! And So
`xkcd-dl <https://github.com/prodicus/xkcd-dl>`__

I thought why not create something like that but for downloading
``xkcd``'s!

How about you get to download all of the xkcd which have been uploaded
till date? This does just that!

Feautures
=========

-  Can download all the xkcd's uploaded till date(1603 as I am writing
   this!).
-  Download individual xkcd's and store them
-  Download the latest issue xkcd
-  No duplicacy in your XKCD database.
-  Stores each xckd in a seperate file named as the ``title`` of the
   xkcd at your home directory
-  Writes a ``description.txt`` for each xkcd. Storing meta-data like

   -  ``date-publised``
   -  url value
   -  a small description of that xkcd

-  written in ``python``.

Usage
=====

To-do
=====

-  [x] add ``xkcd-cli --download-latest``
-  [x] add ``xkcd-cli --download=XKCDNUMBER``
-  [x] add ``xkcd-cli --download-all``
-  [ ] add
   ``xkcd-cli --start=XKCDNUMBER --end=XKCDNUMBER [--path=/path/to/directory]``
-  [ ] Remove redundant code in ``download_xkcd_number()``,
   ``download_latest()`` and ``download_all()``

Contributing
============

Feel free to contribute

1. Fork it.
2. Create your feature branch
   (``git checkout -b my-new-awesome-feature``)
3. Commit your changes (``git commit -am 'Added <xyz> feature'``)
4. Push to the branch (``git push origin my-new-awesome-feature``)
5. Create new Pull Request

Bugs
====

Please report the bugs at the `issue
tracker <https://github.com/prodicus/xkcd-archiver/issues>`__

License :
=========

MIT License http://prodicus.mit-license.org/ © Tasdik Rahman
