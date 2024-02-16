from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
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
pd.options.mode.copy_on_write = True

st.set_page_config(page_title='Zimbabwe ECLI Dashboard', page_icon = ":globe_with_meridians:", layout = "wide", )
st.markdown("<h1 style='text-align: center;'>ZIMBABWE ECLI</h1>", unsafe_allow_html=True)




# conn = pymssql.connect(
#     host=r'10.16.65.18',
#     user=r'sa',
#     password=r'Password2010',
#     database='ECLI'
# )

# cursor = conn.cursor(as_dict=True)
# cursor1 = conn.cursor(as_dict=True)
# cursor2 = conn.cursor(as_dict=True)
# cursor3 = conn.cursor(as_dict=True)
# cursor4 = conn.cursor(as_dict=True)


# cursor = conn.cursor(as_dict=True)
# cursor.execute("""select d.Year, a.CategoryName, a.EcliID,b.QuestionId,  c.QuestionId as QAID,c.DNormalisedWeight,
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
#         on c.SurveyId = d.Id""")
# data3 = cursor.fetchall()
# data_df3 = pd.DataFrame(data3)

data_df3 = pd.read_csv('data_df3.csv')

# cursor.execute("""select b.Year, a.Category, a.[Index] as IDX from tblSummary a
# inner join tblSurvey b
# on a.SurveyId = b.Id
# where Month in ('December')""")
# data1 = cursor.fetchall()
# data_df1 = pd.DataFrame(data1)
# data_df1 = data_df1.groupby(['Category','Year']).sum()
# data_df1 =data_df1.reset_index()
# data_df1['IDX']=data_df1['IDX'].astype('float')

# data_df3.to_csv('samp5.csv')
# st.dataframe(data_df3)
# ds =data_df3.columns.tolist()
ls =data_df3.columns.tolist()
ls1 = ls[7:19]
ls2 = ls[7:19]
st.write(ls)
st.write(ls1)
st.write(ls2)
for i in range(len(ls1)):
    ls1[i] = 'dd'+ls1[i]
df = data_df3.copy()
# df.info()
df[ls2]= df[ls2].apply(pd.to_numeric, errors='coerce')
ls3 = (df.filter(like='Index')).columns.tolist()
df[ls3]= df[ls3].apply(pd.to_numeric, errors='coerce')
for i in ls1:
    df[i] = 1
df['DNormalisedWeight']= df['DNormalisedWeight'].apply(pd.to_numeric, errors='coerce')
for i, j in zip(ls2 , ls1):
    df[j] = df[i]*df['DNormalisedWeight']
df[ls1] = df[ls1]*8 
dfs = df.reindex(columns=['Year', 'CategoryName', 'ServicesIndex', 'AppliestoAllIndex', 'ResidentIndex',\
       'PaymentOutwardsIndex', 'ExchangeRateMeasuresIndex', 'NonResidentIndex',\
       'PaymentInwardsIndex', 'FinancialSectorIndex', 'CapitalAccountIndex',\
       'TradeInwardsIndex', 'TradeOutwardsIndex', 'GoodsIndex',\
       'ddExchangeRateMeasures', 'ddServices', 'ddGoods', 'ddFinancialSector',\
       'ddCapitalAccount', 'ddAppliestoAll', 'ddResident', 'ddNonResident',\
       'ddPaymentInwards', 'ddPaymentOutwards', 'ddTradeInwards',\
       'ddTradeOutwards'])
dfs1 = dfs.groupby(['Year','CategoryName']).sum()  
dfs1['TotWeight'] = dfs1[ls1].sum(axis=1)
dfs1['TotalIndex'] = dfs1[ls3].sum(axis=1) 
dfs2 = dfs1.reset_index()
dfs2['ECLI'] =(dfs2['TotalIndex']/dfs2['TotWeight'])*100




df2 = dfs2.copy()
# st.dataframe(df2)


st.sidebar.header('Please Filter Here')
category_name = st.sidebar.multiselect(
    "Select category:",
    options = df2['CategoryName'].unique(),
    default = df2['CategoryName'][0]   
)

# year = st.sidebar.multiselect(
#     "Select question:",
#     options = df2['Year'].unique(),
#     default = df2['Year'][0]  
# )


    
if category_name:
    df_selection = df2.query(
        "CategoryName == @category_name"
        
    )
else:
    df_selection = []


