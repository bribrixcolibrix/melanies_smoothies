# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 
import requests


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be :', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

max_ing = 6
ingredients_list = st.multiselect(f'Choose up to {max_ing} ingredients: ', my_dataframe,
                                 max_selections=max_ing)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        st.write("https://my.smoothiefroot.com/api/fruit/"+search_on)
        fruityvice_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit order')
    if time_to_insert: 
        session.sql(my_insert_stmt).collect()

        st.success(f'Your Smoothie is ordered, {name_on_order} !', icon="✅")


