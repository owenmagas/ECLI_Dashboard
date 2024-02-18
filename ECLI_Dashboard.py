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

st.set_page_config(page_title='SADC Countries ECLI Dashboard', page_icon = ":globe_with_meridians:", layout = "wide", )
st.markdown("<h1 style='text-align: center;'>SADC COUNTRIES ECLI DASHBOARD</h1>", unsafe_allow_html=True)





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
# cursor.execute("""select d.Year,e.Name, a.CategoryName, a.EcliID,b.QuestionId,  c.QuestionId as QAID,c.DNormalisedWeight,
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
# data3 = cursor.fetchall()
# data_df3 = pd.DataFrame(data3)
data_df3 = pd.read_csv('data_df3.csv')
st.write("Choose your country: ")
country = st.selectbox('Country', options=data_df3['Name'].unique())
left_co, cent_co,last_co = st.columns(3)
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
else:
    with cent_co:        
        st.image("no_image", caption=country) 
    

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

data_df3 = data_df3.query('Name == @country')
if country !='':
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>ECLI PER CATEGORY</h2>", unsafe_allow_html=True)
    
        
    
    
    
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
    # st.write(ls)
    # st.write(ls1)
    # st.write(ls2)
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
        df[j] = df[i]*df['DNormalisedWeight']*8
    # df[ls1] = df[ls1]*8 
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
    
    
    st.sidebar.header('Category Section Filter Here')
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
        df_s1_ = df_s1.style.highlight_between(left=0.0, right = 10.0, color = 'green')\
                        .highlight_between(left=10.0, right = 20.0, color = 'yellow')\
                        .highlight_between(left=30.0, right = 100.0, color = 'orange')\
                        .highlight_between(left=100.0, right = 2000.0, color = 'red')\
                        .format("{:.2f}")\
                        .set_caption('Subcategory ECLI')
        st.table(df_s1_)
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
            height = 800,
            
        )
        st.plotly_chart(fig_df_s, use_container_width=True)
        # st.plotly_chart(fig_df_s)
    except:
        st.markdown("<h3 style='text-align: center;'>You did not select anything</h3>", unsafe_allow_html=True)




















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

    # data_df2.to_csv('data_df2.csv')
    data_df2 = pd.read_csv('data_df2.csv')
    data_df2 = data_df2.query('Name == @country')
    # data_df3.to_csv('samp5.csv')
    # st.dataframe(data_df3)
    # ds =data_df3.columns.tolist()
    ls8 =data_df2.columns.tolist()
    ls5 = ls8[8:19]
    ls6 = ls8[8:19]
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
        df_s9 = df_s8.style.highlight_between(left=0.0, right = 10.0, color = 'green')\
                        .highlight_between(left=10.0, right = 20.0, color = 'yellow')\
                        .highlight_between(left=30.0, right = 100.0, color = 'orange')\
                        .highlight_between(left=100.0, right = 2000.0, color = 'red')\
                        .format("{:.2f}")\
                        .set_caption('Subcategory ECLI')
        st.write(df_s9)



        fig_df_s7 = px.bar(
            df_s7,
            y = 'ECLI',
            x = 'Year',
            color = 'SubCategoryName',
            title = "<b>ECLI by Products</b>",
            barmode = 'group',
            # color_discrete_sequence = ["#0083B8"]*len(df_s7),
            template = "plotly_white"
        )
        fig_df_s7.update_layout(
            xaxis=dict(tickmode="linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
            height = 800,
        )

        # st.plotly_chart(fig_df_s7)
        st.plotly_chart(fig_df_s7, use_container_width=True)
    except:
        st.markdown("<h3 style='text-align: center;'>You did not select anything</h3>", unsafe_allow_html=True)









    #NEW PLOT No. 3

    st.markdown("---")

    st.markdown("<h2 style='text-align: center;'>ECLI PER SECTOR</h2>", unsafe_allow_html=True)

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
    data_df4 = pd.read_csv('data_df4.csv')
    data_df4 = data_df4.query('Name == @country')
    # data_df4.to_csv('data_df4.csv')
    # data_df4 = pd.read_csv('data_df4.csv')
    ls =data_df4.columns.tolist()
    ls3 = (data_df4.filter(like='Index')).columns.tolist()
    ls1 = ls[7:18]
    ls2 = ls[7:18]
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
        "Select question:",
        options = ls2,
        default = ls2
    )
    # st.write(sub_cat)
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
                
        df_selection2 = df_selection2.T.drop_duplicates().T
            
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
                
        df_selection2 = df_selection2.T.drop_duplicates().T
        
    
            
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
        df_selection2 = df_selection2.T.drop_duplicates().T


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
                    .highlight_between(left=10.0, right = 20.0, color = 'yellow')\
                    .highlight_between(left=30.0, right = 100.0, color = 'orange')\
                    .highlight_between(left=100.0, right = 2000.0, color = 'red')\
                    .format("{:.2f}")\
                    .set_caption('Subcategory ECLI')

        st.table(df17)
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
else:
    st.markdown("<h3 style='text-align: center;'>No Country Was Selected</h3>", unsafe_allow_html=True)
    










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
data_df5 = pd.read_csv('data_df5.csv')

data_df5.fillna(0,inplace=True)
ls =data_df5.columns.tolist()
ls3 = (data_df5.filter(like='Index')).columns.tolist()
ls1 = ls[7:19]
ls2 = ls[7:19]
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
sc = ["EServices", "EAppliestoAll", "EResident", "EPaymentOutwards", "EExchangeRateMeasures",\
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
            
    df_selection2 = df_selection2.T.drop_duplicates().T
        
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
            
    df_selection2 = df_selection2.T.drop_duplicates().T
    
   
        
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
    df_selection2 = df_selection2.T.drop_duplicates().T
# df_selection2.columns

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
    # st.write(sub_c)
    sub_c = ['Year','Name',sub_c]
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
        
            df15 = df14.style.highlight_between(left=-0.1, right = 10.0, color = 'green')\
                .highlight_between(left=10.0, right = 20.0, color = 'yellow')\
                .highlight_between(left=30.0, right = 100.0, color = 'orange')\
                .highlight_between(left=100.0, right = 2000.0, color = 'red')\
                .format("{:.2f}")\
                .set_caption('Subcategory ECLI')
                    
            z = df13.columns[2]
        
            st.write(df15)
            
            if year:
                df16 = df13.query(
                    "Year == @year"
                )
            
            fig_df_s16 = px.bar(
            df16,
            y = df13.columns[2] ,
            x = 'Name',
            # color = 'Name',
            title = "<b>ECLI by Products</b>",
            barmode = 'group',
            # color_discrete_sequence = ["#0083B8"]*len(df_s7),
            template = "plotly_white"
            
            )
            fig_df_s16.update_layout(
                xaxis=dict(tickmode="linear"),
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False)),
                height = 800,
            )
            
            # st.plotly_chart(fig_df_s16)
            st.plotly_chart(fig_df_s16, use_container_width=True)
        except:
            st.write("There is no valid data")
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