
This project demonstrates how to access an RPG backend using python on the front end.

The ./FrontEnd/showTable.py will dump the HTML result to the console
The ./FronEnd/runBottle.py will set up a web server on port 80 that will display the 
HTML table in the browser.

The ./BackEnd/product.rpgle is the RPG program that retrieves the data from DB2 and returns an array of datastructures.
The ./BackEnd/build.sh is a shell script to compile the RPG source.
