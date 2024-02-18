import numpy as np
a=np.array([1,2,3])
for ind,e in enumerate(a):
    print("ind,e: ",ind,e)


for ind,e in enumerate(1):
    print("ind,e: ",ind,e)

for i in items:
    j = re.split('-', i)
    if len(j) == 3:
        a = generateline(j[1], j[2], startdate, enddate, option)
        if a is None:
            continue
        time = [d[0] for d in a]
        if j[2] != 'Kline':
            if len(a[0]) == 4 and a[0][2] == 'bar':
                overlap = Overlap()
                form = [e[1] for e in a]
                bar = Bar(j[0] + '-' + j[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                bar.add(j[0] + '-' + j[2], time, form, yaxis_min='dataMin', yaxis_max='dataMax', is_datazoom_show=True, datazoom_type='slider')
                overlap.add(bar)
                line = Line(j[0] + 'price', width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                price = [e[3] for e in a]
                line.add(j[0] + 'price', time, price, yaxis_min='dataMin', yaxis_max='dataMax', is_datazoom_show=True, datazoom_type='slider', yaxis_type='value')
                overlap.add(line, yaxis_index=1, is_add_yaxis=True)
                page.add(overlap)
            if len(a[0]) == 5 and a[0][3] == 'pie':
                overlap = Overlap()
                timeline = Timeline(is_auto_play=False, timeline_bottom=0)
                namearray = [c[0] for c in a]
                valuearray = [d[1] for d in a]
                quarter = [e[2] for e in a]
                num = a[0][4]
                for x in range(0, num / 10):
                    list1 = valuearray[x]
                    names = namearray[x]
                    quarters = quarter[x][0]
                    for (idx, val) in enumerate(list1):
                        list1[idx] = float(val)
                    pie = Pie(j[0] + '-' + '前十股东'.decode('utf-8'), width=width1 * 10 / 11, height=height1 * 10 / 11)
                    pie.add(j[0] + '-' + '前十股东'.decode('utf-8'), names, list1, radius=[30, 55], is_legend_show=False, is_label_show=True, label_formatter='{b}: {c}\n{d}%')
                    timeline.add(pie, quarters)
                timeline.render()
                return
            else:
                form = [e[1] for e in a]
                line = Line(j[0] + '-' + j[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                line.add(j[0] + '-' + j[2], time, form, is_datazoom_show=True, datazoom_type='slider', yaxis_min='dataMin', yaxis_max='dataMax')
                page.add(line)
        else:
            overlap = Overlap()
            close = zip(*a)[2]
            candle = [[x[1], x[2], x[3], x[4]] for x in a]
            candlestick = Kline(j[0] + '-' + j[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
            candlestick.add(j[0], time, candle, is_datazoom_show=True, datazoom_type='slider', yaxis_interval=1)
            overlap.add(candlestick)
            if len(close) > 10:
                ma10 = calculateMa(close, 10)
                line1 = Line(title_color='#C0C0C0')
                line1.add(j[0] + '-' + 'MA10', time, ma10)
                overlap.add(line1)
            if len(close) > 20:
                ma20 = calculateMa(close, 20)
                line2 = Line(title_color='#C0C0C0')
                line2.add(j[0] + '-' + 'MA20', time, ma20)
                overlap.add(line2)
            if len(close) > 30:
                ma30 = calculateMa(close, 30)
                line3 = Line(title_color='#C0C0C0')
                line3.add(j[0] + '-' + 'MA30', time, ma30)
                overlap.add(line3)
            page.add(overlap)
    else:
        for k in range(1, len(j) / 3):
            j[3 * k - 1] = re.sub('\n&', '', j[3 * k - 1])
        sizearray = []
        layout = Overlap()
        for i in xrange(0, len(j), 3):
            array = j[i:i + 3]
            b = generateline(array[1], array[2], startdate, enddate, option)
            if b is None:
                continue
            btime = [d[0] for d in b]
            if array[2] != 'Kline':
                if len(b[0]) == 4 and b[0][2] == 'bar':
                    form = [e[1] for e in b]
                    bar = Bar(array[0] + '-' + array[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                    bar.add(array[0] + '-' + array[2], btime, form, is_datazoom_show=True, datazoom_type='slider', yaxis_min='dataMin', yaxis_max='dataMax')
                    layout.add(bar)
                    line = Line(array[0] + 'price', width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                    price = [e[3] for e in b]
                    line.add(array[0] + 'price', btime, price, is_datazoom_show=True, datazoom_type='slider', yaxis_min='dataMin', yaxis_type='value')
                    layout.add(line, yaxis_index=1, is_add_yaxis=True)
                else:
                    line = Line(array[0] + '-' + array[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                    line.add(array[0] + '-' + array[2], btime, b, is_datazoom_show=True, yaxis_max='dataMax', yaxis_min='dataMin', datazoom_type='slider')
                    layout.add(line)
            else:
                candle = [[x[1], x[2], x[3], x[4]] for x in b]
                candlestick = Kline(array[0] + '-' + array[1], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                candlestick.add(array[0], btime, candle, is_datazoom_show=True, datazoom_type=['slider'])
                close = zip(*b)[2]
                if len(close) > 10:
                    ma10 = calculateMa(close, 10)
                    line4 = Line(title_color='#C0C0C0')
                    line4.add(array[0] + '-' + 'MA10', btime, ma10)
                    layout.add(line4)
                if len(close) > 20:
                    ma20 = calculateMa(close, 20)
                    line5 = Line(title_color='#C0C0C0')
                    line5.add(array[0] + '-' + 'MA20', btime, ma20)
                    layout.add(line5)
                if len(close) > 30:
                    ma30 = calculateMa(close, 30)
                    line6 = Line(title_color='#C0C0C0')
                    line6.add(array[0] + '-' + 'MA30', btime, ma30)
                    layout.add(line6)
                layout.add(candlestick)
        page.add(layout)


for i, item in enumerate(items):
    j = re.split('-', item)
    if len(j) == 3:
        a = generateline(j[1], j[2], startdate, enddate, option)
        if a is None:
            continue
        time = [d[0] for d in a]
        if j[2] != 'Kline':
            if len(a[0]) == 4 and a[0][2] == 'bar':
                overlap = Overlap()
                form = [e[1] for e in a]
                bar = Bar(j[0] + '-' + j[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                bar.add(j[0] + '-' + j[2], time, form, yaxis_min='dataMin', yaxis_max='dataMax', is_datazoom_show=True, datazoom_type='slider')
                overlap.add(bar)
                line = Line(j[0] + 'price', width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                price = [e[3] for e in a]
                line.add(j[0] + 'price', time, price, yaxis_min='dataMin', yaxis_max='dataMax', is_datazoom_show=True, datazoom_type='slider', yaxis_type='value')
                overlap.add(line, yaxis_index=1, is_add_yaxis=True)
                page.add(overlap)
            if len(a[0]) == 5 and a[0][3] == 'pie':
                overlap = Overlap()
                timeline = Timeline(is_auto_play=False, timeline_bottom=0)
                namearray = [c[0] for c in a]
                valuearray = [d[1] for d in a]
                quarter = [e[2] for e in a]
                num = a[0][4]
                for x in range(0, num / 10):
                    list1 = valuearray[x]
                    names = namearray[x]
                    quarters = quarter[x][0]
                    for (idx, val) in enumerate(list1):
                        list1[idx] = float(val)
                    pie = Pie(j[0] + '-' + '前十股东'.decode('utf-8'), width=width1 * 10 / 11, height=height1 * 10 / 11)
                    pie.add(j[0] + '-' + '前十股东'.decode('utf-8'), names, list1, radius=[30, 55], is_legend_show=False, is_label_show=True, label_formatter='{b}: {c}\n{d}%')
                    timeline.add(pie, quarters)
                timeline.render()
                return
            else:
                form = [e[1] for e in a]
                line = Line(j[0] + '-' + j[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                line.add(j[0] + '-' + j[2], time, form, is_datazoom_show=True, datazoom_type='slider', yaxis_min='dataMin', yaxis_max='dataMax')
                page.add(line)
        else:
            overlap = Overlap()
            close = zip(*a)[2]
            candle = [[x[1], x[2], x[3], x[4]] for x in a]
            candlestick = Kline(j[0] + '-' + j[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
            candlestick.add(j[0], time, candle, is_datazoom_show=True, datazoom_type='slider', yaxis_interval=1)
            overlap.add(candlestick)
            if len(close) > 10:
                ma10 = calculateMa(close, 10)
                line1 = Line(title_color='#C0C0C0')
                line1.add(j[0] + '-' + 'MA10', time, ma10)
                overlap.add(line1)
            if len(close) > 20:
                ma20 = calculateMa(close, 20)
                line2 = Line(title_color='#C0C0C0')
                line2.add(j[0] + '-' + 'MA20', time, ma20)
                overlap.add(line2)
            if len(close) > 30:
                ma30 = calculateMa(close, 30)
                line3 = Line(title_color='#C0C0C0')
                line3.add(j[0] + '-' + 'MA30', time, ma30)
                overlap.add(line3)
            page.add(overlap)
    else:
        for k in range(1, len(j) / 3):
            j[3 * k - 1] = re.sub('\n&', '', j[3 * k - 1])
        sizearray = []
        layout = Overlap()
        for idx in xrange(0, len(j), 3):
            array = j[idx:idx + 3]
            b = generateline(array[1], array[2], startdate, enddate, option)
            if b is None:
                continue
            btime = [d[0] for d in b]
            if array[2] != 'Kline':
                if len(b[0]) == 4 and b[0][2] == 'bar':
                    form = [e[1] for e in b]
                    bar = Bar(array[0] + '-' + array[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                    bar.add(array[0] + '-' + array[2], btime, form, is_datazoom_show=True, datazoom_type='slider', yaxis_min='dataMin', yaxis_max='dataMax')
                    layout.add(bar)
                    line = Line(array[0] + 'price', width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                    price = [e[3] for e in b]
                    line.add(array[0] + 'price', btime, price, is_datazoom_show=True, datazoom_type='slider', yaxis_min='dataMin', yaxis_type='value')
                    layout.add(line, yaxis_index=1, is_add_yaxis=True)
                else:
                    line = Line(array[0] + '-' + array[2], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                    line.add(array[0] + '-' + array[2], btime, b, is_datazoom_show=True, yaxis_max='dataMax', yaxis_min='dataMin', datazoom_type='slider')
                    layout.add(line)
            else:
                candle = [[x[1], x[2], x[3], x[4]] for x in b]
                candlestick = Kline(array[0] + '-' + array[1], width=width1 * 10 / 11, height=height1 * 10 / 11 / len(items))
                candlestick.add(array[0], btime, candle, is_datazoom_show=True, datazoom_type=['slider'])
                close = zip(*b)[2]
                if len(close) > 10:
                    ma10 = calculateMa(close, 10)
                    line4 = Line(title_color='#C0C0C0')
                    line4.add(array[0] + '-' + 'MA10', btime, ma10)
                    layout.add(line4)
                if len(close) > 20:
                    ma20 = calculateMa(close, 20)
                    line5 = Line(title_color='#C0C0C0')
                    line5.add(array[0] + '-' + 'MA20', btime, ma20)
                    layout.add(line5)
                if len(close) > 30:
                    ma30 = calculateMa(close, 30)
                    line6 = Line(title_color='#C0C0C0')
                    line6.add(array[0] + '-' + 'MA30', btime, ma30)
                    layout.add(line6)
                layout.add(candlestick)
        page.add(layout)
