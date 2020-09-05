# This Python file uses the following encoding: utf-8
import statsmodels.api as sm
import pandas

df= pandas.read_csv('database.csv', index_col=0, parse_dates=["Date"]).dropna()
df_out= pandas.read_csv('database2.csv', index_col=0, parse_dates=["Date"]).dropna()
if df_out.dropna().empty:
    df_out=df
df_total= df.append(df_out, sort=False).drop_duplicates(subset=["Article"]).dropna()

file= input("Information to process (1:Just the houses on the website; 2: Just the houses already rented; 3: All data available): ")
if file=="1":
    x= df.loc[:,"Parking":"Floor"]
    y= df.loc[:,"Price"]
elif file=="2":
    x= df_out.loc[:,"Parking":"Floor":]
    y= df_out.loc[:,"Price"]
elif file=="3":
    x= df_total.loc[:,"Parking":"Floor"]
    y= df_total.loc[:,"Price"]
else:
    print("Write only available numbers. Reset the program and try again, please")

x= sm.add_constant(x.values)
model= sm.OLS(y,x)
results= model.fit()
print(results.summary())
print()
r_sq= results.rsquared

if r_sq > 0.75:
    print("The information provided is enough to make predictions about the house average rental price. Submit the following information:")
    parking= int(input("Parking (0: NO, 1: YES): "))
    rooms= int(input("Number of rooms: "))
    meters= int(input("Square meters of the entire house: "))
    floor= int(input("Number of floor of the house: "))
    values= [1,parking,rooms,meters,floor]
    f_price= results.predict(values)
    print("The objective rental price of a house or apartment with these features is: {}€/month.".format(round(f_price[0]),2))
else:
    print("The information provided is not enough to make predictions about the house average rental price. Reset the program and submit more information to try it again.")