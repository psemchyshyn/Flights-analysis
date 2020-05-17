# Flights Detector

### Deplyoed on heroku https://flights-detector-ucu.herokuapp.com/home

## What Flights Detector does?

Flight Detector is created for managing flights of different directions and finding the most beneficial in terms of money and time saving ones. 

The results are presented in user-friendly web-applications(one of them performs alternative flights analysis and the other one - route analysis), which allow to get flights and present them in a shape of graphs and web-maps by indicating the required parameters. You can access the wanted application via the website wrapper, which will navigate you to what information you want to obtain(either alternative flights analysis or route analysis)

**If you choose route analysis, then by entering the names of the origin city and the destination city you will be able: **

* to see the web-map portraying your route
* to explore the table(sorted by price), which will present data about tickets including:

  * the day of departure
  * the return date
  * the date, when the ticket was found
  * the gate, where you can buy this ticket
  * the distance, which covers the found flight
  * the time needed to cover this flight
  * origin and destination city in IATA code
  * the price of the ticket
  
* to see the graph visualizing how the prices fluctuate depending on filter type. Among filters there are(you can choose at once whatever filters you want(they are presented as checkbox)):

  * departure date
  * return date
  * the date, when the ticket was found
  
* to choose the desired price range, by moving the slider of prices

If you chose the city, to which there are no available tickets or the city, which doesn't have an IATA code - you would get just the map (graph and table are going to be empty).

If you didn't choose the origin city or destination city or both, then you wouldn't get a web-map, but the API will perform search finding the cheapest available prices, therefore you will get the graph and table.

[route img]()


**If you choose alternative flights analysis, then by entering the names of the origin city and the destination city and the date you will be able: **

* to see the web-map proposing all alternative directions to the entered destination city
* to get those alternative flights on the bubbled graph(the OY axis will show the distance from origin city to alternative city) and each bubble represents an alternative flight
* by hovering on the wanted bubble toget another graph, which presents additional information about that flight tickets prices.

The same result as in route analysis application you are going to get in this one if you mistype city, doesn't enter it or if there are no flights from it.

[alt img]()


*More information about Flights Detector is on wiki pages* [wiki](https://github.com/psemchyshyn/dz_project/wiki)

***

# Table of contents

### Wiki

* [ДЗ0](https://github.com/psemchyshyn/dz_project/wiki/%D0%94%D0%970)
* [ДЗ1](https://github.com/psemchyshyn/dz_project/wiki/%D0%94%D0%971)
* [ДЗ2](https://github.com/psemchyshyn/dz_project/wiki/%D0%94%D0%972)
* [ДЗ3](https://github.com/psemchyshyn/dz_project/wiki/%D0%94%D0%973)
* [ДЗ4](https://github.com/psemchyshyn/dz_project/wiki/%D0%94%D0%974)
* [ДЗ5](https://github.com/psemchyshyn/dz_project/wiki/%D0%94%D0%975)


***

### Required modules to install

* pip install dash dash-html-components dash-core-components dash-table
* pip install flask
* pip install geopy
* pip install werkzeug
* pip install pandas
* pip install requests
* pip install plotly

To access the API you must pass your token in the X-Access-Token header or in the token parameter. To obtain a token for the Data Access API, go to http://www.travelpayouts.com/developers/api. (**Compulsory**)

***

### Installation

```
$ git clone https://github.com/psemchyshyn/dz_project.git
$ cd dz_project
$ pip install -r requirements.txt
```

***

### Modules

* [retrieve_data.py]()
* [geo.py]
* [manager.py]
* [cities.py]

***

### Examples

***

### Credits

*Pavlo Semchyshyn, Ukrainian Catholic University, 2020*





