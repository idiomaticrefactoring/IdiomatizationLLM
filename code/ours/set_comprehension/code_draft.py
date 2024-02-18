for num_months_ago in range(0, NUM_MONTHS_FOR_PARTITIONS):
    date_of_interest = datetime.datetime.now() - relativedelta(months=num_months_ago)
    year = date_of_interest.year
    month = '{:0>2}'.format(date_of_interest.month)
    query = ''
    for region in regions:
        if 'region={region}/year={year}/month={month}'.format(region=region, year=year, month=month) in partition_set:
            continue
        query += "PARTITION (region='{region}',year='{year}',month='{month}') location '{cloudtrail_log_path}/{region}/{year}/{month}/'\n".format(region=region, year=year, month=month, cloudtrail_log_path=cloudtrail_log_path)
    if query != '':
        queries_to_make.add('ALTER TABLE {table_name} ADD '.format(table_name=self.table_name) + query)


queries_to_make = {'ALTER TABLE {table_name} ADD '.format(table_name=self.table_name) + ''.join(["PARTITION (region='{region}',year='{year}',month='{month}') location '{cloudtrail_log_path}/{region}/{year}/{month}/'\n".format(region=region, year=date_of_interest.year, month='{0:0>2}'.format(date_of_interest.month), cloudtrail_log_path=cloudtrail_log_path)
      for region in regions if 'region={region}/year={year}/month={month}'.format(region=region, year=date_of_interest.year, month='{0:0>2}'.format(date_of_interest.month)) not in partition_set])
      for num_months_ago in range(0, NUM_MONTHS_FOR_PARTITIONS)
      for partition_set in [set(self.get_partitions())]
      for date_of_interest in [datetime.datetime.now() - relativedelta(months=num_months_ago)]}