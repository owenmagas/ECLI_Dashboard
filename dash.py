from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import os
from datetime import datetime
import json
import requests
import webbrowser
import msal
import pandas as pd 
import pymssql 
import streamlit as st 
import plotly_express as px 
import numpy as np
from pandasql import sqldf
import panel as pn
pn.extension('tabulator')
import hvplot.pandas 
import holoviews as hv
hv.extension('bokeh')

# code to display headings on the page
st.set_page_config(page_title='SADC Countries ECLI 1 Dashboard', page_icon = ":globe_with_meridians:", layout = "wide", )
st.markdown("<h1 style='text-align: center;'>SADC COUNTRIES ECLI DASHBOARD</h1>", unsafe_allow_html=True)

# cosde to style the background iage of the page
st.markdown("<style>\
            .stAppViewBlockContainer{\
  background-image: url('DRC.png);\
  background-size: cover;\
}\
</style>", unsafe_allow_html=True)

## code to connect to a Microsoft SQL Server database using mssql python library
# conn = pymssql.connect(
#     host=r'ecliproject.database.windows.net',
#     port = '1433',
#     user=r'ecli_sa',
#     password=r'Password2010',
#     database='ECLI'
# )

conn = pymssql.connect(
    host=r'10.16.65.18',
    user=r'sa',
    password=r'Password2010',
    database='ECLI'
)

cursor = conn.cursor(as_dict=True)
cursor1 = conn.cursor(as_dict=True)
cursor2 = conn.cursor(as_dict=True)
cursor3 = conn.cursor(as_dict=True)
cursor4 = conn.cursor(as_dict=True)

# code to run a query on the connected database
cursor = conn.cursor(as_dict=True)
cursor.execute("""select d.Year,e.Name, a.CategoryName,f.SubCategoryName, f.EcliID as SECLiID, a.EcliID,b.QuestionId,  c.QuestionId as QAID,c.DNormalisedWeight,
b.ExchangeRateMeasures,b.Services,
       c.Goods, c.FinancialSector, c.CapitalAccount, c.AppliestoAll,
       c.Resident, c.NonResident, c.PaymentInwards, c.PaymentOutwards,
       c.TradeInwards, c.TradeOutwards,c.ServicesIndex,
       c.AppliestoAllIndex, c.ResidentIndex, c.PaymentOutwardsIndex,
       c.ExchangeRateMeasuresIndex, c.NonResidentIndex, c.PaymentInwardsIndex,
       c.FinancialSectorIndex, c.CapitalAccountIndex, c.TradeInwardsIndex,
       c.TradeOutwardsIndex, c.GoodsIndex   from tblCategory a
        inner join tblQuestion b
        on a.Id = b.CategoryId
        inner join tblAnswer c
        on b.QuestionId = c.QuestionId
        inner join tblSurvey d
        on c.SurveyId = d.Id
        inner join tblCountry e
        on e.Id = d.CountryId
        inner join tblSubCategory f
        on f.Id = b.SubCategoryId""")
data = cursor.fetchall()
ecli = pd.DataFrame(data)

# GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

# def generate_access_token(app_id, scopes):
#     access_token_cache  = msal.SerializableTokenCache()
    
#     #read toke file
#     if os.path.exists('api_token_access.json'):
#         access_token_cache.deserialize(open('api_token_access.json', 'r').read())
#         token_detail = json.load(open('api_token_access.json',))
#         token_detail_key = list(token_detail['AccessToken'].keys())[0]
#         token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
#         if datetime.now() > token_expiration:
#             os.remove('api_token_access.json')
#             access_token_cache = msal.SerializableTokenCache()
#     client = msal.PublicClientApplication(client_id = APP_ID, token_cache = access_token_cache)
#     accounts = client.get_accounts()
#     if accounts:
#         token_response = client.acquire_token_silent(scopes, account = accounts[0])
#     else:
#         flow = client.initiate_device_flow(scopes = SCOPES)
#         print('user code: ' + flow['user_code'])
#         webbrowser.open('https://microsoft.com/devicelogin')
#         token_response = client.acquire_token_by_device_flow(flow)
#         # print(token_response)

#     with open('api_token_access.json', 'w') as f:
#         f.write(access_token_cache.serialize())
#     return token_response



# ecli.to_csv('ecli1.csv', index=False)

#reading saved file form database back into the file
# ecli = pd.read_csv('ecli1.csv')
ecli = ecli.replace(np.nan,0)
ecli.fillna(0, inplace=True)

ls =ecli.columns.tolist()
# ecli[ls[8:32]].info()
ecli[ls[8:33]] = ecli[ls[8:33]].astype(float)
# ecli[ls[8:32]].info()

#replacing none values with zeros


#code to direct user to choose a country and showing options for user to choose
st.write("Choose your country: ")
c = ecli['Name'].unique()
c = list(c)
c.sort()
# st.write(c)
country = st.selectbox('Country', options=c)
left_co, cent_co,last_co = st.columns(3)

#code to display country flag depending oon user choice
if country=='Zimbabwe':
    with cent_co:        
        st.image("Zimbabwe.png", caption='ZIMBABWE') 
        
elif country=='Democratic Republic of the Congo':
    with cent_co:        
        st.image("DRC.png", caption='DRC') 
    
elif country=='Eswatini':
    with cent_co:        
        st.image("Eswatini.png", caption='ESWATINI') 
    
elif country=='Botswana':
    with cent_co:        
        st.image("Botswana.png", caption='BOTSWANA') 
    
elif country=='Lesotho':
    with cent_co:        
        st.image("Lesotho.png", caption='LESOTHO') 
    
elif country=='Malawi':
    with cent_co:        
        st.image("Malawi.png", caption='MALAWI') 
    
elif country=='Mozambique':
    with cent_co:        
        st.image("Mozambique.png", caption='MOZAMBIQUE')
elif country=='Tanzania':
    with cent_co:        
        st.image("Tanzania.png", caption='TANZANIA')
elif country=='South Africa':
    with cent_co:        
        st.image("South_Africa.png", caption='SOUTH AFRICA')
elif country=='Namibia':
    with cent_co:        
        st.image("Namibia.png", caption='NAMIBIA')
elif country=='Angola':
    with cent_co:        
        st.image("Angola.png", caption='ANGOLA')
else:
    with cent_co:        
        st.image(f"{country}.png", caption=country) 
    

# cursor.execute("""select b.Year, a.Category, a.[Index] as IDX from tblSummary a
# inner join tblSurvey b
# on a.SurveyId = b.Id
# where Month in ('December')""")
# data1 = cursor.fetchall()
# data_df1 = pd.DataFrame(data1)
# data_df1 = data_df1.groupby(['Category','Year']).sum()
# data_df1 =data_df1.reset_index()
# data_df1['IDX']=data_df1['IDX'].astype('float')
# data_df3.to_csv('data_df3.csv', index=False)
col1 = st.columns(1)
col2= st.columns(1)

