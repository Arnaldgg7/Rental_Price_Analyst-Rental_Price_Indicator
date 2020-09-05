# Rental_Price_Analyst-Rental_Price_Indicator
These are 2 Python programs aimed to retrieve automatically all information needed about rentals or overall prices of houses in a specific locations, and make predictions from them.

PYTHON PROGRAMS - FUNCTIONALITIES
PROGRAM 1: RENTAL PRICE ANALYST
The Rental Price Analyst program performs the following actions and outcomes:
1. It checks every page of a given URL of an important web portal of houses for rent in a stated
location.

2. It fetches several relevant items of each house, such as price, parking, number of rooms, square
meters or floor, and adds other important items for analysis and handling the data (number of
article and square meter price).

3. It checks the integrity of the data and stores them in a Pandas Dataframe, saving it in a CSV file
(database.csv).

4. It also checks which houses were for rent the previous day and not now, and store them in a
separate file (database2.csv). Therefore, it means that they have been rented, so their prices
are accepted by the market, reason why they are stored in a separated file and it enrich the
afterwards analysis.

5. The program is automatically executed daily, and every last day of each month the program
gather all the information and generates one email with the following:
  a. Monthly statistics about evolution of rentals in the current month:
    i. Monthly average rental price.
    ii. Average of rooms in the offered houses for rent.
    iii. Average of square meters per house of those houses.
    iv. Most usual floor.
    v. If parking is usually included or not.
    vi. Square meter price average in such location.
  
  b. Additionally, the program attaches two graphs about all historical available data (one
  for exclusively see the evolution of every parameter as a picture format, and the other
  for data manipulation in HTML format) and for each database (houses for rent and
  rented houses) with the following information:
    i. Price Mean evolution.
    ii. Price Standard Deviation evolution.
    iii. Square Meter Price evolution.
    iv. Evolution of number of houses for rent.

IMPORTANT: If you want to receive the monthly statistics about market house rental prices, and also the error emails when the
information cannot be fetched, open the program with an IDE and state your emails in the indicated places.
Note: The program stores the data in a CSV format file instead of a SQL database, in order to make the data more accessible for
those people who are not familiar with SQL and want to have the chance to deal with the data in Microsoft Excel, for example.



PROGRAM 2: RENTAL PRICE INDICATOR
Additionally, another Rental Price Indicator program taps into those data by performing a multiple
linear regression model with the aforementioned fetched data items (rooms, square meters, floor, etc)
and allows the user to find the objective right price for rent in such location by providing the features of
the house for which is asking for such information.
