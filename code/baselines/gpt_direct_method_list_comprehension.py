import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random, chat_gpt_ast_util
import openai, tiktoken, ast, util, util_rewrite,baseline_util
import ast
if __name__ == '__main__':
    user_instr = '''
Refactor the following Python code with list comprehension. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with list comprehension.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with list comprehension.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with list comprehension.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with list comprehension. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
def get_etf_historical_data(etf, country, from_date, to_date, stock_exchange=None, as_json=False, order='ascending', interval='Daily'):
    if not etf:
        raise ValueError('ERR#0031: etf parameter is mandatory and must be a valid etf name.')
    if not isinstance(etf, str):
        raise ValueError('ERR#0030: etf argument needs to be a str.')
    if country is None:
        raise ValueError('ERR#0039: country can not be None, it should be a str.')
    if country is not None and (not isinstance(country, str)):
        raise ValueError('ERR#0025: specified country value not valid.')
    if stock_exchange is not None and (not isinstance(stock_exchange, str)):
        raise ValueError('ERR#0125: specified stock_exchange value is not valid, it should be a str.')
    if not isinstance(as_json, bool):
        raise ValueError('ERR#0002: as_json argument can just be True or False, bool type.')
    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError('ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.')
    if not interval:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")
    if not isinstance(interval, str):
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")
    interval = interval.lower()
    if interval not in ['daily', 'weekly', 'monthly']:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")
    try:
        datetime.strptime(from_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")
    try:
        datetime.strptime(to_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")
    start_date = datetime.strptime(from_date, '%d/%m/%Y')
    end_date = datetime.strptime(to_date, '%d/%m/%Y')
    if start_date >= end_date:
        raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")
    date_interval = {'intervals': []}
    flag = True
    while flag is True:
        diff = end_date.year - start_date.year
        if diff > 19:
            obj = {'start': start_date.strftime('%m/%d/%Y'), 'end': start_date.replace(year=start_date.year + 19).strftime('%m/%d/%Y')}
            date_interval['intervals'].append(obj)
            start_date = start_date.replace(year=start_date.year + 19) + timedelta(days=1)
        else:
            obj = {'start': start_date.strftime('%m/%d/%Y'), 'end': end_date.strftime('%m/%d/%Y')}
            date_interval['intervals'].append(obj)
            flag = False
    interval_limit = len(date_interval['intervals'])
    interval_counter = 0
    data_flag = False
    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path), keep_default_na=False)
    else:
        raise FileNotFoundError('ERR#0058: etfs file not found or errored.')
    if etfs is None:
        raise IOError('ERR#0009: etfs object not found or unable to retrieve.')
    country = unidecode(country.strip().lower())
    if country not in get_etf_countries():
        raise RuntimeError('ERR#0034: country ' + country + ' not found, check if it is correct.')
    etf = unidecode(etf.strip().lower())
    def_exchange = etfs.loc[((etfs['name'].apply(unidecode).str.lower() == etf) & (etfs['def_stock_exchange'] == True)).idxmax()]
    etfs = etfs[etfs['country'].str.lower() == country]
    if etf not in list(etfs['name'].apply(unidecode).str.lower()):
        raise RuntimeError('ERR#0019: etf ' + etf + ' not found, check if it is correct.')
    etfs = etfs[etfs['name'].apply(unidecode).str.lower() == etf]
    if def_exchange['country'] != country:
        warnings.warn('Selected country does not contain the default stock exchange of the introduced ETF. ' + 'Default country is: "' + def_exchange['country'] + '" and default stock_exchange: "' + def_exchange['stock_exchange'] + '".', Warning)
        if stock_exchange:
            if stock_exchange.lower() not in etfs['stock_exchange'].str.lower():
                raise ValueError('ERR#0126: introduced stock_exchange value does not exists, leave this parameter to None to use default stock_exchange.')
            etf_exchange = etfs.loc[(etfs['stock_exchange'].str.lower() == stock_exchange.lower()).idxmax(), 'stock_exchange']
        else:
            found_etfs = etfs[etfs['name'].apply(unidecode).str.lower() == etf]
            if len(found_etfs) > 1:
                warnings.warn('Note that the displayed information can differ depending on the stock exchange. Available stock_exchange' + ' values for "' + country + '" are: "' + '", "'.join(found_etfs['stock_exchange']) + '".', Warning)
            del found_etfs
            etf_exchange = etfs.loc[(etfs['name'].apply(unidecode).str.lower() == etf).idxmax(), 'stock_exchange']
    elif stock_exchange:
        if stock_exchange.lower() not in etfs['stock_exchange'].str.lower():
            raise ValueError('ERR#0126: introduced stock_exchange value does not exists, leave this parameter to None to use default stock_exchange.')
        if def_exchange['stock_exchange'].lower() != stock_exchange.lower():
            warnings.warn('Selected stock_exchange is not the default one of the introduced ETF. ' + 'Default country is: "' + def_exchange['country'] + '" and default stock_exchange: "' + def_exchange['stock_exchange'].lower() + '".', Warning)
        etf_exchange = etfs.loc[(etfs['stock_exchange'].str.lower() == stock_exchange.lower()).idxmax(), 'stock_exchange']
    else:
        etf_exchange = def_exchange['stock_exchange']
    symbol = etfs.loc[((etfs['name'].apply(unidecode).str.lower() == etf) & (etfs['stock_exchange'].str.lower() == etf_exchange.lower())).idxmax(), 'symbol']
    id_ = etfs.loc[((etfs['name'].apply(unidecode).str.lower() == etf) & (etfs['stock_exchange'].str.lower() == etf_exchange.lower())).idxmax(), 'id']
    name = etfs.loc[((etfs['name'].apply(unidecode).str.lower() == etf) & (etfs['stock_exchange'].str.lower() == etf_exchange.lower())).idxmax(), 'name']
    etf_currency = etfs.loc[((etfs['name'].apply(unidecode).str.lower() == etf) & (etfs['stock_exchange'].str.lower() == etf_exchange.lower())).idxmax(), 'currency']
    final = list()
    header = symbol + ' Historical Data'
    for index in range(len(date_interval['intervals'])):
        interval_counter += 1
        params = {'curr_id': id_, 'smlID': str(randint(1000000, 99999999)), 'header': header, 'st_date': date_interval['intervals'][index]['start'], 'end_date': date_interval['intervals'][index]['end'], 'interval_sec': interval.capitalize(), 'sort_col': 'date', 'sort_ord': 'DESC', 'action': 'historical_data'}
        head = {'User-Agent': random_user_agent(), 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'text/html', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive'}
        url = 'https://www.investing.com/instruments/HistoricalDataAjax'
        req = requests.post(url, headers=head, data=params)
        if req.status_code != 200:
            raise ConnectionError('ERR#0015: error ' + str(req.status_code) + ', try again later.')
        if not req.text:
            continue
        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
        result = list()
        if path_:
            for elements_ in path_:
                if elements_.xpath('.//td')[0].text_content() == 'No results found':
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError('ERR#0010: etf information unavailable or not found.')
                else:
                    data_flag = True
                info = []
                for nested_ in elements_.xpath('.//td'):
                    info.append(nested_.get('data-real-value'))
                if data_flag is True:
                    etf_date = datetime.strptime(str(datetime.fromtimestamp(int(info[0]), tz=pytz.timezone('GMT')).date()), '%Y-%m-%d')
                    etf_close = float(info[1].replace(',', ''))
                    etf_open = float(info[2].replace(',', ''))
                    etf_high = float(info[3].replace(',', ''))
                    etf_low = float(info[4].replace(',', ''))
                    etf_volume = int(info[5])
                    result.insert(len(result), Data(etf_date, etf_open, etf_high, etf_low, etf_close, etf_volume, etf_currency, etf_exchange))
            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result
                if as_json is True:
                    json_list = [value.etf_as_json() for value in result]
                    final.append(json_list)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.etf_to_dict() for value in result])
                    df.set_index('Date', inplace=True)
                    final.append(df)
        else:
            raise RuntimeError('ERR#0004: data retrieval error while scraping.')
    if order in ['descending', 'desc']:
        final.reverse()
    if as_json is True:
        json_ = {'name': name, 'historical': [value for json_list in final for value in json_list]}
        return json.dumps(json_, sort_keys=False)
    elif as_json is False:
        return pd.concat(final)

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with list comprehension.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with list comprehension.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with list comprehension.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
info = []
for nested_ in elements_.xpath('.//td'):
    info.append(nested_.get('data-real-value'))
    
Refactored code:
info = [nested_.get('data-real-value') for nested_ in elements_.xpath('.//td')]
''']]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "list_comprehension"
    file_name = idiom + "_methods"

    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample
    '''
    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    
    file_name = "baseline_list_comprehension"
    util.save_pkl(save_complicated_code_dir_root + "baseline/",
                  file_name,
                  reponse_list)
    '''
    file_name = "baseline_list_comprehension"
    reponse_list = util.load_pkl(save_complicated_code_dir_root+ "baseline/", file_name)  # methods_sample
    print("reponse_list: ",len(reponse_list))