st.title(":bar_chart: ECLI Dashboard")
st.markdown("##")

# st.dataframe(df_selection)
if len(df_selection) >0:
    if((df_selection[ls1].sum()).sum()) >0:
        try:
            total_ecli  = (((df_selection[ls3].sum()).sum())/((df_selection[ls1].sum()).sum()*8))*100
        except:
            print("Nothing to show here")
    else:
        print("No data found")
        
    c = []

    for i in category_name:
        df = df_selection.query("CategoryName == @i")
        if ((df[ls1].sum()).sum())>0:
            c.append((f"ECLI for {i} is {(((((df[ls3].sum()).sum()))/((((df[ls1].sum()).sum()*8))))*100)},\n"))
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.subheader("Total Ecli: ")
        st.subheader(f"Total ECLi is: {total_ecli:,}")

    with right_column:
        st.subheader("Other Ecli: ")
        for i in c:
            st.write(i)
else:
    st.markdown('No data found')

st.markdown("---")

ls4 = ["Year","CategoryName","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
  "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
  "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
  "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards", "ddTotal"]

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



fig_df_s = px.bar(
    df_s,
    x = 'Year',
    y = 'ECLI',
    color = 'CategoryName',
    title = "<b>ECLI by category and year</b>",
    barmode = 'group',
    # color_discrete_sequence = ["#0083B8"]*len(df_s),
    template = "plotly_white", 
)
fig_df_s.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_df_s)

st.markdown("---")

st.markdown("<h2 style='text-align: center;'>Sub Categories</h2>", unsafe_allow_html=True)
# cursor.execute("""select d.Year, a.SubCategoryName, a.EcliID,b.QuestionId,  c.QuestionId as QAID,c.DNormalisedWeight,
# b.ExchangeRateMeasures,b.Services,
#        b.Goods, b.FinancialSector, b.CapitalAccount, b.AppliestoAll,
#        b.Resident, b.NonResident, b.PaymentInwards, b.PaymentOutwards,
#        b.TradeInwards, b.TradeOutwards,c.ServicesIndex,
#        c.AppliestoAllIndex, c.ResidentIndex, c.PaymentOutwardsIndex,
#        c.ExchangeRateMeasuresIndex, c.NonResidentIndex, c.PaymentInwardsIndex,
#        c.FinancialSectorIndex, c.CapitalAccountIndex, c.TradeInwardsIndex,
#        c.TradeOutwardsIndex, c.GoodsIndex   from tblSubCategory a
#         inner join tblQuestion b
#         on a.Id = b.SubCategoryId
#         inner join tblAnswer c
#         on b.QuestionId = c.QuestionId
#         inner join tblSurvey d
#         on c.SurveyId = d.Id""")
# data2 = cursor.fetchall()
# data_df2 = pd.DataFrame(data2)
data_df2 = pd.read_csv('data_df2.csv')

# data_df3.to_csv('samp5.csv')
# st.dataframe(data_df3)
# ds =data_df3.columns.tolist()
ls8 =data_df2.columns.tolist()
ls5 = ls8[7:19]
ls6 = ls8[7:19]
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
    df5[j] = df5[i]*df5['DNormalisedWeight']
df5[ls5] = df5[ls5]*8 
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