#selct a sub dataframe with data from the slected country
data_df3 = ecli.copy()
data_df3 = data_df3.query('Name == @country')
if country !='':
    st.markdown("---")
    # st.markdown("<h2 style='text-align: center;'>ECLI PER CATEGORY</h2>", unsafe_allow_html=True)
        
    #code to create a list containing dataframe columns
    #and list of subset of the columns
    ls =data_df3.columns.tolist()
    ls1 = ls[9:21]
    ls2 = ls[9:21]
    
    #encoding columns to change their names
    for i in range(len(ls1)):
        ls1[i] = 'dd'+ls1[i]
    df = data_df3.copy()
    # df.info()
    #converting non-numeric alues to numeric
    # df[ls2]= df[ls2].apply(pd.to_numeric, errors='coerce')
    
    #selecting a subset of columns which have Index in their name
    ls3 = (df.filter(like='Index')).columns.tolist()
    # df[ls3]= df[ls3].apply(pd.to_numeric, errors='coerce')
    
    #setting a subset of colums to an initial value of 1
    for i in ls1:
        df[i] = 1
        
    #
    df['DNormalisedWeight']= df['DNormalisedWeight'].apply(pd.to_numeric, errors='coerce')
    #calculating wigthed values and populate the dataframe
    for i, j in zip(ls2 , ls1):
        df[j] = df[i]*df['DNormalisedWeight']*8
    # df[ls1] = df[ls1]*8 
    
    #selecting a subset of columns to assigne to a new dataframe  
    dfs = df.reindex(columns=['Year', 'CategoryName', 'ServicesIndex', 'AppliestoAllIndex', 'ResidentIndex',\
           'PaymentOutwardsIndex', 'ExchangeRateMeasuresIndex', 'NonResidentIndex',\
           'PaymentInwardsIndex', 'FinancialSectorIndex', 'CapitalAccountIndex',\
           'TradeInwardsIndex', 'TradeOutwardsIndex', 'GoodsIndex',\
           'ddExchangeRateMeasures', 'ddServices', 'ddGoods', 'ddFinancialSector',\
           'ddCapitalAccount', 'ddAppliestoAll', 'ddResident', 'ddNonResident',\
           'ddPaymentInwards', 'ddPaymentOutwards', 'ddTradeInwards',\
           'ddTradeOutwards'])
    
    #grouping and summing columns vertically basing on the year and category
    dfs1 = dfs.groupby(['Year','CategoryName']).sum()  
    
    #creating weights and index as a sum of the individual columns
    dfs1['TotWeight'] = dfs1[ls1].sum(axis=1)
    dfs1['TotalIndex'] = dfs1[ls3].sum(axis=1) 
    dfs2 = dfs1.reset_index()
    dfs2['ECLI'] =(dfs2['TotalIndex']/dfs2['TotWeight'])*100
    
    
    
    
    df2 = dfs2.copy()
    # st.dataframe(df2)
    
    
    st.sidebar.header('Category Section Filter Here')
    category_name = st.sidebar.multiselect(
        "Select category:",
        options = df2['CategoryName'].unique(),
        default = df2['CategoryName']  
    ) 
    
        
    if category_name:
        df_selection = df2.query(
            "CategoryName == @category_name"
            
        )
    else:
        df_selection = []
    
    
    # st.title(":bar_chart: ECLI Dashboard")
    st.markdown("##")
    
    # st.dataframe(df_selection)
    # if len(df_selection) >0:
    #     if((df_selection[ls1].sum()).sum()) >0:
    #         try:           
    #             total_ecli  = ((df_selection['TotalIndex'].sum())/(df_selection['TotWeight'].sum()))*100
    #         except:            
    #             total_ecli = 0
    #     else:
    #         print("No data found")
            
    #     c = []
    
    #     for i in category_name:
            
    #         df = df_selection.query("CategoryName == @i")
    #         if (df[ls1].sum()).sum()>0:
    #             c.append((f"ECLI for {i} is {(((((df[ls3].sum()).sum()))/((((df[ls1].sum()).sum()))))*100)},\n"))
    #     left_column, right_column = st.columns(2)
        
    #     with left_column:
            
    #         st.subheader(f"Total ECLi is: {total_ecli:}")
    
    #     with right_column:
            
    #         for i in c:
    #             st.write(i)
    # else:
    #     st.markdown('No data found')
    
    st.markdown("---")
    
    ls4 = ["Year","CategoryName","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
      "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
      "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
      "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards", "ddTotal"]
    
    try:
        df_s = ((df_selection.reindex(columns=["Year","CategoryName","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
        "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
        "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
        "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards"])).groupby(['Year','CategoryName']).sum()).reset_index()
        # df_s = df_selection[[]]
    
        
        df_s['TotWeight'] = df_s[ls1].sum(axis=1)
        df_s['TotalIndex'] = df_s[ls3].sum(axis=1) 
        # df_s = dfs1.reset_index()
        df_s['ECLI'] =(df_s['TotalIndex']/df_s['TotWeight'])*100
    
    
    
        # df_s1 = df_selection1.groupby(['Year','Category']).sum().reset_index()
    
        # df_s1 = ((df_s[["Year","CategoryName","ECLI_Index"]]))
        # df_s2 = df_s1.pivot(index = 'CategoryName', columns = 'Year', values = 'ECLI_Index')
    
        df_s1 = df_s[["Year","CategoryName",'ECLI']]
        # st.dataframe(df_s1)
        df_s1 = df_s1.pivot(index = 'CategoryName', values='ECLI', columns = 'Year')
        df_s1_ = df_s1.style.highlight_between(left=0.0, right = 10.1, color = 'green')\
                        .highlight_between(left=10.1, right = 20.1, color = 'orange')\
                        .highlight_between(left=20.1, right = 30.1, color = 'yellow')\
                        .highlight_between(left=30.1, right = 100.0, color = 'red')\
                        .format("{:.2f}")
        st.markdown("<h3 style='text-align: center;'>MAIN CATEGORY ECLIs</h3>", unsafe_allow_html=True)
        st.table(df_s1_)
        # fig_df_s = px.bar(
        #     df_s,
        #     x = 'Year',
        #     y = 'ECLI',
        #     color = 'CategoryName',
        #     title = "<b>ECLI by category and year</b>",
        #     barmode = 'group',
        #     # color_discrete_sequence = ["#0083B8"]*len(df_s),
        #     template = "plotly_white", 
        # )
        # fig_df_s.update_layout(
        #     xaxis=dict(tickmode="linear"),
        #     plot_bgcolor="rgba(0,0,0,0)",
        #     yaxis=(dict(showgrid=False)),
        #     height = 800,
            
        # )
        # st.plotly_chart(fig_df_s, use_container_width=True)
        # st.plotly_chart(fig_df_s)
    except:
        st.warning("No Main Category ECLIs to show: You did not select anything")




















    #NEW PLOT No. 2





    st.markdown("---")


    st.markdown("<h2 style='text-align: center;'>ECLI PER SUBCATEGORY</h2>", unsafe_allow_html=True)
    # cursor.execute("""select d.Year,e.Name, a.SubCategoryName, a.EcliID,b.QuestionId,  c.QuestionId as QAID,c.DNormalisedWeight,
    # b.ExchangeRateMeasures,b.Services,
    #     b.Goods, b.FinancialSector, b.CapitalAccount, b.AppliestoAll,
    #     b.Resident, b.NonResident, b.PaymentInwards, b.PaymentOutwards,
    #     b.TradeInwards, b.TradeOutwards,c.ServicesIndex,
    #     c.AppliestoAllIndex, c.ResidentIndex, c.PaymentOutwardsIndex,
    #     c.ExchangeRateMeasuresIndex, c.NonResidentIndex, c.PaymentInwardsIndex,
    #     c.FinancialSectorIndex, c.CapitalAccountIndex, c.TradeInwardsIndex,
    #     c.TradeOutwardsIndex, c.GoodsIndex   from tblSubCategory a
    #         inner join tblQuestion b
    #         on a.Id = b.SubCategoryId
    #         inner join tblAnswer c
    #         on b.QuestionId = c.QuestionId
    #         inner join tblSurvey d
    #         on c.SurveyId = d.Id
    #         inner join tblCountry e
    #         on e.Id = d.CountryId""")
    # data2 = cursor.fetchall()
    # data_df2 = pd.DataFrame(data2)

    # data_df2.to_csv('data_df2.csv', index=False)
    # data_df2 = pd.read_csv('data_df2.csv')
    # data_df2 = data_df2.replace(np.nan,0)
    data_df2 = ecli.copy()
    data_df2 = data_df2.query('Name == @country')
    # data_df3.to_csv('samp5.csv')
    # st.dataframe(data_df3)
    # ds =data_df3.columns.tolist()
    ls8 =data_df2.columns.tolist()
    ls5 = ls8[9:21]
    ls6 = ls8[9:21]
    for i in range(len(ls5)):
        ls5[i] = 'dd'+ls5[i]
    df5 = data_df2.copy()
    # df.info()
    df5[ls6]= df5[ls6].apply(pd.to_numeric, errors='coerce')
    ls7 = (df5.filter(like='Index')).columns.tolist()
    df5[ls7]= df5[ls7].apply(pd.to_numeric, errors='coerce')
    for i in ls5:
        df5[i] = 1
    df5['DNormalisedWeight']= df5['DNormalisedWeight'].apply(pd.to_numeric, errors='coerce')
    for i, j in zip(ls6 , ls5):
        df5[j] = df5[i]*df5['DNormalisedWeight']*8

    dfs5 = df5.reindex(columns=['Year', 'SubCategoryName', 'ServicesIndex', 'AppliestoAllIndex', 'ResidentIndex',\
        'PaymentOutwardsIndex', 'ExchangeRateMeasuresIndex', 'NonResidentIndex',\
        'PaymentInwardsIndex', 'FinancialSectorIndex', 'CapitalAccountIndex',\
        'TradeInwardsIndex', 'TradeOutwardsIndex', 'GoodsIndex',\
        'ddExchangeRateMeasures', 'ddServices', 'ddGoods', 'ddFinancialSector',\
        'ddCapitalAccount', 'ddAppliestoAll', 'ddResident', 'ddNonResident',\
        'ddPaymentInwards', 'ddPaymentOutwards', 'ddTradeInwards',\
        'ddTradeOutwards'])
    dfs6 = dfs5.groupby(['Year','SubCategoryName']).sum()  
    dfs6['TotWeight'] = dfs6[ls5].sum(axis=1)
    dfs6['TotalIndex'] = dfs6[ls7].sum(axis=1) 
    dfs7 = dfs6.reset_index()
    dfs7['ECLI'] =(dfs7['TotalIndex']/dfs7['TotWeight'])*100




    df7 = dfs7.copy()
    # st.dataframe(df2)


    st.sidebar.header('SubCategory Section Filter Here')
    subcategory_name = st.sidebar.multiselect(
        "Select SubCategory:",
        options = df7['SubCategoryName'].unique(),
        default = df7['SubCategoryName']  
    )

    # year = st.sidebar.multiselect(
    #     "Select question:",
    #     options = df2['Year'].unique(),
    #     default = df2['Year'][0]  
    # )



    if subcategory_name:
        df_selection7 = df7.query(
            "SubCategoryName == @subcategory_name"
            
        )
    else:
        df_selection7 = []
        

    # st.title(":bar_chart: ECLI Dashboard")
    st.markdown("##")

    # st.dataframe(df_selection)
    # if len(df_selection7) >0:
    #     if((df_selection7[ls5].sum()).sum()) >0:
    #         try:
    #             total_ecli7  = ((df_selection7['TotalIndex'].sum())/(df_selection7['TotWeight'].sum()))*100
    #         except:
    #             total_ecli7 = 0
    #     else:
    #         print("No data found")
            
    #     c1 = []

    #     for i in subcategory_name:
    #         df8 = df_selection7.query("SubCategoryName == @i")
    #         if ((df8[ls5].sum()).sum())>0:
    #             c1.append((f"ECLI for {i} is {(((((df8[ls7].sum()).sum()))/((((df8[ls5].sum()).sum()))))*100)},\n"))
    #     left_column, right_column = st.columns(2)
        
    #     with left_column:
    #         st.subheader("Total Ecli: ")
    #         st.subheader(f"Total ECLi is: {total_ecli7:,}")

    #     with right_column:
    #         st.subheader("Other Ecli: ")
    #         for i in c1:
                
    #             st.write(i)
    # else:
    #     st.markdown('No data found')
        
    st.markdown("---")

    ls9 = ["Year","SCategoryName","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
    "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
    "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
    "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards", "ddTotal"]
    try:
        df_s7 = ((df_selection7.reindex(columns=["Year","SubCategoryName","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
        "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
        "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
        "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards"])).groupby(['Year','SubCategoryName']).sum()).reset_index()
        # df_s = df_selection[[]]
        df_s7['TotWeight'] = df_s7[ls5].sum(axis=1)
        df_s7['TotalIndex'] = df_s7[ls7].sum(axis=1) 
        # df_s = dfs1.reset_index()
        df_s7['ECLI'] =(df_s7['TotalIndex']/df_s7['TotWeight'])*100



        # st.dataframe(df_s7)
        df_s7 = df_s7[["Year","SubCategoryName",'ECLI']]
        # st.dataframe(df_s1)
        df_s8 = df_s7.pivot(index = "SubCategoryName", values='ECLI', columns = 'Year')
        df_s9 = df_s8.style.highlight_between(left=0.0, right = 10.1, color = 'green')\
                        .highlight_between(left=10.1, right = 20.1, color = 'orange')\
                        .highlight_between(left=20.1, right = 30.1, color = 'yellow')\
                        .highlight_between(left=30.1, right = 100.0, color = 'red')\
                        .format("{:.2f}")
                        
        st.markdown("<h3 style='text-align: center;'>SUBCATEGORY ECLIs</h3>", unsafe_allow_html=True)
        st.table(df_s9)
        df_s7.to_csv('file1.csv')


        # fig_df_s7 = px.bar(
        #     df_s7,
        #     y = 'ECLI',
        #     x = 'Year',
        #     color = 'SubCategoryName',
        #     title = "<b>ECLI by Products</b>",
        #     barmode = 'group',
        #     # color_discrete_sequence = ["#0083B8"]*len(df_s7),
        #     template = "plotly_white"
        # )
        # fig_df_s7.update_layout(
        #     xaxis=dict(tickmode="linear"),
        #     plot_bgcolor="rgba(0,0,0,0)",
        #     yaxis=(dict(showgrid=False)),
        #     height = 800,
        # )

        # st.plotly_chart(fig_df_s7)
        st.plotly_chart(fig_df_s7, use_container_width=True)
    except:
        st.warning("No subcategory ECLIs to show: You did not select anything")









    #NEW PLOT No. 3

    st.markdown("---")

    st.markdown("<h2 style='text-align: center;'>ECLI PER SECTOR</h2>", unsafe_allow_html=True)
    left = st.columns(1)
    left = st.columns(1)
    # cursor = conn.cursor(as_dict=True)
    # cursor.execute("""select d.Year,e.Name, a.CategoryName, a.EcliID,b.QuestionId,  c.QuestionId as QAID,c.DNormalisedWeight,
    # b.ExchangeRateMeasures,b.Services,
    #     b.Goods, b.FinancialSector, b.CapitalAccount, b.AppliestoAll,
    #     b.Resident, b.NonResident, b.PaymentInwards, b.PaymentOutwards,
    #     b.TradeInwards, b.TradeOutwards,c.ServicesIndex,
    #     c.AppliestoAllIndex, c.ResidentIndex, c.PaymentOutwardsIndex,
    #     c.ExchangeRateMeasuresIndex, c.NonResidentIndex, c.PaymentInwardsIndex,
    #     c.FinancialSectorIndex, c.CapitalAccountIndex, c.TradeInwardsIndex,
    #     c.TradeOutwardsIndex, c.GoodsIndex   from tblCategory a
    #     inner join tblQuestion b
    #     on a.Id = b.CategoryId
    #     inner join tblAnswer c
    #     on b.QuestionId = c.QuestionId
    #     inner join tblSurvey d
    #     on c.SurveyId = d.Id 
    #     inner join tblCountry e
    #     on e.Id = d.CountryId""")
    # data4 = cursor.fetchall()
    # data_df4 = pd.DataFrame(data4)

    # data_df4.to_csv('data_df4.csv', index=False)
    # data_df4 = pd.read_csv('data_df4.csv')
    # data_df4 = data_df4.replace(np.nan,0)
    # data_df4.to_csv('data_df4.csv', index=False)
    data_df4 = ecli.copy()
    data_df4 = data_df4.query('Name == @country')
    # data_df4.to_csv('data_df4.csv')
    # data_df4 = pd.read_csv('data_df4.csv')
    ls =data_df4.columns.tolist()
    ls3 = (data_df4.filter(like='Index')).columns.tolist()
    ls1 = ls[9:21]
    ls2 = ls[9:21]
    for i in range(len(ls1)):
        ls1[i] = 'dd'+ls1[i]
    data_df4[ls2]= data_df4[ls2].apply(pd.to_numeric, errors='coerce')
    ls3 = (data_df4.filter(like='Index')).columns.tolist()
    data_df4[ls3]= data_df4[ls3].apply(pd.to_numeric, errors='coerce')
    for i in ls1:
        data_df4[i] = 1
    data_df4['DNormalisedWeight']= data_df4['DNormalisedWeight'].apply(pd.to_numeric, errors='coerce')
    
    for i, j in zip(ls2 , ls1):
        data_df4[j] = data_df4[i]*data_df4['DNormalisedWeight']*8
        
    data_df4['TotWeight'] = data_df4[ls1].sum(axis=1)
    data_df4['TotalIndex'] = data_df4[ls3].sum(axis=1)
    
    df_s2 = ((data_df4.reindex(columns=["Year","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
    "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
    "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
    "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards",'TotWeight','TotalIndex',]))).groupby(["Year"]).sum().reset_index()

    # # df_s3 = (df_s.reindex(columns=["CategoryName",'TotWeight','TotalIndex']))

    # # sub_cat = st.sidebar.multiselect(
    # #     "Select question:",
    # #     options = ls2,
    # #     default = ls2
    # # )
    # # sub_cat = ['Year', 'ExchangeRateMeasures', 'Services', 'Goods', 'FinancialSector', 'CapitalAccount', 'AppliestoAll', 'Resident',\
    # #        'NonResident', 'PaymentInwards', 'PaymentOutwards', 'TradeInwards','TradeOutwards',]
    select = ['ExchangeRateMeasures', 'Services', 'Goods', 'FinancialSector', 'CapitalAccount', 'AppliestoAll']

    st.sidebar.header('Sector Section Filter Here')

    sub_cat = st.sidebar.multiselect(
        "Select Sector:",
        options = ls2,
        default = ls2
    )
    # st.write(sub_cat)
    sc = []
    for i in sub_cat:
        x = df_s2.columns.str.contains(i)
        for j in range(len(x)):
            if x[j]==True:
                y = df_s2.columns[j]
                if y not in sc:
                    sc.append(y)
    
    
         
    
    if sub_cat:
        sc.insert(0,'Year')
        df_selection2 = df_s2[sc]


    df_selection2.to_csv('data_df.csv', index=False)
    # # df_s3.head()
    if len(sub_cat)>0:
        if 'Services' in sub_cat:
            try:
                df_selection2['EServices']=(df_selection2.filter(like='Services')[df_selection2.filter(like='Services').columns[0]]/df_selection2.filter(like='Services')[df_selection2.filter(like='Services').columns[1]])*100
            except:
                df_selection2['EServices']=0

                
        if 'AppliestoAll' in sub_cat:
            
            try:
                df_selection2['EAppliestoAll']=(df_selection2.filter(like='AppliestoAll')[df_selection2.filter(like='AppliestoAll').columns[0]]/df_selection2.filter(like='AppliestoAll')[df_selection2.filter(like='AppliestoAll').columns[1]])*100
            except:
                df_selection2['EAppliestoAll']=0

        if 'Resident' in sub_cat:
            try:
                df_selection2['EResident']=(((df_selection2.filter(like='Resident'))[['ResidentIndex', 'ddResident']])[(df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']]).columns[0]]/(df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']])[df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']].columns[1]])*100
            except:
                df_selection2['EResident']=0
                
        # df_selection2 = df_selection2.T.drop_duplicates().T
            
        if 'ExchangeRateMeasures' in sub_cat:
            try:
                df_selection2['EExchangeRateMeasure']=((df_selection2.filter(like='ExchangeRateMeasure'))[(df_selection2.filter(like='ExchangeRateMeasure')).columns[0]]/(df_selection2.filter(like='ExchangeRateMeasure'))[(df_selection2.filter(like='ExchangeRateMeasure')).columns[1]])*100
            except:
                df_selection2['EExchangeRateMeasure']=0
            
        if 'NonResident' in sub_cat:
            try:
                df_selection2['ENonResident']=(((df_selection2.filter(like='NonResident'))[['NonResidentIndex', 'ddNonResident']])[(df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']]).columns[0]]/(df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']])[df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']].columns[1]])*100
            except:
                df_selection2['ENonResident']=0
                
        # df_selection2 = df_selection2.T.drop_duplicates().T
        
    
            
        if 'PaymentInwards' in sub_cat:
            try:
                df_selection2['EPaymentInwards']=((df_selection2.filter(like='PaymentInwards'))[(df_selection2.filter(like='PaymentInwards')).columns[0]]/(df_selection2.filter(like='PaymentInwards'))[(df_selection2.filter(like='PaymentInwards')).columns[1]])*100
            except:
                df_selection2['EPaymentInwards']=0

            
        if 'FinancialSector' in sub_cat:
            try:
                df_selection2['EFinancialSector']=(df_selection2.filter(like='FinancialSector')[df_selection2.filter(like='FinancialSector').columns[0]]/df_selection2.filter(like='FinancialSector')[df_selection2.filter(like='FinancialSector').columns[1]])*100
            except:
                df_selection2['EFinancialSector']=0

            
        if 'CapitalAccount' in sub_cat:
            try:
                df_selection2['ECapitalAccount']=(df_selection2.filter(like='CapitalAccount')[df_selection2.filter(like='CapitalAccount').columns[0]]/df_selection2.filter(like='CapitalAccount')[df_selection2.filter(like='CapitalAccount').columns[1]])*100
            except:
                df_selection2['ECapitalAccount']=0
            
        if ('TradeInwards') in sub_cat:
            try:
                df_selection2['ETradeInwards']=(df_selection2.filter(like='TradeInwards')[df_selection2.filter(like='TradeInwards').columns[0]]/df_selection2.filter(like='TradeInwards')[df_selection2.filter(like='TradeInwards').columns[1]])*100
            except:
                df_selection2['ETradeInwards']=0

            
        if 'TradeOutwards' in sub_cat:
            try:
                df_selection2['ETradeOutwards']=(df_selection2.filter(like='TradeOutwards')[df_selection2.filter(like='TradeOutwards').columns[0]]/df_selection2.filter(like='TradeOutwards')[df_selection2.filter(like='TradeOutwards').columns[1]])*100
            except:
                df_selection2['ETradeOutwards']=0

            
        if 'Goods' in sub_cat:
            try:
                df_selection2['EGoods']=(df_selection2.filter(like='Goods')[df_selection2.filter(like='Goods').columns[0]]/df_selection2.filter(like='Goods')[df_selection2.filter(like='Goods').columns[1]])*100
            except:
                df_selection2['EGoods']=0
            
        if 'PaymentOutwards' in sub_cat:
            try:
                df_selection2['EPaymentOutwards']=(df_selection2.filter(like='PaymentOutwards')[df_selection2.filter(like='PaymentOutwards').columns[0]]/df_selection2.filter(like='PaymentOutwards')[df_selection2.filter(like='PaymentOutwards').columns[1]])*100
            except:
                df_selection2['EPaymentOutwards'] = 0
        # df_selection2 = df_selection2.T.drop_duplicates().T
        
        # df_selection2.to_csv('data_df1.csv', index=False)


        # duplicate_cols = df_selection2.columns[df_selection2.columns.duplicated()]
        # df_selection2.drop(columns=duplicate_cols, inplace=True)
        # df_selection2 = df_selection2.T.drop_duplicates().T


        # # df_selection2 = df_selection2.T.drop_duplicates().T
        # # df_selection2.to_csv('see.csv')
        # df_selection2.columns
        if len(df_selection2)>0:
            col_s =['EExchangeRateMeasure','EServices', 'EAppliestoAll', 'EResident','EPaymentInwards', 'EFinancialSector','ENonResident','ECapitalAccount',\
                'ETradeInwards', 'ETradeOutwards', 'EGoods', 'EPaymentOutwards']
            cols = []
            for i in col_s:
                if i in df_selection2.columns:
                    cols.append(i)
                

        df_selection2.fillna(0, inplace=True)
        # st.write(df_selection2.columns)
        cols1=['Year'] + cols 
        # cols1   
        # df13 = df_selection2[cols].apply(pd.to_numeric, errors='coerce')
        df13 = df_selection2[cols1]
        # df13
        # df13.to_csv('df_sel.csv')
        # # cols1.insert(0,'Year')
        
        # # cols = ['EServices', 'EAppliestoAll',  'EResident', 'EExchangeRateMeasure','ENonResident', 'EPaymentInwards', \
        # #                              'EFinancialSector',  'ECapitalAccount', 'ETradeInwards', 'ETradeOutwards', 'EGoods', 'EPaymentOutwards']
        # # df13[cols] = df13[cols].apply(pd.to_numeric, errors='coerce')
        # # df14 = df13[['Year', 'EServices', 'EAppliestoAll',  'EResident', 'EExchangeRateMeasure','ENonResident', 'EPaymentInwards', \
        # #                              'EFinancialSector',  'ECapitalAccount', 'ETradeInwards', 'ETradeOutwards', 'EGoods', 'EPaymentOutwards']]
        df14 = df13.copy()
        select = ['ExchangeRateMeasuresIndex', 'ServicesIndex', 'GoodsIndex', 'FinancialSectorIndex', 'CapitalAccountIndex', 'AppliestoAllIndex']
        select1 = ['ddExchangeRateMeasures', 'ddServices', 'ddGoods', 'ddFinancialSector', 'ddCapitalAccount', 'ddAppliestoAll']
        # df_s2
        df_selection2_ = df_s2.copy()
        df_selection2_['total_ECLI'] = (df_selection2_[select].sum(axis=1)/df_selection2_[select1].sum(axis=1))*100
        # df_selection2_
        y = df_selection2_['total_ECLI'].to_list()
        # df14
        df14.insert(1,'total_Ecli',y)
        # df14['total_Ecl'] = y
        # df14.to_csv('df14.csv')

        df15 = df14.transpose()
        # df15

        df16 = df15.copy()
        # # df15.to_csv('df15.csv')
        # df16.reset_index(inplace=True)
        # df16 = df16.apply(pd.to_numeric, errors='coerce')
        df16.columns = df16.iloc[0]

        df16 = df16[1:]
        # st.dataframe(df16)
        # df16 = df16[~df16.index.duplicated(keep='first')]
        # df16.to_csv('df16.csv')

        df17 = df16.style.highlight_between(left=0.0, right = 10.1, color = 'green')\
                        .highlight_between(left=10.1, right = 20.1, color = 'orange')\
                        .highlight_between(left=20.1, right = 30.1, color = 'yellow')\
                        .highlight_between(left=30.1, right = 100.0, color = 'red')\
                        .format("{:.2f}")\
                        .set_caption('Subcategory ECLI')
        df16.to_csv('file2.csv')
                    
        st.markdown("<h3 style='text-align: center;'>ECLI PER SECTOR</h3>", unsafe_allow_html=True)
        st.table(df17)
    else:
        select = ['ExchangeRateMeasuresIndex', 'ServicesIndex', 'GoodsIndex', 'FinancialSectorIndex', 'CapitalAccountIndex', 'AppliestoAllIndex']
        select1 = ['ddExchangeRateMeasures', 'ddServices', 'ddGoods', 'ddFinancialSector', 'ddCapitalAccount', 'ddAppliestoAll']
        df_selection2_ = df_s2.copy()
        df_selection2_['total_ECLI'] = (df_selection2_[select].sum(axis=1)/df_selection2_[select1].sum(axis=1))*100
        # dfs2 = df_selection2_.transpose()
        dfs2 = df_selection2_[['Year','total_ECLI']].transpose()
        dfs3 =dfs2.style.style.highlight_between(left=0.0, right = 10.1, color = 'green')\
                        .highlight_between(left=10.1, right = 20.1, color = 'orange')\
                        .highlight_between(left=20.1, right = 30.1, color = 'yellow')\
                        .highlight_between(left=30.1, right = 100.0, color = 'red')\
                        .format("{:.2f}")
        st.markdown("<h3 style='text-align: center;'>ECLI PER SECTOR</h3>", unsafe_allow_html=True)
        st.table(dfs3)
    # st.dataframe(data_df4)
    # # multi_select = st.multiselect('Choose Category', options=('2020', '2021','amazon','oracle'))
    # # multi_select1 = st.multiselect('Choose Year', options=('MICRosoft', 'Apple','amazon','oracle'))
    # # multi_select2 = st.multiselect('Choose Selection', options=('MICRosoft', 'Apple','amazon','oracle'))
    # # if multi_select:
    # #     df3 = df2[df2['Year']== multi_select]
    # #     st.dataframe(df3)
else:
    st.warning("No Sector ECLIs to show: No valid selection was done")
    






## Table 5
# x = ecli['CategoryName'].unique().tolist()
# df
df_sub = ((df.reindex(columns=["Year","Name","CategoryName","SubCategoryName","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
  "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
  "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
  "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards",'TotWeight','TotalIndex',]))).groupby(["Year","Name","CategoryName","SubCategoryName"]).sum().reset_index()
df_sub  = df_sub.query('Name == @country')

df_sub['TotWeight'] = df_sub[ls1].sum(axis=1)
df_sub['TotalIndex'] = df_sub[ls3].sum(axis=1) 
# df_sub
df_sub1 = df_sub.reset_index()
df_sub1['ECLI'] =(df_sub1['TotalIndex']/df_sub1['TotWeight'])*100
df_sub1 = df_sub1.query(
                    "CategoryName == @category_name"
                )
df_sub2 = df_sub1[["Year","CategoryName","SubCategoryName",'ECLI']]
        # st.dataframe(df_s1)
df_sub2 = df_sub2.pivot(index = ['CategoryName', 'SubCategoryName'], values='ECLI', columns = 'Year')
df_sub2_ = df_sub2.style.highlight_between(left=0.0, right = 10.1, color = 'green')\
                        .highlight_between(left=10.1, right = 20.1, color = 'orange')\
                        .highlight_between(left=20.1, right = 30.1, color = 'yellow')\
                        .highlight_between(left=30.1, right = 100.0, color = 'red')\
                        .format("{:.2f}")
df_sub1.to_csv('file3.csv')
                        
st.dataframe(df_sub2_)









#NEW PLOT No. 4


st.markdown("---")

st.markdown("<h2 style='text-align: center;'>ECLI PER COUNTRY</h2>", unsafe_allow_html=True)
# cursor = conn.cursor(as_dict=True)
# cursor.execute("""select d.Year, e.Name, a.CategoryName, a.EcliID,b.QuestionId,  c.QuestionId as QAID,c.DNormalisedWeight,
# b.ExchangeRateMeasures,b.Services,
#        b.Goods, b.FinancialSector, b.CapitalAccount, b.AppliestoAll,
#        b.Resident, b.NonResident, b.PaymentInwards, b.PaymentOutwards,
#        b.TradeInwards, b.TradeOutwards,c.ServicesIndex,
#        c.AppliestoAllIndex, c.ResidentIndex, c.PaymentOutwardsIndex,
#        c.ExchangeRateMeasuresIndex, c.NonResidentIndex, c.PaymentInwardsIndex,
#        c.FinancialSectorIndex, c.CapitalAccountIndex, c.TradeInwardsIndex,
#        c.TradeOutwardsIndex, c.GoodsIndex   from tblCategory a
#         inner join tblQuestion b
#         on a.Id = b.CategoryId
#         inner join tblAnswer c
#         on b.QuestionId = c.QuestionId
#         inner join tblSurvey d
#         on c.SurveyId = d.Id 
#         inner join tblCountry e
#         on e.Id = d.CountryId""")
# data5 = cursor.fetchall()
# data_df5 = pd.DataFrame(data5)

# data_df5.to_csv('data_df5.csv', index=False)
# data_df5 = pd.read_csv('data_df5.csv')
data_df5 = ecli.copy()

data_df5 = data_df5.replace(np.nan,0)
# data_df5.fillna(0,inplace=True)
ls =data_df5.columns.tolist()
ls3 = (data_df5.filter(like='Index')).columns.tolist()
ls1 = ls[9:21]
ls2 = ls[9:21]
for i in range(len(ls1)):
    ls1[i] = 'dd'+ls1[i]
data_df5[ls2]= data_df5[ls2].apply(pd.to_numeric, errors='coerce')
ls3 = (data_df5.filter(like='Index')).columns.tolist()
data_df5[ls3]= data_df5[ls3].apply(pd.to_numeric, errors='coerce')
for i in ls1:
    data_df5[i] = 1
data_df5['DNormalisedWeight']= data_df5['DNormalisedWeight'].apply(pd.to_numeric, errors='coerce')
for i, j in zip(ls2 , ls1):
    data_df5[j] = data_df5[i]*data_df5['DNormalisedWeight']*8
   
data_df5['TotWeight'] = data_df5[ls1].sum(axis=1)
data_df5['TotalIndex'] = data_df5[ls3].sum(axis=1)
# st.dataframe(data_df5)
df_s2 = ((data_df5.reindex(columns=["Year","Name","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
  "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
  "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
  "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards",'TotWeight','TotalIndex',]))).groupby(["Year","Name"]).sum().reset_index()

# # df_s3 = (df_s.reindex(columns=["CategoryName",'TotWeight','TotalIndex']))

# # sub_cat = st.sidebar.multiselect(
# #     "Select question:",
# #     options = ls2,
# #     default = ls2
# # )
# # sub_cat = ['Year', 'ExchangeRateMeasures', 'Services', 'Goods', 'FinancialSector', 'CapitalAccount', 'AppliestoAll', 'Resident',\
# #        'NonResident', 'PaymentInwards', 'PaymentOutwards', 'TradeInwards','TradeOutwards',]
select = ['ExchangeRateMeasures', 'Services', 'Goods', 'FinancialSector', 'CapitalAccount', 'AppliestoAll']

# sub_cat = st.sidebar.multiselect(
#     "Select question:",
#     options = ls2,
#     default = ls2
# )
sc = ["EServices", "EAppliestoAll", "EResident", "EPaymentOutwards", "EExchangeRateMeasure",\
  "ENonResident", "EPaymentInwards", "EFinancialSector", "ECapitalAccount", "ETradeInwards", "ETradeOutwards",\
  "EGoods"]
# st.write(sc)
# year = st.checkbox(
#     "Chhoose year",
#     options = df_s2['Year'].unique()
# )
st.sidebar.header('Country Section Filter Here')
year = st.sidebar.selectbox('Year', options=df_s2['Year'].unique())
sub_c = st.sidebar.selectbox('Sub_Cat', options=sc)
# # st.write(sub_cat)
# sc = []
# for i in sub_cat:
#     x = df_s2.columns.str.contains(i)
#     for i in range(len(x)):
#         if x[i]==True:
#             sc.append(df_s2.columns[i])    

sub_cat = ['Year']+['Name']+ls2
# sub_cat
# df_s2

df_selection2 = df_s2.copy()
# # df_s3.head()
# sub_cat
# df_selection2
if len(sub_cat)>0:
    
    if 'Services' in sub_cat:
        try:
            df_selection2['EServices']=(df_selection2.filter(like='Services')[df_selection2.filter(like='Services').columns[0]]/df_selection2.filter(like='Services')[df_selection2.filter(like='Services').columns[1]])*100
        except:
            df_selection2['EServices']=0

            
    if 'AppliestoAll' in sub_cat:
        
        try:
            df_selection2['EAppliestoAll']=(df_selection2.filter(like='AppliestoAll')[df_selection2.filter(like='AppliestoAll').columns[0]]/df_selection2.filter(like='AppliestoAll')[df_selection2.filter(like='AppliestoAll').columns[1]])*100
        except:
            df_selection2['EAppliestoAll']=0

    if 'Resident' in sub_cat:
        try:
            # df_selection2.drop(columns=['EResident'], inplace=True)
            df_selection2['EResident']=(((df_selection2.filter(like='Resident'))[['ResidentIndex', 'ddResident']])[(df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']]).columns[0]]/(df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']])[df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']].columns[1]])*100
        except:
            df_selection2['EResident']=0
            
        
        
    if 'ExchangeRateMeasures' in sub_cat:
        try:
            df_selection2['EExchangeRateMeasure']=((df_selection2.filter(like='ExchangeRateMeasure'))[(df_selection2.filter(like='ExchangeRateMeasure')).columns[0]]/(df_selection2.filter(like='ExchangeRateMeasure'))[(df_selection2.filter(like='ExchangeRateMeasure')).columns[1]])*100
        except:
            df_selection2['EExchangeRateMeasure']=0
        
    if 'NonResident' in sub_cat:
        try:
            # df_selection2.drop(columns=['ENonResident'], inplace=True)
            df_selection2['ENonResident']=(((df_selection2.filter(like='NonResident'))[['NonResidentIndex', 'ddNonResident']])[(df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']]).columns[0]]/(df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']])[df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']].columns[1]])*100
        except:
            df_selection2['ENonResident']=0
        
        # df_selection2
            
        
    
   
        
    if 'PaymentInwards' in sub_cat:
        try:
            df_selection2['EPaymentInwards']=((df_selection2.filter(like='PaymentInwards'))[(df_selection2.filter(like='PaymentInwards')).columns[0]]/(df_selection2.filter(like='PaymentInwards'))[(df_selection2.filter(like='PaymentInwards')).columns[1]])*100
        except:
            df_selection2['EPaymentInwards']=0

        
    if 'FinancialSector' in sub_cat:
        try:
            df_selection2['EFinancialSector']=(df_selection2.filter(like='FinancialSector')[df_selection2.filter(like='FinancialSector').columns[0]]/df_selection2.filter(like='FinancialSector')[df_selection2.filter(like='FinancialSector').columns[1]])*100
        except:
            df_selection2['EFinancialSector']=0

        
    if 'CapitalAccount' in sub_cat:
        try:
            df_selection2['ECapitalAccount']=(df_selection2.filter(like='CapitalAccount')[df_selection2.filter(like='CapitalAccount').columns[0]]/df_selection2.filter(like='CapitalAccount')[df_selection2.filter(like='CapitalAccount').columns[1]])*100
        except:
            df_selection2['ECapitalAccount']=0
        
    if ('TradeInwards') in sub_cat:
        try:
            df_selection2['ETradeInwards']=(df_selection2.filter(like='TradeInwards')[df_selection2.filter(like='TradeInwards').columns[0]]/df_selection2.filter(like='TradeInwards')[df_selection2.filter(like='TradeInwards').columns[1]])*100
        except:
            df_selection2['ETradeInwards']=0

        
    if 'TradeOutwards' in sub_cat:
        try:
            df_selection2['ETradeOutwards']=(df_selection2.filter(like='TradeOutwards')[df_selection2.filter(like='TradeOutwards').columns[0]]/df_selection2.filter(like='TradeOutwards')[df_selection2.filter(like='TradeOutwards').columns[1]])*100
        except:
            df_selection2['ETradeOutwards']=0

        
    if 'Goods' in sub_cat:
        try:
            df_selection2['EGoods']=(df_selection2.filter(like='Goods')[df_selection2.filter(like='Goods').columns[0]]/df_selection2.filter(like='Goods')[df_selection2.filter(like='Goods').columns[1]])*100
        except:
            df_selection2['EGoods']=0
        
    if 'PaymentOutwards' in sub_cat:
        try:
            df_selection2['EPaymentOutwards']=(df_selection2.filter(like='PaymentOutwards')[df_selection2.filter(like='PaymentOutwards').columns[0]]/df_selection2.filter(like='PaymentOutwards')[df_selection2.filter(like='PaymentOutwards').columns[1]])*100
        except:
            df_selection2['EPaymentOutwards'] = 0
    # df_selection2 = df_selection2.T.drop_duplicates().T
    # df_selection2

    # duplicate_cols = df_selection2.columns[df_selection2.columns.duplicated()]
    # df_selection2.drop(columns=duplicate_cols, inplace=True)
    # df_selection2 = df_selection2.T.drop_duplicates().T


    # # df_selection2 = df_selection2.T.drop_duplicates().T
    # # df_selection2.to_csv('see.csv')
    if len(df_selection2)>0:
        col_s =['EExchangeRateMeasure','EServices', 'EAppliestoAll', 'EResident','EPaymentInwards', 'EFinancialSector','ENonResident','ECapitalAccount',\
            'ETradeInwards', 'ETradeOutwards', 'EGoods', 'EPaymentOutwards']
        cols = []
        for i in col_s:
            if i in df_selection2.columns:
                cols.append(i)
    # df_selection2.columns        
    # cols
    df_selection2.fillna(0, inplace=True)
    # st.write(df_selection2.columns)
    cols=['Year'] +["Name"]+ cols    
    # df13 = df_selection2[cols].apply(pd.to_numeric, errors='coerce')
    df13 = df_selection2[cols]
    # df13
    df13 = df13.T.drop_duplicates().T
    # df13
    # st.write(sub_c)
    sub_c = ['Year','Name',sub_c]
    # sub_c
    # sub_c.insert(0,'Year')
    # sub_c.insert(1,'Name')
    if len(sub_c)>0:
        try:
            df13_1 = df13[sub_c]
            # if sub_c:
            #     df13_1 = df13[['Year']+['Name']+sub_c]
            # st.write(df13_1)
            
            df14 = df13_1.pivot(index='Name', columns = 'Year', values = df13_1.columns[2])
            # df14
            # df13.to_csv('df_sel.csv')
            # # cols1.insert(0,'Year')
            
            # # cols = ['EServices', 'EAppliestoAll',  'EResident', 'EExchangeRateMeasure','ENonResident', 'EPaymentInwards', \
            # #                              'EFinancialSector',  'ECapitalAccount', 'ETradeInwards', 'ETradeOutwards', 'EGoods', 'EPaymentOutwards']
            # # df13[cols] = df13[cols].apply(pd.to_numeric, errors='coerce')
            # # df14 = df13[['Year', 'EServices', 'EAppliestoAll',  'EResident', 'EExchangeRateMeasure','ENonResident', 'EPaymentInwards', \
            # #                              'EFinancialSector',  'ECapitalAccount', 'ETradeInwards', 'ETradeOutwards', 'EGoods', 'EPaymentOutwards']]
            # df14 = df13.copy()
            # select = ['ExchangeRateMeasuresIndex', 'ServicesIndex', 'GoodsIndex', 'FinancialSectorIndex', 'CapitalAccountIndex', 'AppliestoAllIndex']
            # select1 = ['ddExchangeRateMeasures', 'ddServices', 'ddGoods', 'ddFinancialSector', 'ddCapitalAccount', 'ddAppliestoAll']
            # df_selection2_ = df_s2.copy()
            # df_selection2_['total_ECLI'] = (df_selection2_[select].sum(axis=1)/df_selection2_[select1].sum(axis=1))*100
            # y = df_selection2_['total_ECLI'].to_list()
            # df14.insert(2,'total_Ecli',y)
            # # df14['total_Ecl'] = y
            # # df14.to_csv('df14.csv')
        
            # df15 = df14.transpose()
            # st.write(df15)
            # # df15 = df15.pivot(columns = 'Name')
        
            # df16 = df15.copy()
            # # # df15.to_csv('df15.csv')
            # # df16.reset_index(inplace=True)
            # # df16 = df16.apply(pd.to_numeric, errors='coerce')
            # df16.columns = df16.iloc[0]
        
            # df16 = df16[1:]
            # # st.dataframe(df16)
            # # df16 = df16[~df16.index.duplicated(keep='first')]
            # # df16.to_csv('df16.csv')
        
            df15 = df14.style.highlight_between(left=0.0, right = 10.1, color = 'green')\
                        .highlight_between(left=10.1, right = 20.1, color = 'orange')\
                        .highlight_between(left=20.1, right = 30.1, color = 'yellow')\
                        .highlight_between(left=30.1, right = 100.0, color = 'red')\
                        .format("{:.2f}")
            df14.to_csv('file4.csv')
                    
            z = df13.columns[2]

            st.markdown("<h3 style='text-align: center;'>COUNTRY ECLIs PER SECTOR</h3>", unsafe_allow_html=True)
            st.table(df15)
            
            if year:
                df16 = df13_1.query(
                    "Year == @year"
                )
            # df13_1
            # fig_df_s16 = px.bar(
            # df16,
            # y = df13_1.columns[2] ,
            # x = 'Name',
            # # color = 'Name',
            # title = "<b>ECLIs PER COUNTRY BY SECTOR</b>",
            # barmode = 'group',
            # # color_discrete_sequence = ["#0083B8"]*len(df_s7),
            # template = "plotly_white"
            
            # )
            # fig_df_s16.update_layout(
            #     xaxis=dict(tickmode="linear"),
            #     plot_bgcolor="rgba(0,0,0,0)",
            #     yaxis=(dict(showgrid=False)),
            #     height = 800,
            # )
            
            # # st.plotly_chart(fig_df_s16)
            # st.plotly_chart(fig_df_s16, use_container_width=True)
        except:
            st.warning("No Country ECLIs to show: There is no valid data")
# else:
#     select = ['ExchangeRateMeasuresIndex', 'ServicesIndex', 'GoodsIndex', 'FinancialSectorIndex', 'CapitalAccountIndex', 'AppliestoAllIndex']
#     select1 = ['ddExchangeRateMeasures', 'ddServices', 'ddGoods', 'ddFinancialSector', 'ddCapitalAccount', 'ddAppliestoAll']
#     df_selection2_ = df_s2.copy()
#     df_selection2_['total_ECLI'] = (df_selection2_[select].sum(axis=1)/df_selection2_[select1].sum(axis=1))*100
#     st.dataframe(df_selection2_[['Year','total_ECLI']])
# st.dataframe(data_df4)
# # multi_select = st.multiselect('Choose Category', options=('2020', '2021','amazon','oracle'))
# # multi_select1 = st.multiselect('Choose Year', options=('MICRosoft', 'Apple','amazon','oracle'))
# # multi_select2 = st.multiselect('Choose Selection', options=('MICRosoft', 'Apple','amazon','oracle'))
# # if multi_select:
# #     df3 = df2[df2['Year']== multi_select]
# #     st.dataframe(df3)

# APP_ID = '4562dbbd-c2c6-4785-9309-aab7427b5d4d'
# SCOPES  = ['Files.ReadWrite']

# access_token = generate_access_token(APP_ID, SCOPES)

# headers = {
#     'Authorization' :'Bearer' + access_token['access_token']
    
# }

# file_path = r'file4.csv'
# file_name = os.path.basename(file_path)
# with open(file_path,'rb') as upload:
#     media_content = upload.read()

# response  = requests.put(
#     GRAPH_API_ENDPOINT + f'/me/drive/items/root:/{file_name}:/content',
#     headers = headers,
#     data = media_content
# )

# file_path1 = r'file1.csv'
# file_name1 = os.path.basename(file_path1)
# with open(file_path1,'rb') as upload:
#     media_content = upload.read()

# response  = requests.put(
#     GRAPH_API_ENDPOINT + f'/me/drive/items/root:/{file_name1}:/content',
#     headers = headers,
#     data = media_content
# )

# file_path2 = r'file2.csv'
# file_name2 = os.path.basename(file_path2)
# with open(file_path2,'rb') as upload:
#     media_content = upload.read()

# response  = requests.put(
#     GRAPH_API_ENDPOINT + f'/me/drive/items/root:/{file_name2}:/content',
#     headers = headers,
#     data = media_content
# )

# file_path3 = r'file3.csv'
# file_name3 = os.path.basename(file_path3)
# with open(file_path3,'rb') as upload:
#     media_content = upload.read()

# response  = requests.put(
#     GRAPH_API_ENDPOINT + f'/me/drive/items/root:/{file_name3}:/content',
#     headers = headers,
#     data = media_content
# )
#print(response.json())

dfs16, df_sub1, df_s7, df_s1