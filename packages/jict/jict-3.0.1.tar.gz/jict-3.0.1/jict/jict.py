#!/usr/bin/env python
import sys, json, yaml, os
from collections import defaultdict , deque
from datetime import timedelta as td, datetime as dt
from .helpers import loader, jsonencoder
from time import time

def to_jict(prev):
    nd = jict()
    for k,i in prev.items():
        if isinstance(i,dict):
            nd[k] = to_jict(i)
        else:
            nd[k] = i
    return nd

class jict( defaultdict ):
    generator = None
    storepath = None

    def __new__(self, nd = None, extra = None):
        if isinstance( nd, dict ):
            dt = to_jict(nd)
            return dt

        # elif isinstance( nd, list ):
        #     jct = jict()
        #     for i,e in enumerate( nd ):
        #         if isinstance( e, dict ):
        #             e = to_jict(e)
        #         jct[i] = e
        #
        #     jct.generator = list
        #     return jct

        elif str(nd) == "<class 'pymongo.collection.Collection'>":
            jct = jict()
            k = nd.find({'key':extra})
            if k.count() >= 1:
                jct = jict(json.loads(next(k)['data']))

            jct.generator = nd
            jct.storepath = extra
            return jct
        elif isinstance( nd, str ):
            append = [ '.yaml' , '.json', '.list', '.env', '.env.example']
            # prepend= [ 'shm//:', 'set://' ]
            dt,transf,prepsf,file,size = None,'','',False,len(nd)

            for x in append:
                xs = len(x)
                if xs >= size: continue
                if nd[-xs:]==x:
                    file,transf=True,x
                    break

            # for x in prepend:
            #     xs = len(x)
            #     if xs => size: continue
            #     if nd[:xs]==x:
            #         prepsf,nd=x,nd[xs:]
            #         break

            if file:
                if not os.path.isfile( nd ):
                    dr = os.path.dirname(nd)
                    if not os.path.exists( dr ):
                        os.makedirs(dr)

                    f = open( nd , 'w+' );
                    f.write("{}"); f.close()

                    transf = ''

            if transf in [ '.yaml',  '.yml' , '.json' ]:
                da = loader( nd , transf )
                dt = None
                if isinstance(da,dict):
                    dt = to_jict(da)
                elif isinstance( da, list ):
                    dt = jict()
                    for i,e in enumerate( da ):
                        if isinstance( e, dict ):
                            e = to_jict(e)
                        dt[i] = e
                    dt.generator = list
                else:
                    dt = jict()
                dt.storepath = nd
            elif transf in ['.env','.env.example','.list']:
                lst = [x for x in open(nd,"r+").read().split('\n') if x !='']
                if transf == '.list':
                    dt = lst
                else:
                    for y in lst:
                        if '=' in y:
                            x = y.split('=')
                            jct[x[0]] = x[1]

                    jct.storepath = nd
                    dt = jct
            else:
                dt = jict()

            return dt

        return super(jict, self).__new__(self, nd )

    def __init__(self, nd = None , extra = ''):
        self.factory = jict
        defaultdict.__init__( self, self.factory )

        # if self.generator == list:
        #     @property
        #     def avg(self):
        #         return self.sum / self.len
        #     @property
        #     def max(self):
        #         suma = 0
        #         for x in self: suma += self[x]
        #         return max(self)
        #     @property
        #     def min(self):
        #         return min(self)
        #     @property
        #     def sum(self):
        #         suma = 0
        #         for x in self: suma += self[x]
        #         return suma
        #     @property
        #     def len(self):
        #         return len(self.keys())
        #
        #     self.avg = avg
        #     self.max = max
        #     self.min = min
        #     self.sum = sum
        #     self.len = len

    # creates a default valuef for the key if doesn't has one
    def init(self,key, deft ):
        if key in self.keys():
            return self[key]
        self[key] = deft
        return self[key]

    def take(self, key , deft , format = '__deft__' ):
        if key in self:
            try:
                if format == '__deft__':
                    return self[key]
                elif type(self[key]) == format:
                    return self[key]
                elif format == int:
                    return int(self[key])
                elif format == str:
                    return str(self[key])
                elif format == float:
                    return float(self[key])
                elif format == list:
                    return []
            except:
                pass

        self[key] = deft
        return self[key]

    def strptime(self,key,pattern):
        if key not in self:
            return None
        return dt.strptime( self[key] ,pattern )

    def strptimestamp(self,key,pattern):
        if key not in self:
            return None
        return dt.timestamp( dt.strptime( self[key] ,pattern ) )

    def __iadd__(self, other):
        typ = type(other)

        if typ == int:
            return 0 + other

        if typ == dict:
            other = jict(other)
            typ = jict

        if typ == jict:
            for x in other.keys():
                if x not in self.keys():
                    self[x] = other[x]
                else:
                    self[x] += other[x]

        return self

    def set_max(self,key,val,create = False):
        if key not in self.keys():
            if not create: return self[key]
            else:
                self[key] = val
                return self[key]

        if self[key] == None:
            self[key] = 0

        self[key] = val if val > self[key] else self[key]
        return self[key]

    def set_min(self,key,val,create = False ):
        if key not in self.keys():
            if not create: return self[key]
            else:
                self[key] = val
                return self[key]

        if self[key] == None:
            self[key] = 10 ** 15

        self[key] = val if val < self[key] else self[key]
        return self[key]

    def dropk(self,*args,as_type='',deep=False):
        for x in args:
            if x in self:
                del self[x]
            elif isinstance(self[x],jict) and deep:
                self[x].dropk(*args,as_type='',deep=deep)

        if as_type == 'dict':
            return self.dict()

    def drop(self ,target = None, as_type='', deep = False ):

        def ittrlis(val,tar):
            for l in val:
                if isinstance(l,jict):
                    l.drop(tar)
                if isinstance(l,list):
                    ittrlis(l,tar)

        for x in list(self):
            val = self[x]
            if isinstance(val , jict):
                val.drop( target )

                if deep:
                    skp = False
                    for y in val:
                        if val[y] != target:
                            skp = True; break
                    if not skp:
                        del self[x]
                        continue

            if isinstance(val , list ):
                ittrlis(val, target)

            if val == target:
                del self[x]

        if as_type == 'dict':
            return self.dict()

        return self

    def rename(self,target,replace):
        def ittrlist(lst,tg,rp):
            nl = []
            for x in lst:
                if isinstance(x,jict):
                    x.rename(tg,rp)
                if isinstance(x,dict):
                    jct = jict(x)
                    jct.rename(tg,rp)
                    x = jct.dict()
                if isinstance(x,list):
                    x = ittrlist(x,tg,rp)

                nl.append(x)
            return nl

        for k in self.keys():
            val = self[k]
            if isinstance(val,list):
                self[k] = ittrlist(val,target,replace)
            if isinstance(val,jict):
                val.rename(target,replace)
            if isinstance(val,dict):
                jct = jict(val)
                jct.rename(target,replace)
                self[k] = jct.dict()
            if k == target:
                self[replace] = self.pop(target)

    def replace(self, target , replacef = None ):
        if replacef == None and isinstance(target,dict):
            for k in target.keys():
                self.replace(k,target[k])
            return

        def ittrlist(lst,tg,rp):
            nl = []
            for x in lst:
                if isinstance(x,jict):
                    x.replace(tg,rp)
                if isinstance(x,dict):
                    jct = jict(x)
                    jct.replace(tg,rp)
                    x = jct.dict()
                if isinstance(x,list):
                    x = ittrlist(x,tg,rp)
                nl.append(x)
            return nl

        for k in self.keys():
            val = self[k]
            if isinstance(val,list):
                self[k] = ittrlist(val,target,replacef)
            if isinstance(val,jict):
                val.replace(target,replacef)
            if isinstance(val,dict):
                jct = jict(val)
                jct.replace(target,replacef)
                self[k] = jct.dict()

            if k == target:
                if hasattr(replacef, '__call__'):
                    self[k] = replacef(val)
                else:
                    self[k] = replacef

    def _ittrlist(self,lst,k,v,luky=True ):
        found = []
        for x in lst:
            if isinstance(x,list):
                found += self._ittrlist(x,k,v,luky)
                continue
            elif isinstance(x,dict) or isinstance(x,jict):
                found += self._ittrdict(x,k,v,luky)
        return found

    def _ittrdict(self,dic,k,v,luky = True ):
        found = []
        for x in dic.keys():
            val = dic[x]

            if x == k:
                found.append(val)
                if luky: return found
                continue

            if isinstance(val, list):
                found += self._ittrlist(val,k,v,luky)
                continue

            elif isinstance(val,dict) or isinstance(val,jict):
                found += self._ittrdict(val,k,v,luky)

        return found

    def get(self,key,val=None,luky = True ):
        ret = self._ittrdict(self, key, val , luky )

        if len(ret) == 1:
            return ret[-1]
        elif len(ret) > 1:
            return ret

        return None

    def dict(self, input_dict=None ):
        plain_dict = dict()
        if input_dict is None:
            input_dict = self
        for key in input_dict.keys():
            value = input_dict[key]
            if isinstance(value, jict):
                plain_dict[ key ] = self.dict(value)
            else:
                plain_dict[ key ] = value
        return plain_dict

    def __str__(self):
        return self.json()

    def json(self,indent=2):
        if indent == 0: return json.dumps( self.dict() , cls= jsonencoder )
        return json.dumps( self.dict() , indent = indent , cls= jsonencoder )

    def yaml(self):
        return yaml.dump(yaml.full_load( self.json(0) ), default_flow_style=False)

    def deque(self,key,data,maxlen = 5 ):
        if not isinstance(self[key], deque ):
            if isinstance(self[key], list ):
                self[key] = deque(self[key], maxlen = maxlen)
            else:
                self[key] = deque(maxlen = maxlen)

        self[key].append( data )

    def save(self, name = None ):
        # generators
        if str(self.generator) == "<class 'pymongo.collection.Collection'>":
            if '_id' not in self.keys():
                k = self.generator.find({'key':self.storepath})
                if k.count() >= 1:
                    self['_id'] = next(k)['_id']

            if '_id' not in self.keys():
                self.generator.insert_one({ 'data':self.json(), 'key': self.storepath })
            else:
                self.generator.update_one(
                    { '_id':self['_id'] },{ '$set':{'data':self.json()} }
                )
            return self

        if name != None:
            self.storepath = name

        if self.storepath == None:
            return self

        if not os.path.isfile( self.storepath ):
            dr = os.path.dirname(self.storepath)
            if not os.path.exists(dr):
                os.makedirs(dr)

        transf = ''
        size = len( self.storepath )
        for x in ['.list','.env','.env.example','.yaml','.json']:
            xs = len( x )
            if xs >= size: continue
            if self.storepath[-xs:]==x:
                transf=x
                break

        f = open(self.storepath, "w+")
        if transf in ['.example','.env']:
            f.write( '\n'.join([f'{x}='+str(self[x]) for x in self.keys()]) )
        elif transf == '.list':
            f.write( '\n'.join([str(self[x]) for x in self.keys()]) )
        elif transf == '.yaml':
            f.write( self.yaml() )
        else:
            f.write( self.json() )

        f.close()
