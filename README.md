This project demonstrates how to access an RPG backend using python on the front end.
=======

###Front End
+ `./FrontEnd/showTable.py` will dump the HTML result to the console
+ `./FronEnd/runBottle.py` will set up a web server on port 80 that will display the 
HTML table in the browser.

###Back End
+ `./BackEnd/product.rpgle` is the RPG program that retrieves the data from DB2 and returns an array of datastructures.
+ `./BackEnd/build.sh` is a shell script to compile the RPG source using `system -i`.

###Communication Layer
+ [XmlService](https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/IBM%20i%20Technology%20Updates/page/Python) is used to communicate between the front and the back end.
