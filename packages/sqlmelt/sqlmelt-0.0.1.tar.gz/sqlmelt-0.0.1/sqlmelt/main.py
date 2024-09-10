def melt(dict_measure):

    
    # Функция для чтения и формирования фильтров
    def read_filters(x,y):
    #----------------
        filters = ''
        f_filters = x.iloc[0]
        p_filters = y.iloc[0]
    #----------------    
        try:
            ff = f_filters.split(';')
            for f in ff:
                filters = filters + '\n' + '  AND ' + f
        except:
            one = 1
    #----------------
        try:
            pf = p_filters.split(';')
            for f in pf:
                filters = filters + '\n' + '  AND ' + f
        except:
            one = 1
    #----------------
        return filters
    
    
    # Функция задающая поля агрегации для пивотов
    def agg_creater(x):
        agg_columns_tech = []
        for i in x:
            tech = '       ' + i + ','
            agg_columns_tech.append(tech)
        agg_col = '\n'.join(agg_columns_tech)
        return agg_col
    
    
    # Функция наводящая красоту в аутпуте работы готового скрипта
    def query_runner(query):
        for index in query.split(';'):
            if index != '':
                print(f'''
    [bold red]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Выполнение запроса:[/bold red]
    {index}
                       ''')
                pd.read_sql_query(index, engine)
    
    #кейс для даты
    log_d_case = '''CASE
             --
             WHEN ActionTypeComb_adj IN ('y301y302y401n402n403',
                                         'y301y302y401y403n402',
                                         'y301y302y402y401',
                                         'y301y401n302n402',
                                         'y301y401y402n403n302n700',
                                         'y301y401y402n403n302n700_loss',
                                         'y301y401y402n403n302y700',
                                         'y301y401y403n402n302n700',
                                         'y301y401y403n402n302n700_loss',
                                         'y301y401y403n402n302y700') 
             THEN (YEAR(FactDate_401)||'-'||(MONTH(FactDate_401))::VARCHAR(10)||'-1')::date
             --
             WHEN ActionTypeComb_adj IN ('only_301_loss',
                                         'y301y1101_loss',
                                         'y301y700') 
             THEN (YEAR(Losses_date)||'-'||(MONTH(Losses_date))::VARCHAR(10)||'-1')::date
             --
             WHEN ActionTypeComb_adj = 'y301y302n402n401' 
             THEN (YEAR(FactDate_302)||'-'||(MONTH(FactDate_302))::VARCHAR(10)||'-1')::date
             --
           END AS FactDate,'''
    
    log_d = '''Log_D_accrual_date AS FactDate,'''
    
    #кейс для даты
    log_r_case = '''CASE
             --
             WHEN ActionTypeComb_adj IN ('y301y302n402n401',
                                         'y301y302y401n402n403',
                                         'y301y302y401y403n402',
                                         'y301y302y402y401') 
             THEN (YEAR(FactDate_302)||'-'||(MONTH(FactDate_302))::VARCHAR(10)||'-1')::date
             --
             WHEN ActionTypeComb_adj IN ('y301y1101_loss',
                                         'y301y401y402n403n302n700_loss',
                                         'y301y401y402n403n302y700',
                                         'y301y401y403n402n302n700_loss',
                                         'y301y401y403n402n302y700') 
             THEN (YEAR(Losses_date)||'-'||(MONTH(Losses_date))::VARCHAR(10)||'-1')::date
             --
           END AS FactDate,'''
    
    log_r = '''Log_R_accrual_date AS FactDate,'''
    
    #кейс для даты
    date_301 = '''(YEAR(FactDate_301)||'-'||(MONTH(FactDate_301))::VARCHAR(10)||'-1')::date AS FactDate,'''
    
    #кейс для даты
    date_302 = '''(YEAR(FactDate_302)||'-'||(MONTH(FactDate_302))::VARCHAR(10)||'-1')::date AS FactDate,'''
    
    #кейс для даты
    date_401 = '''(YEAR(FactDate_401)||'-'||(MONTH(FactDate_401))::VARCHAR(10)||'-1')::date AS FactDate,'''
    
    #кейс для даты
    date_402_403 = '''(YEAR(FactDate_402_403)||'-'||(MONTH(FactDate_402_403))::VARCHAR(10)||'-1')::date AS FactDate,'''
    
    #кейс для даты
    sold_r_case = '''CASE
             --
             WHEN ActionTypeComb_adj IN ('y301y302y401y403n402',
                                         'y301y302y402y401',
                                         'y301y401y402n403n302n700',
                                         'y301y401y402n403n302n700_loss',
                                         'y301y401y402n403n302y700',
                                         'y301y401y403n402n302n700',
                                         'y301y401y403n402n302n700_loss',
                                         'y301y401y403n402n302y700') 
             THEN (YEAR(FactDate_402_403)||'-'||(MONTH(FactDate_402_403))::VARCHAR(10)||'-1')::date
             --
             WHEN ActionTypeComb_adj IN ('y301y1101_loss',
                                         'y301y700') 
             THEN (YEAR(Losses_date)||'-'||(MONTH(Losses_date))::VARCHAR(10)||'-1')::date
             --
             WHEN ActionTypeComb_adj IN ('y301y302n402n401',
                                         'y301y302y401n402n403') 
             THEN (YEAR(FactDate_302)||'-'||(MONTH(FactDate_302))::VARCHAR(10)||'-1')::date
             --
           END AS FactDate,'''
    
    sold_r = '''Sold_R_accrual_date AS FactDate,'''
    
    #кейс для даты
    inter = '''International_Date AS FactDate,'''
    
    # Начало скрипта, задаём заголовки.
    query_start = '''DROP TABLE IF EXISTS table_1;
    CREATE LOCAL TEMPORARY TABLE table_1
    ON COMMIT PRESERVE ROWS AS
    
    SELECT *
    FROM {}
    LIMIT 0;
    
    SELECT ANALYZE_STATISTICS ('table_1');
    '''
    
    # Конец скрипта, склеиваем группы пивотов в одну таблицу
    query_end = '''
    DROP TABLE IF EXISTS result_table;
    CREATE LOCAL TEMPORARY TABLE result_table ON COMMIT PRESERVE ROWS AS
    
    {};
    
    SELECT ANALYZE_STATISTICS('result_table');
                   '''
    
    # шкурка для группы пивотов
    query_group_start = '''
    DROP TABLE IF EXISTS table_{};
    CREATE LOCAL TEMPORARY TABLE table_{} ON COMMIT PRESERVE ROWS AS
    
    SELECT *
    FROM (
    SELECT FactDate_301 AS FactDate,
    {}
           '' AS metric,
           0 AS value
    FROM table_1'''
    
    # закрытие группы пивотов
    query_group_end = ''') AS unpivot;
    
    SELECT ANALYZE_STATISTICS('table_{}');
    '''
    
    query= '''
    --==============--#
         UNION ALL  --#
    --==============--#
    SELECT {}
    {}
           '{}',
           {}({})
    FROM {}
    WHERE 1=1{}
    GROUP BY {}
    HAVING 1=1
       AND {}({}) <> 0
       AND {}({}) IS NOT NULL'''
    
    # Пишем скрипт для склеивания всех групп сводников в одну таблицу
    x = '''SELECT *
    FROM table_{}'''
    
    u = list(dict_measure['group'].unique())
    
    l = []
    
    for index in u:
        l.append(x.format(index))
    
    screp = '''
    --==============--#
         UNION ALL  --# 
    --==============--#
    '''.join(l)
    
    agg_columns = list(dict_measure['category_columns'].unique()) # <-- поля для агрегации
    agg_columns = [x for x in agg_columns if str(x) != 'nan']
    
    order = ','.join(str(x+1) for x in range(len(agg_columns)+2))
    
    table_name = '{}'.format(t_name) # <-- введите сюда наименование таблицы (с указанием схемы, если это не темп сгенерированный выше)
    
    # чистим переменную хранящую готовую простыню
    result = ''
    
    # вставляем первую часть простыни
    result = result + query_start.format(table_name)
    
    # записываем уникальные группы пивотов (большое количество групп положительно влияет на работоспособность скрипта)
    groups = list(dict_measure['group'].unique())
    
    # цикл создания простыни
    for g in groups:
    
         # для каждой группы формируем шкурку
        agg_col = agg_creater(agg_columns)
        result = result + query_group_start.format(g,g,agg_col)
    
        # определяем меры в группе
        list_measure_log_d = dict_measure.loc[dict_measure['group'] == g]['new_name']
    
        # цикл в котором создаются простыночки для кажной группы
        for index in list_measure_log_d:
    
            c_operator = dict_measure.loc[dict_measure['new_name'] == index]['operator'].iloc[0]
            c_measure = dict_measure.loc[dict_measure['new_name'] == index]['columns'].iloc[0]
            c_date = dict_measure.loc[dict_measure['new_name'] == index]['date'].iloc[0]
    
            total_filter = dict_measure.loc[dict_measure['new_name'] == index]['total_filter']
            account_filter = dict_measure.loc[dict_measure['new_name'] == index]['account_filter']
            
            c_filter = read_filters(total_filter, account_filter)
            
            exec(f'''result = result + query.format({c_date}, 
                                                     agg_col, 
                                                     index, 
                                                     c_operator, 
                                                     c_measure, 
                                                     table_name, 
                                                     c_filter, 
                                                     order,
                                                     c_operator, 
                                                     c_measure, 
                                                     c_operator, 
                                                     c_measure)
                  ''')
        # закрываем каждую группу    
        result = result + query_group_end.format(g)
    # склеиваем все простыночки в большую простыню
    result = result + query_end.format(screp)
    pc.copy(result)
    
    return