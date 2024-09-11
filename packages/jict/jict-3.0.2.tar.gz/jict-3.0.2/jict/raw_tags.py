from .tag_attrs import tag_attrs

def raw_tags(value):
    slen = len(value)
    starters  = [(i,c) for i,c in enumerate(value) if c in ['<','>']]
    nstarters = len(starters)
    entries   = []

    for i, s in enumerate(starters):
        _next = slen if (i+1) == nstarters else starters[i+1]
        pos = s[0]
        typ = s[1]

        if typ == '<':
            name  = value[s[0]+1:_next[0]].split(' ')[0]
            name  = name.replace('\n','').replace('\t','')
            sname = name.replace("/",'')

            cnt = 0
            ends = None
            for j in range(i,nstarters):
                if starters[j][1] == "<":
                    cnt += 1
                if starters[j][1] == ">" and cnt != 0:
                    cnt -= 1
                if starters[j][1] == ">" and cnt == 0:
                    ends = starters[j][0]
                    break

            if ends == None:
                continue

            entries.append({
                "name" : sname,
                "has_slash" : sname != name,
                "start" : s[0],
                "ends" : ends+1,
                "ender" : False if len(name) == 0 else (name[0] == "/"),
                "stupid" : len(name) == 0,
                "simple" : False if len(name) == 0 else (name[-1] == "/"),
                "single" : value[s[0]:ends+1].endswith("/>")
            })




    tags = []
    for i,e in enumerate(entries):
        name,start = e['name'], e['start']
        start_ends = e['ends']

        if e['stupid'] or e['simple'] or e['single']:
            tags.append({
                "name" : name ,
                "tabs" : value[0:start].split('\n')[-1],
                "start" : start,
                "start_ends" : start_ends,
                "close" : None ,
                "close_ends" : None ,
            })
            continue
        if e['ender']:
            continue

        cnt,ends = 0,None
        for j in range(i,len(entries)):
            if entries[j]['name'] != name or entries[j]['single']:
                continue
            if not entries[j]['ender']:
                cnt += 1
            if entries[j]['ender'] and cnt != 0:
                cnt -= 1
            if entries[j]['ender'] and cnt == 0:
                ends = entries[j]
                break

        tags.append({
            "name" : name ,
            "tabs" : value[0:start].split('\n')[-1],
            "start" : start,
            "start_ends" : start_ends,
            "close" : None if ends is None else ends['start'],
            "close_ends" : None if ends is None else ends['ends'],
        })


    for t in tags:
        # t['start_tag'] = value[t['start']:t['start_ends']]
        # t['close_tag'] = value[t['close']:t['close_ends']]

        t[  'attrs'  ] = tag_attrs(
            value[t['start']:t['start_ends']]
        )

        t['raw'] = value[
            t['start']:t['start_ends']
        ] if (t['close_ends'] is None) else value[
            t['start']:t['close_ends']
        ]

        t['contents'] = None if (t['close_ends'] is None) else value[
            t['start_ends']:t['close']
        ]

    for t in tags:
        t['slots'] = []
        if t['contents'] == None:
            continue

        # get all sub tags that are slots
        for st in tags:
            if st['close_ends'] == None:
                continue
            if not (st['start'] > t['start'] and st['close_ends'] < t['close_ends']):
                continue
            if st['name'] == 'slot':
                t['slots'].append(st)

    return tags
