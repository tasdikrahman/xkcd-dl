.. figure:: https://raw.githubusercontent.com/prodicus/xkcd-dl/master/assets/logo.png
   :alt: logo


|PyPI version| |License|

Download each and every `xkcd <http://xkcd.com>`__ comic uploaded! Like ever!

:Author: Tasdik Rahman

.. contents::
    :backlinks: none

.. sectnum::


Features
=========

-  Can download all the xkcd's uploaded till date(1603 as I am writing
   this!).
-  Download individual xkcd's and store them
-  Download ranges of xkcd's and store them
-  Download the latest issue xkcd
-  Download the meta text inside each xkcd and store it
-  No duplicacy in your XKCD database.
-  Stores each xkcd in a separate file named as the ``title`` of the
   xkcd at your home directory
-  Writes a ``description.txt`` for each xkcd. Storing meta-data like

   -  ``date-publised``
   -  url value
   -  a small description of that xkcd
   -  The alt text on the comic

-  written in uncomplicated ``python``.

Usage
=====

When running for the first time, do a ``xkcd-dl --update-db``

.. code:: bash

    $ xkcd-dl --update-db
    XKCD link database updated
    Stored it in 'xkcd_dict.json'. You can start downloading your XKCD's!
    Run 'xkcd-dl --help' for more options
    $

``--download-latest``
---------------------

This downloads the last uploaded xkcd comic and stores under the home
directory of the user with a brief description

.. code:: bash

    $ xkcd-dl --download-latest
    Downloading xkcd from 'http://imgs.xkcd.com/comics/flashlights.png' and storing it under '/home/tasdik/xkcd_archive/1603'
    $

If it has been downloaded, will not do anything

This command will work even if you have not run --update-db yet.

``--download=XKCDNUMBER``
-------------------------

Downloads the particular ``XKCDNUMBER``\ (given that it exists and has
not been downloaded already) and stores it in the home directory

.. code:: bash

    $ xkcd-dl --download=143
    Downloading xkcd from 'http://xkcd.com/143/' and storing it under '/home/tasdik/xkcd_archive/143'
    $ xkcd-dl --download=1603
    Downloading xkcd from 'http://xkcd.com/1603/' and storing it under '/home/tasdik/xkcd_archive/1603'
    xkcd  number '1603' has already been downloaded!
    $

``--download-range <START> <END>``
--------------------

Will take two number parameters and download all the xkcd's between
the two, inclusive.

.. code:: bash

    $ xkcd-dl --download-range 32 36
    Downloading xkcd from 'http://xkcd.com/32/' and storing it under '/home/tasdik/xkcd_archive/32'
    Downloading xkcd from 'http://xkcd.com/33/' and storing it under '/home/tasdik/xkcd_archive/33'
    Downloading xkcd from 'http://xkcd.com/34/' and storing it under '/home/tasdik/xkcd_archive/34'
    Downloading xkcd from 'http://xkcd.com/35/' and storing it under '/home/tasdik/xkcd_archive/35'
    Downloading xkcd from 'http://xkcd.com/36/' and storing it under '/home/tasdik/xkcd_archive/36'

``--download-all``
------------------

As the name suggests, will download all the xkcd's uploaded till date
and store them under the home directory of the user.

.. code:: bash

    $ xkcd-dl --download-all
    Downloading all xkcd's Till date!!
    Downloading xkcd from 'http://xkcd.com/1466' and storing it under '/home/tasdik/xkcd_archive/1466'
    Downloading xkcd from 'http://xkcd.com/381' and storing it under '/home/tasdik/xkcd_archive/381'
    Downloading xkcd from 'http://xkcd.com/198' and storing it under '/home/tasdik/xkcd_archive/198'
    Downloading xkcd from 'http://xkcd.com/512' and storing it under '/home/tasdik/xkcd_archive/512'
    Downloading xkcd from 'http://xkcd.com/842' and storing it under '/home/tasdik/xkcd_archive/842'
    Downloading xkcd from 'http://xkcd.com/920' and storing it under '/home/tasdik/xkcd_archive/920'
    ....
    ....

``--path=PATH``
---------------

To use a custom directory to store your xkcd_archive, you can append
--path=./any/path/here to the end of any download method. Absolute and relative
paths work, but the directory must already exist.

.. code:: bash

    $ xkcd-dl --download=3 --path=comic
    Downloading xkcd from 'http://xkcd.com/3/' and storing it under '/home/tasdik/comic/xkcd_archive/3'
    $ xkcd-dl --download-range 54 56 --path=/home/tasdik/xkcd
    Downloading xkcd from 'http://xkcd.com/54/' and storing it under '/home/tasdik/xkcd/xkcd_archive/54'
    Downloading xkcd from 'http://xkcd.com/55/' and storing it under '/home/tasdik/xkcd/xkcd_archive/55'
    Downloading xkcd from 'http://xkcd.com/56/' and storing it under '/home/tasdik/xkcd/xkcd_archive/56'

Demo
====

.. figure:: https://raw.githubusercontent.com/prodicus/xkcd-dl/master/assets/usage.gif
   :alt: Usage

   Usage

Each Comic is stored in it's own individual folder with a
``description.txt`` placed in it. It contains meta-data like -
``img-link`` - ``title`` - ``date-published`` - ``alt``

Here's a little example for the same

.. figure:: https://raw.githubusercontent.com/prodicus/xkcd-dl/master/assets/directory_struc.jpg
   :alt: xkcd\_archive Structure

   xkcd\_archive Structure



Installation
============

