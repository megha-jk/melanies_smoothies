# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")

name_on_order = st.text_input("Name on smoothie: ")
st.write("The name on your smoothie will be ", name_on_order)

st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients: ',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''    # initialize to empty string
    # convert list to string using for loop
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

st.write(ingredients_string)

# sql statement
my_insert_stmt = """insert into smoothies.public.orders (name_on_order, ingredients) 
values ('""" + name_on_order + """', '""" + ingredients_string + """');
"""
#st.write(my_insert_stmt)

insert_order = st.button("Place order")

if insert_order:
    session.sql(my_insert_stmt).collect()               # SQL query executed
    message = 'Your Smoothie is ordered, '+name_on_order+'!'
    st.success(message, icon="✅")






