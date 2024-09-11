
def tag_attrs(value):
    ref = value

    ref = ref.replace("/>","").replace('\n',' ').replace('>','')
    ref = " ".join([r for r in ref.split(' ') if r.strip() != '' and '<' not in r and '>' not in r])
    ref = ref.replace(" =","=").replace("= ","=")
    rei = [i for i, v in enumerate(ref) if v in ["'",'"']]

    dc = {"'":0,'"':0}
    lt = {"'":None,'"':None}
    pairs = []
    for c in rei:
        r = ref[c]
        n = dc[r]

        if n != 0: # close
            ref[c]
            dc[r] = 0
            o = "'" if r != "'" else '"'
            dc[o] = 0
            s,e = (lt[r],c)
            cnn = ref[s:e+1]
            pairs.append((s,e,cnn))
            lt[r] = None
        else:
            dc[r] += 1
            lt[r] = c

    dc = {str(i):v[2] for i,v in enumerate(pairs)}
    for k,v in dc.items():
        ref = ref.replace(v,f'{k}'.strip("'\"\n"))

    ref = ref.split(" ")
    data = {}
    for a in ref:
        g = a.split('=')
        data[g[0]] = True if len(g) < 2 else dc.get(g[1],None)
        i = data[g[0]]
        if isinstance(i,str):
            data[g[0]] = i[1:-1]

    return data
