from bs4 import BeautifulSoup
import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as mp
import sqlite3
import pymysql
import sqlalchemy

# Read the CSV file from the cwd(current working directory)
# and convert it to a dataframe
dataframe = pd.read_csv('test-data.csv')


# create a function which will clean the dataframe
# it takes in an argument of data, which will be the
# dataframe we read above
def clean_data(data):
    # removes N/A fields
    data = data.dropna()

    # changes negative ages to positive by ensuring they are absolute values
    data['age'] = data['age'].abs()

    # splits the order month e.g.  from the "-" so from "oct-21" becomes "oct  21"
    # also creates a new column called "month", "year" in which the split string enters
    # column
    data[["month", "Year"]] = data["order_month"].str.split("-", n=1, expand=True)

    # This deletes the column "order_month"
    data.drop("order_month", axis=1, inplace=True)

    # This reformat the string years that state "21" and turns it into "2021"
    data["Year"] = data["Year"].str.replace("21", "2021")

    # This returns the dataframe
    return data

    # Editing the dataframe to total up orders
    # def total_orders(data):
    data = clean_data(data)
    # Group the orders by the product, ensuring the index is remained, while only
    # returning the quantity column


#   total_of_orders = data.groupby(['product'], as_index=False)['quantity'].count()

# def graph_total_orders(data_required):
# Using plotly to graph the dataframe, passing in the dataframe as an argument
#    fig = px.bar(
#       total_of_orders,
#      title='Amount of orders per product',
#     x='product',
#    y='quantity'
# )
# fig.show()

# return graph_total_orders(total_of_orders)

# total_orders(dataframe)

# Toothbrushes outperforms toys
# total_orders(dataframe)


# create a function for the total quantity of products which was sold
def total_quantity(data):
    data = clean_data(data)
    total_quantity_products = data.groupby(['product'], as_index=False)['quantity'].sum()

    # create a function which contains the visualisation of the product and quantity
    def graph_total_quantity(data_required):
        fig = px.bar(
            total_quantity_products,
            title='Quantity of products ordered',
            x='product',
            y='quantity'
        )
        fig.show()

    return graph_total_quantity(total_quantity_products)


# total_quantity(dataframe)

# 39 toothbrushes was purchased whereas, only 27 toys were bought so toothbrushes performed better


# Creating a function which show the quantity of products bought per certain age
# Creating a function which show the quanatity of products bought per area via UK
def demographic_split(data):
    data = clean_data(data)
    age_split = data.groupby(['age'], as_index=False)['quantity'].sum()
    region_split = data.groupby(['uk_region'], as_index=False)['quantity'].sum()

    # Creating a function which show the visualisation of age and regions
    def graph_demographics(data_required):
        age_fig = px.line(
            age_split,
            title='Split by age',
            x='age',
            y='quantity'
        )
        age_fig.show()
        region_fig = px.pie(
            region_split,
            title='Split by region',
            names='uk_region',
            values='quantity'
        )
        region_fig.show()

    return graph_demographics(region_split)


# demographic_split(dataframe)

# Most products were bought by 18 and 35-year-olds whereas, the least products bought was
# done by 45-year-olds

# As for region most products was bought by individuals who live within the UK South East
# as %54.5 of the products were bought by them.
# Whereas, the least was done by South as they bought no products

def seasons(data):
    data = clean_data(data)
    seasons_split = data.groupby(['month'], as_index=False)['quantity'].sum()

    def graph_total_orders(data_required):
        # Using plotly to graph the dataframe, passing in the dataframe as an argument
        fig = px.bar(
            data_required,
            title='Amount of orders per season',
            x='month',
            y='quantity')

        fig.show()

    return graph_total_orders(seasons_split)


# seasons(dataframe)

# From this data it is quite obvious that the sales are infact seasonal as most of the sales
# was completed during Winter/ spring whereas thre was absoloutely no sales completed during the summer

def comparison(data):
    data = clean_data(data)
    area_quantity = data.groupby(["uk_region"], as_index=False)['cpa'].mean()

    def graph_area_quantity(data_required):
        quantity_region_fig = px.bar(
            area_quantity,
            title="amount of order per UK Region",
            x="uk_region",
            y="quantity")
        quantity_region_fig.show()

    return area_quantity


data = dataframe.head()

df = pd.DataFrame(data, columns=["uk_region", 'quantity', "cpa"])

# plot the dataframe
df.plot(x="uk_region", y=["quantity", "cpa"], kind="bar", figsize=(9, 8))

# this prints the bar
#mp.show()
# We see that the quantity is lower than the CPA

# print(comparison(dataframe))

# Here is the webscraping data
source = requests.get("https://mystaticwebsite-3.s3.amazonaws.com/index.html")
source = source.text
soup = BeautifulSoup(source, "html.parser")
# this finds the soup table
table = soup.table
df = pd.read_html(str(table))[0]

# this helps us to remove the £ signs
df['Average CPA by Region'] = df['Average CPA by Region'].str.replace("£", '').astype(float)
# this helps us to rename Region to Uk_region
df = df.rename(columns={"Region": "uk_region"})
# print(df)

# this combines my comparison table with my scraped data
df3 = pd.concat([comparison(dataframe), df], axis=1, join="inner")
print(df3)

df3.plot(kind='bar')
# this helps me to index my x values 0 = South East, 1 = North East....
mp.xticks([0, 1, 2, 3], ['South East', 'North East', 'North', 'South'])
mp.title('CPA Comparison by Region')
mp.ylabel('CPA')
mp.xlabel('Region')
mp.show()

# The CPA is lower on my data than the average cpa.
