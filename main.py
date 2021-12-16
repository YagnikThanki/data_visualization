#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from send_email import send_report

raw_data_file = "Data Set 2.csv"
fileToSend = "generated_report.csv"
graph_name = "cohorts_graph.png"
listoffiles = ["generated_report.csv", "cohorts_graph.png"]
    # please allow less secure app permission from security setting of your sender google account

emailto = "tridhyatesting@gmail.com"#"receiver email"
username = "yagnikttridhyatech@gmail.com"
password = "Yagnik@1112"  

def generate_cohornt(final_norm):
    # verage_standard_cost.index = average_standard_cost.index.strftime('%Y-%m')
    # Initialize the figure
    plt.figure(figsize=(16, 10))
    # Adding a title
    plt.title('Average Standard Cost: Monthly Cohorts', fontsize = 14)
    vis_df = final_norm.drop("amount")

    # Creating the heatmap
    sns.heatmap(vis_df, annot = True,vmin = 0.0,cmap="YlGnBu", fmt='g')
    plt.ylabel('Cohort Month')
    plt.xlabel('Cohort Index')
    plt.yticks( rotation='360')
    # plt.show()
    plt.savefig(graph_name)

def main():

    main_df = pd.read_csv(raw_data_file, index_col=False)

    test_df = main_df.copy()
    test_df['total_orders'] = 1

    test_df['created_on'] = pd.to_datetime(main_df.created_on,format='%d-%m-%Y %H:%M')
    # df.ix[]
    # print(test)
    test = test_df.sort_values("created_on")

    user = test.groupby(['customer_id'])['created_on'].min().reset_index()
    user.columns = ['customer_id','order_month']
    user['reg_month'] = user['order_month'].values.astype('datetime64[M]')
    min_month = test['created_on'].values.astype('datetime64[M]').min()
    max_month = test['created_on'].values.astype('datetime64[M]').max()
    dr = pd.DataFrame(pd.date_range(min_month,max_month,freq='MS'))
    dr.columns = ['month']


    dr['key'] = 1
    user['key'] = 1
    report = dr.merge(user,on='key')

    report = report[report['month']>=report['reg_month']]

    test_df['month'] = test_df['created_on'].values.astype('datetime64[M]')
    # df['revenue'] = df['UnitPrice'] * df['Quantity']
    sales_month = test_df.groupby(['customer_id','month'])[['amount']].agg('sum').reset_index()

    sales_month_key = test_df.groupby(['customer_id','month'])[['total_orders']].agg('sum').reset_index()

    report = report.merge(sales_month,how='left',on=['customer_id','month'])
    report = report.merge(sales_month_key,how='left',on=['customer_id','month'])

    report = report[report['amount'].notna()]

    report['user'] = 1
    report['new'] = (report['reg_month'] == report['month']) * 1
    report['active'] = (report['amount'] > 0) * 1

    final_save = report.groupby('month')[['amount','total_orders','user','new','active']].agg('sum')
    final_save = final_save.T
    final_save.to_csv(fileToSend)
    generate_cohornt(final_save)
    send_report(emailto,listoffiles,username,password)


if __name__ == "__main__":
    main()
