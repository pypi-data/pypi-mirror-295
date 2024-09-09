from pandas import read_sql

def Create_Offline_file(connection, df, ds_column, man ):       
    #create offline file
    offline_columns= [man, 'Man_code', 'Online Link',
                    'Product URL page', 'File Path',
                    'PDF Source', 'File type',
                    'Task Name', 'Team Name', 'Document Type']

    offline= df[df['Status']=='DONE'].copy()

    offline['File Path']= offline.apply(lambda x: [x['S'], x['L'], x['O']], axis=1)
    offline['Online Link']= offline.apply(lambda x: [None, None, x[ds_column]], axis=1)
    offline['PDF Source']= offline.apply(lambda x: ['Data Sheet', 'Data Sheet', 'Supplier Site'], axis=1)
    offline['Product URL page']= 'N/A'
    offline['File type']= '.jpg'
    offline['Team Name']= 'Design_Support'
    offline['Document Type']= 'Image'

    length= offline.shape[0]
    if length <= 30:
        task_name= "(CS_Urgent_Active)"
    elif length <=150:
        task_name= "(Urgent_Image_NPI)"
    elif length<=500:
        task_name= "(CS_Image_FB)"
    elif length<=1000:
        task_name= "(CS_Special_image)"
    elif length<=3000:
        task_name= "(CS_daily_image)"
    elif length<=5000:
        task_name= "Part_Image_SYS"
    elif length<=10000:
        task_name= "CS_Design_Resources"
    else:
        task_name= "CS_Part_Image"
    offline['Task Name']= task_name

    if connection:
        uni_mans= offline[man].unique()
        if len(uni_mans) == 1:
            mans= tuple(offline[man][:2])
        else:
            mans= tuple(uni_mans)
        query= f"""
        SELECT MAN_NAME, MAN_CODE
        FROM cm.xlp_se_manufacturer
        WHERE MAN_NAME IN {mans}
        """
        man_df= read_sql(query, connection)
        offline['Man_code']= offline[man].apply(
                                        lambda x: man_df['MAN_CODE'][man_df['MAN_NAME']==x].unique()[0] 
                                        if x in man_df['MAN_NAME'].unique() else None   
                                                                )
    else:
        offline['Man_code']= 'Faild To Connect DB'
        print('Note: Faild To Connect DB So Man_Code Doesn\'t Set.')
    offline= offline[offline_columns]
    offline= offline.explode(['Online Link', 'PDF Source' ,'File Path'])
    print('Offline Exported Successfully') 
    return offline
    