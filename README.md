##XKCD-Archiver-cli



Now we geeks look some [xkcd](https://xkcd.com/) and go on from checking the site from time to time to amuze outselfs. 

How about you get to download all of the xkcd which have been uploaded till date? This does just that!

##Feautures

- Can download all the xkcd's uploaded till date(1603 as I am writing this!).
- Download individual xkcd's and store them
- Download the latest issue xkcd 
- No duplicacy in your XKCD database. 
- Stores each xckd in a seperate file named as the `title` of the xkcd
- Writes a `description.txt` for each xkcd. Storing meta-data like 
    - `date-publised`
    - url value
    - a small description of that xkcd
- written in `python`. 

##Usage

Will be added soon!

##To-do

- [x] add `xkcd-cli --download-latest`
- [x] add `xkcd-cli --download=XKCDNUMBER`
- [x] add `xkcd-cli --download-all`
- [ ] add `xkcd-cli --start=XKCDNUMBER --end=XKCDNUMBER [--path=/path/to/directory]`
- [ ]Remove redundant code in `download_xkcd_number()`, `download_latest()` and `download_all()`

##Contributing

Feel free to contribute

1. Fork it.
2. Create your feature branch (`git checkout -b my-new-awesome-feature`)
3. Commit your changes (`git commit -am 'Added <xyz> feature'`)
4. Push to the branch (`git push origin my-new-awesome-feature`)
5. Create new Pull Request

##Bugs

Please report the bugs at the [issue tracker](https://github.com/prodicus/xkcd-archiver/issues)

## License :

MIT License [http://prodicus.mit-license.org/](http://prodicus.mit-license.org/) &copy; Tasdik Rahman