st.sidebar.header('Please Filter Here')
subcategory_name = st.sidebar.multiselect(
    "Select category:",
    options = df7['SubCategoryName'].unique(),
    default = df7['SubCategoryName'][0]   
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
    

st.title(":bar_chart: ECLI Dashboard")
st.markdown("##")

# st.dataframe(df_selection)
if len(df_selection7) >0:
    if((df_selection7[ls1].sum()).sum()) >0:
        try:
            total_ecli7  = (((df_selection7[ls7].sum()).sum())/((df_selection7[ls5].sum()).sum()*8))*100
        except:
            print("Nothing to show here")
    else:
        print("No data found")
        
    c1 = []

    for i in subcategory_name:
        df8 = df_selection7.query("SubCategoryName == @i")
        if ((df8[ls5].sum()).sum())>0:
            c1.append((f"ECLI for {i} is {(((((df8[ls7].sum()).sum()))/((((df8[ls5].sum()).sum()*8))))*100)},\n"))
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.subheader("Total Ecli: ")
        st.subheader(f"Total ECLi is: {total_ecli7:,}")

    with right_column:
        st.subheader("Other Ecli: ")
        for i in c1:
            
            st.write(i)
else:
    st.markdown('No data found')
    
st.markdown("---")

ls9 = ["Year","SCategoryName","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
  "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
  "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
  "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards", "ddTotal"]

df_s7 = ((df_selection7.reindex(columns=["Year","SubCategoryName","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
  "NonResidentIndex", "PaymentInwardsIndex", "FinancialSectorIndex", "CapitalAccountIndex", "TradeInwardsIndex", "TradeOutwardsIndex",\
  "GoodsIndex", "ddExchangeRateMeasures", "ddServices", "ddGoods", "ddFinancialSector", "ddCapitalAccount", "ddAppliestoAll",\
  "ddResident", "ddNonResident", "ddPaymentInwards", "ddPaymentOutwards", "ddTradeInwards", "ddTradeOutwards"])).groupby(['Year','SubCategoryName']).sum()).reset_index()
# df_s = df_selection[[]]
df_s7['TotWeight'] = df_s7[ls5].sum(axis=1)
df_s7['TotalIndex'] = df_s7[ls7].sum(axis=1) 
# df_s = dfs1.reset_index()
df_s7['ECLI'] =(df_s7['TotalIndex']/df_s7['TotWeight'])*100



st.dataframe(df_s7)




fig_df_s7 = px.bar(
    df_s7,
    y = 'ECLI',
    x = 'Year',
    color = 'SubCategoryName',
    title = "<b>ECLI by Products</b>",
    barmode = 'group',
    # color_discrete_sequence = ["#0083B8"]*len(df_s7),
    template = "plotly_white",
    width = 1000, height = 600
)
fig_df_s7.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_df_s7)

st.markdown("---")

st.markdown("<h2 style='text-align: center;'>Tables</h2>", unsafe_allow_html=True)

# cursor = conn.cursor(as_dict=True)
# cursor.execute("""select d.Year, a.CategoryName, a.EcliID,b.QuestionId,  c.QuestionId as QAID,c.DNormalisedWeight,
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
#         on c.SurveyId = d.Id """)
# data4 = cursor.fetchall()
# data_df4 = pd.DataFrame(data4)
data_df4 = pd.read_csv('data_df4.csv')
# data_df4.to_csv('data_df4.csv')
# data_df4 = pd.read_csv('data_df4.csv')
ls =data_df4.columns.tolist()
ls3 = (data_df4.filter(like='Index')).columns.tolist()
ls1 = ls[6:18]
ls2 = ls[6:18]
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

sub_cat = st.sidebar.multiselect(
    "Select question:",
    options = ls2,
    default = ls2
)
st.write(sub_cat)
sc = []
for i in sub_cat:
    x = df_s2.columns.str.contains(i)
    for i in range(len(x)):
        if x[i]==True:
            sc.append(df_s2.columns[i])    
if sub_cat:
    sc.insert(0,'Year')
    df_selection2 = df_s2[sc]