Option 1: installing through `pip <https://pypi.python.org/pypi/xkcd-dl>`__ (Suggested way)
-------------------------------------------------------------------------------------------

`pypi package link <https://pypi.python.org/pypi/xkcd-dl>`__

``$ pip3 install xkcd-dl``

If you are behind a proxy

``$ pip3 --proxy [username:password@]domain_name:port install xkcd-dl``

**Note:** If you get ``command not found`` then
``$ sudo apt-get install python3-pip`` should fix that

Option 2: installing from source
--------------------------------

.. code:: bash

    $ git clone https://github.com/prodicus/xkcd-dl.git
    $ cd xkcd-dl/
    $ pip3 install -r requirements.txt
    $ python3 setup.py install

Upgrading
---------

.. code:: bash

    $ pip3 install -U xkcd-dl

Uninstalling
------------

``$ pip3 uninstall xkcd-dl``

For ``Arch`` distributions
--------------------------

Here is the ``AUR`` link for you

-  `Arch package <https://aur4.archlinux.org/packages/xkcd-dl-git/>`__


Help menu:
==========

.. code:: bash

    $ xkcd-dl --help
    Run `xkcd-dl --update-db` if running for the first time.

    Usage:
      xkcd-dl --update-db
      xkcd-dl --download-latest [--path=PATH]
      xkcd-dl --download=XKCDNUMBER [--path=PATH]
      xkcd-dl --downoad-range <START> <END> [--path=PATH]
      xkcd-dl --download-all [--path=PATH]
      xkcd-dl --version
      xkcd-dl (-h | --help)
    Options:
      --update-db   Updates dictionary which stores all xkcd"s till date
      -h --help     Show this screen
      -v --version  Show version 
    $

Contributing
============

**I hacked this up in one night, so its a little messy up there.** Feel free to contribute.

1. Fork it.
2. Create your feature branch
   (``git checkout -b my-new-awesome-feature``)
3. Commit your changes (``git commit -am 'Added <xyz> feature'``)
4. Push to the branch (``git push origin my-new-awesome-feature``)
5. Create new Pull Request

Contributors
------------

Big shout out to

-  `Ian C <https://github.com/GrappigPanda>`__ for fixing issue `#2 <https://github.com/prodicus/xkcd-dl/issues/2>`__ which stopped the download if a title of a comic had a special character in it and `BlitzKraft <https://github.com/BlitzKraft>`__ for pointing it out.
-  `BlitzKraft <https://github.com/BlitzKraft>`__ for adding the feature to download the `alt-text` from the the xkcd **and** major clean ups!
-  `Braden Best <https://github.com/bradenbest>`__ for pointing out the issues when installing from source apart from his valuable input.

To-do
-----

-  [x] add ``xkcd-dl --download-latest``
-  [x] add ``xkcd-dl --download=XKCDNUMBER``
-  [x] add ``xkcd-dl --download-all``
-  [x] add ``xkcd-dl download-range <START> <END>``
-  [x] add path setting with ``[--path=/path/to/directory]`` option
-  [x] add exclude list to easily recognize and ignore dynamic comics
   i.e. comics without a default image.
-  [ ] Remove redundant code in ``download_xkcd_number()``,
   ``download_latest()`` and ``download_all()`` (**Refactoring!!**)
-  [ ] Adding support to open a particular xkcd at the CLI itself.
   (Thinking of using `img2txt <https://github.com/hit9/img2txt>`__ for
   that)


Known Issues
------------

-  There have been issues when installed from source if you are using
   ``python 2.*`` as discussed in
   `#5 <https://github.com/prodicus/xkcd-dl/issues/5#issuecomment-159868497>`__.
   So using ``python3.*`` is suggested.
-  If you get ``command not found`` when installing, it may mean that
   you don't have ``pip3`` installed.
   ``$ sudo apt-get install python3-pip`` should fix that. To check your
   version of pip
-  Dynamic comics have to be added manually using the excludeList

.. code:: bash

    $ pip3 --version
    pip 1.5.6 from /usr/lib/python3/dist-packages (python 3.4)
    $ 


Bugs
----

Please report the bugs at the `issue
tracker <https://github.com/prodicus/xkcd-archiver/issues>`__

**OR**

You can tweet me at `@tasdikrahman <https://twitter.com/tasdikrahman>`__ if you can't get it to work. In fact, you should tweet me anyway.

Motivation
==========

``xkcd-dl`` is inspired by an awesome package called `youtube-dl <https://github.com/rg3/youtube-dl/>`__ written by `Daniel Bolton <https://github.com/rg3>`__ (Much respect!)

How about you get to download all of the xkcd which have been uploaded
till date? This does just that!

Now I don't know about you, but I just love reading ``xkcd``'s! Had a boring Sunday night looming over, thought why not create something like ``youtube-dl`` but for downloading ``xkcd``'s!

And hence `xkcd-dl <https://github.com/prodicus/xkcd-dl>`__

Cheers to a crazy night!

Legal stuff
===========

Built with ♥ by `Tasdik Rahman <http://tasdikrahman.me>`__ `(@tasdikrahman) <https://twitter.com/tasdikrahman>`__ and `others <https://github.com/prodicus/xkcd-dl/graphs/contributors>`__ released under `MIT License <http://prodicus.mit-license.org>`__

You can find a copy of the License at http://prodicus.mit-license.org/


.. |PyPI version| image:: https://badge.fury.io/py/xkcd-dl.svg
   :target: https://badge.fury.io/py/xkcd-dl
.. |License| image:: https://img.shields.io/pypi/l/xkcd-dl.svg
   :target: https://img.shields.io/pypi/l/xkcd-dl.svg
