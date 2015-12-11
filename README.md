# KDVS Downloader

![Image of Kool-Aid Man]
(http://www.edinformatics.com/inventions_inventors/Kool-AidMan.jpg)

````
0 9 * * 0 /usr/local/bin/get_kdvs_programming.py -s 'Raise The Dead' -d $(/bin/date --date=yesterday +\%Y-\%m-\%d)
````
````
0 9 * * 2 /usr/local/bin/get_kdvs_programming.py -s 'Caves XL' -d $(/bin/date --date=yesterday +\%Y-\%m-\%d)
````
````
0 9 * * 2 /usr/local/bin/get_kdvs_programming.py -s 'Apartment 5' -d $(/bin/date --date=yesterday +\%Y-\%m-\%d)
````