# # df_s3.head()
if sub_cat:
    if 'Services' in sub_cat:
        df_selection2['EServices']=(df_selection2.filter(like='Services')[df_selection2.filter(like='Services').columns[0]]/df_selection2.filter(like='Services')[df_selection2.filter(like='Services').columns[1]])*100

            
    if 'AppliestoAll' in sub_cat:
        df_selection2['EAppliestoAll']=(df_selection2.filter(like='AppliestoAll')[df_selection2.filter(like='AppliestoAll').columns[0]]/df_selection2.filter(like='AppliestoAll')[df_selection2.filter(like='AppliestoAll').columns[1]])*100


    if 'Resident' in sub_cat:
        df_selection2['EResident']=(((df_selection2.filter(like='Resident'))[['ResidentIndex', 'ddResident']])[(df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']]).columns[0]]/(df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']])[df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']].columns[1]])*100

    df_selection2 = df_selection2.T.drop_duplicates().T
        
    if 'ExchangeRateMeasures' in sub_cat:
        df_selection2['EExchangeRateMeasure']=((df_selection2.filter(like='ExchangeRateMeasure'))[(df_selection2.filter(like='ExchangeRateMeasure')).columns[0]]/(df_selection2.filter(like='ExchangeRateMeasure'))[(df_selection2.filter(like='ExchangeRateMeasure')).columns[1]])*100
    df_selection2 = df_selection2.T.drop_duplicates().T
        
    if 'NonResident' in sub_cat:
        df_selection2['ENonResident']=(((df_selection2.filter(like='NonResident'))[['NonResidentIndex', 'ddNonResident']])[(df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']]).columns[0]]/(df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']])[df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']].columns[1]])*100


        
    if 'PaymentInwards' in sub_cat:
        df_selection2['EPaymentInwards']=((df_selection2.filter(like='PaymentInwards'))[(df_selection2.filter(like='PaymentInwards')).columns[0]]/(df_selection2.filter(like='PaymentInwards'))[(df_selection2.filter(like='PaymentInwards')).columns[1]])*100

        
    if 'FinancialSector' in sub_cat:
        df_selection2['EFinancialSector']=(df_selection2.filter(like='FinancialSector')[df_selection2.filter(like='FinancialSector').columns[0]]/df_selection2.filter(like='FinancialSector')[df_selection2.filter(like='FinancialSector').columns[1]])*100

        
    if 'CapitalAccount' in sub_cat:
        df_selection2['ECapitalAccount']=(df_selection2.filter(like='CapitalAccount')[df_selection2.filter(like='CapitalAccount').columns[0]]/df_selection2.filter(like='CapitalAccount')[df_selection2.filter(like='CapitalAccount').columns[1]])*100

        
    if ('TradeInwards') in sub_cat:
        df_selection2['ETradeInwards']=(df_selection2.filter(like='TradeInwards')[df_selection2.filter(like='TradeInwards').columns[0]]/df_selection2.filter(like='TradeInwards')[df_selection2.filter(like='TradeInwards').columns[1]])*100

        
    if 'TradeOutwards' in sub_cat:
        df_selection2['ETradeOutwards']=(df_selection2.filter(like='TradeOutwards')[df_selection2.filter(like='TradeOutwards').columns[0]]/df_selection2.filter(like='TradeOutwards')[df_selection2.filter(like='TradeOutwards').columns[1]])*100

        
    if 'Goods' in sub_cat:
        df_selection2['EGoods']=(df_selection2.filter(like='Goods')[df_selection2.filter(like='Goods').columns[0]]/df_selection2.filter(like='Goods')[df_selection2.filter(like='Goods').columns[1]])*100

        
    if 'PaymentOutwards' in sub_cat:
        df_selection2['EPaymentOutwards']=(df_selection2.filter(like='PaymentOutwards')[df_selection2.filter(like='PaymentOutwards').columns[0]]/df_selection2.filter(like='PaymentOutwards')[df_selection2.filter(like='PaymentOutwards').columns[1]])*100


    # duplicate_cols = df_selection2.columns[df_selection2.columns.duplicated()]
    # df_selection2.drop(columns=duplicate_cols, inplace=True)
    # df_selection2 = df_selection2.T.drop_duplicates().T


    # # df_selection2 = df_selection2.T.drop_duplicates().T
    # # df_selection2.to_csv('see.csv')
    if len(df_selection2)>0:
        col_s =['EServices', 'EAppliestoAll', 'EResident','EPaymentInwards', 'EFinancialSector','ENonResident','ECapitalAccount',\
            'ETradeInwards', 'ETradeOutwards', 'EGoods', 'EPaymentOutwards']
        cols = []
        for i in col_s:
            if i in df_selection2.columns:
                cols.append(i)
            

    df_selection2.fillna(0, inplace=True)
    # st.write(df_selection2.columns)
    cols=['Year'] + cols    
    # df13 = df_selection2[cols].apply(pd.to_numeric, errors='coerce')
    df13 = df_selection2[cols]
    
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
    df_selection2_ = df_s2.copy()
    df_selection2_['total_ECLI'] = (df_selection2_[select].sum(axis=1)/df_selection2_[select1].sum(axis=1))*100
    y = df_selection2_['total_ECLI'].to_list()
    df14.insert(1,'total_Ecli',y)
    # df14['total_Ecl'] = y
    # df14.to_csv('df14.csv')

    df15 = df14.transpose()


    df16 = df15.copy()
    # # df15.to_csv('df15.csv')
    # df16.reset_index(inplace=True)
    # df16 = df16.apply(pd.to_numeric, errors='coerce')
    df16.columns = df16.iloc[0]

    df16 = df16[1:]
    # st.dataframe(df16)
    # df16 = df16[~df16.index.duplicated(keep='first')]
    # df16.to_csv('df16.csv')

    df17 = df16.style.highlight_between(left=0.0, right = 10.0, color = 'green')\
                .highlight_between(left=10.0, right = 100.0, color = 'lightblue')\
                .set_caption('Subcategory ECLI')
            


    df17
else:
    select = ['ExchangeRateMeasuresIndex', 'ServicesIndex', 'GoodsIndex', 'FinancialSectorIndex', 'CapitalAccountIndex', 'AppliestoAllIndex']
    select1 = ['ddExchangeRateMeasures', 'ddServices', 'ddGoods', 'ddFinancialSector', 'ddCapitalAccount', 'ddAppliestoAll']
    df_selection2_ = df_s2.copy()
    df_selection2_['total_ECLI'] = (df_selection2_[select].sum(axis=1)/df_selection2_[select1].sum(axis=1))*100
    st.dataframe(df_selection2_[['Year','total_ECLI']])
# st.dataframe(data_df4)
# # multi_select = st.multiselect('Choose Category', options=('2020', '2021','amazon','oracle'))
# # multi_select1 = st.multiselect('Choose Year', options=('MICRosoft', 'Apple','amazon','oracle'))
# # multi_select2 = st.multiselect('Choose Selection', options=('MICRosoft', 'Apple','amazon','oracle'))
# # if multi_select:
# #     df3 = df2[df2['Year']== multi_select]
# #     st.dataframe(df3)

st.markdown("---")


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
#         on e.Id = d.CountryId """)
# data4 = cursor.fetchall()
# data_df4 = pd.DataFrame(data4)
data_df5 = pd.read_csv('data_df5.csv')

ls =data_df5.columns.tolist()
ls3 = (data_df5.filter(like='Index')).columns.tolist()
ls1 = ls[6:18]
ls2 = ls[6:18]
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

df_s2 = ((data_df4.reindex(columns=["Year","Name","ServicesIndex", "AppliestoAllIndex", "ResidentIndex", "PaymentOutwardsIndex", "ExchangeRateMeasuresIndex",\
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

sub_cat = st.sidebar.multiselect(
    "Select question:",
    options = ls2,
    default = ls2
)

# year = st.checkbox(
#     "Chhoose year",
#     options = df_s2['Year'].unique()
# )
year = st.sidebar.selectbox('Year', options=df_s2['Year'].unique())

st.write(sub_cat)
sc = []
for i in sub_cat:
    x = df_s2.columns.str.contains(i)
    for i in range(len(x)):
        if x[i]==True:
            sc.append(df_s2.columns[i])    
if sub_cat:
    sc.insert(0,'Year')
    sc.insert(1,'Name')
    df_selection2 = df_s2[sc]



# # df_s3.head()
if sub_cat:
    if 'Services' in sub_cat:
        df_selection2['EServices']=(df_selection2.filter(like='Services')[df_selection2.filter(like='Services').columns[0]]/df_selection2.filter(like='Services')[df_selection2.filter(like='Services').columns[1]])*100

            
    if 'AppliestoAll' in sub_cat:
        df_selection2['EAppliestoAll']=(df_selection2.filter(like='AppliestoAll')[df_selection2.filter(like='AppliestoAll').columns[0]]/df_selection2.filter(like='AppliestoAll')[df_selection2.filter(like='AppliestoAll').columns[1]])*100


    if 'Resident' in sub_cat:
        df_selection2['EResident']=(((df_selection2.filter(like='Resident'))[['ResidentIndex', 'ddResident']])[(df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']]).columns[0]]/(df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']])[df_selection2.filter(like='Resident')[['ResidentIndex', 'ddResident']].columns[1]])*100

    df_selection2 = df_selection2.T.drop_duplicates().T
        
    if 'ExchangeRateMeasures' in sub_cat:
        df_selection2['EExchangeRateMeasure']=((df_selection2.filter(like='ExchangeRateMeasure'))[(df_selection2.filter(like='ExchangeRateMeasure')).columns[0]]/(df_selection2.filter(like='ExchangeRateMeasure'))[(df_selection2.filter(like='ExchangeRateMeasure')).columns[1]])*100

        
    if 'NonResident' in sub_cat:
        df_selection2['ENonResident']=(((df_selection2.filter(like='NonResident'))[['NonResidentIndex', 'ddNonResident']])[(df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']]).columns[0]]/(df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']])[df_selection2.filter(like='NonResident')[['NonResidentIndex', 'ddNonResident']].columns[1]])*100
        # df_selection2 = df_selection2.T.drop_duplicates().T

        
    if 'PaymentInwards' in sub_cat:
        df_selection2['EPaymentInwards']=((df_selection2.filter(like='PaymentInwards'))[(df_selection2.filter(like='PaymentInwards')).columns[0]]/(df_selection2.filter(like='PaymentInwards'))[(df_selection2.filter(like='PaymentInwards')).columns[1]])*100

        
    if 'FinancialSector' in sub_cat:
        df_selection2['EFinancialSector']=(df_selection2.filter(like='FinancialSector')[df_selection2.filter(like='FinancialSector').columns[0]]/df_selection2.filter(like='FinancialSector')[df_selection2.filter(like='FinancialSector').columns[1]])*100

        
    if 'CapitalAccount' in sub_cat:
        df_selection2['ECapitalAccount']=(df_selection2.filter(like='CapitalAccount')[df_selection2.filter(like='CapitalAccount').columns[0]]/df_selection2.filter(like='CapitalAccount')[df_selection2.filter(like='CapitalAccount').columns[1]])*100

        
    if ('TradeInwards') in sub_cat:
        df_selection2['ETradeInwards']=(df_selection2.filter(like='TradeInwards')[df_selection2.filter(like='TradeInwards').columns[0]]/df_selection2.filter(like='TradeInwards')[df_selection2.filter(like='TradeInwards').columns[1]])*100

        
    if 'TradeOutwards' in sub_cat:
        df_selection2['ETradeOutwards']=(df_selection2.filter(like='TradeOutwards')[df_selection2.filter(like='TradeOutwards').columns[0]]/df_selection2.filter(like='TradeOutwards')[df_selection2.filter(like='TradeOutwards').columns[1]])*100

        
    if 'Goods' in sub_cat:
        df_selection2['EGoods']=(df_selection2.filter(like='Goods')[df_selection2.filter(like='Goods').columns[0]]/df_selection2.filter(like='Goods')[df_selection2.filter(like='Goods').columns[1]])*100

        
    if 'PaymentOutwards' in sub_cat:
        df_selection2['EPaymentOutwards']=(df_selection2.filter(like='PaymentOutwards')[df_selection2.filter(like='PaymentOutwards').columns[0]]/df_selection2.filter(like='PaymentOutwards')[df_selection2.filter(like='PaymentOutwards').columns[1]])*100


    # duplicate_cols = df_selection2.columns[df_selection2.columns.duplicated()]
    # df_selection2.drop(columns=duplicate_cols, inplace=True)
    # df_selection2 = df_selection2.T.drop_duplicates().T


    # # df_selection2 = df_selection2.T.drop_duplicates().T
    # # df_selection2.to_csv('see.csv')
    if len(df_selection2)>0:
        col_s =['ExchangeRateMeasures','EServices', 'EAppliestoAll', 'EResident','EPaymentInwards', 'EFinancialSector','ENonResident','ECapitalAccount',\
            'ETradeInwards', 'ETradeOutwards', 'EGoods', 'EPaymentOutwards']
        cols = []
        for i in col_s:
            if i in df_selection2.columns:
                cols.append(i)
            

    df_selection2.fillna(0, inplace=True)
    # st.write(df_selection2.columns)
    cols=['Year'] +["Name"]+ cols    
    # df13 = df_selection2[cols].apply(pd.to_numeric, errors='coerce')
    df13 = df_selection2[cols]
    df13 = df13.T.drop_duplicates().T
    st.write(df13)
    
    df14 = df13.pivot(index='Name', columns = 'Year', values = df13.columns[2])
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

    df15 = df14.style.highlight_between(left=0.0, right = 10.0, color = 'green')\
                .highlight_between(left=10.0, right = 100.0, color = 'lightblue')\
                .set_caption('Subcategory ECLI')
            
    z = df13.columns[2]

    df15
    
    if year:
        df16 = df13.query(
            "Year == @year"
        )
    
    fig_df_s7 = px.bar(
    df16,
    y = df13.columns[2] ,
    x = 'Name',
    # color = 'Name',
    title = "<b>ECLI by Products</b>",
    barmode = 'group',
    # color_discrete_sequence = ["#0083B8"]*len(df_s7),
    template = "plotly_white",
    width = 1000, height = 600
)
fig_df_s7.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_df_s7)
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