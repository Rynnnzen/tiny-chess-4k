import os,json,urllib.request as u
NB=65000;MT=30000;IF=10**9
PV=[0,100,320,330,500,900,0]
PW=[0,0,1,1,2,4,0]
ND=[-33,-31,-18,-14,14,18,31,33];KD=[-17,-16,-15,-1,1,15,16,17];BD=[-17,-15,15,17];RD=[-16,-1,1,16]
KN,KG=[[[fr+d for d in D if not(fr+d&0x88)]for fr in range(128)]for D in(ND,KD)]
PS=[[0]*128 for _ in range(15)]
for sq in range(128):
 if sq&0x88:continue
 f=sq&7;r=sq>>4;c=min(f,7-f)+min(r,7-r)
 for o,rr in((0,r),(8,7-r)):
  PS[1+o][sq]=6*rr+3*c;PS[2+o][sq]=10*c;PS[3+o][sq]=5*c;PS[4+o][sq]=2*rr+12*(rr==6);PS[5+o][sq]=2*c;PS[6+o][sq]=(-10*c-6*rr,12*c)
B=[0]*128;S=0;C=0;E=-1;H=0;K=[0,0];MA=0;P=0;BC=[0,0];PH=24;PC=0;N=0;TT={};KL=[[0,0]for _ in range(64)];RP={};BR=0;GP=0;HH={}
class BE(Exception):pass
def F(fen):
 global B,S,C,E,H,K,MA,P,BC,PH,PC
 B=[0]*128;MA=0;P=0;BC=[0,0];PH=0;PC=0;K=[0,0]
 p=fen.split();r=p[0].split('/');sq=112
 for row in r:
  for ch in row:
   if ch.isdigit():sq+=int(ch)
   else:
    col=ch.islower();pt='PNBRQK'.index(ch.upper())+1;pc=pt+col*8
    B[sq]=pc;PC+=1
    if pt==6:K[col]=sq
    MA+=PV[pt]*(1-col*2)
    if pt==3:BC[col]+=1
    PH+=PW[pt]
    if pt!=6:v=PS[pc][sq];P+=v*(1-col*2)
    sq+=1
  sq-=24
 S=p[1]!='w';C=0
 for ch in p[2]:C|={'K':1,'Q':2,'k':4,'q':8}.get(ch,0)
 E=-1
 if p[3]!='-':E=(int(p[3][1])-1<<4)+ord(p[3][0])-97
 H=int(p[4])
def M(m):
 global S,C,E,H,K,MA,P,BC,PH,PC
 b=B;fr=m&127;to=(m>>7)&127;pr=(m>>14)&7;fl=m>>17;pc=b[fr];col=pc>>3;pt=pc&7;cap=b[to]
 undo=(pc,cap,C,E,H,K[col],MA,P,BC[0],BC[1],PH,PC)
 b[fr]=0;b[to]=pc if not pr else pr+col*8
 if cap:
  ccol=cap>>3;cpt=cap&7;MA-=PV[cpt]*(1-ccol*2);PC-=1
  if cpt!=6:v=PS[cap][to];P-=v*(1-ccol*2)
  if cpt==3:BC[ccol]-=1
  PH-=PW[cpt]
 if pt!=6:v=PS[pc][fr];P-=v*(1-col*2);v=PS[b[to]][to];P+=v*(1-col*2)
 else:K[col]=to
 if pt==6:C&=~3 if col==0 else~12
 if pt==4:C&={0:~2,7:~1,112:~8,119:~4}.get(fr,-1)
 if cap and(cap&7)==4:C&={0:~2,7:~1,112:~8,119:~4}.get(to,-1)
 if fl&1:
  csq=to-(16-32*col);cpc=b[csq];b[csq]=0;MA-=PV[1]*(1-(cpc>>3)*2);v=PS[cpc][csq];P-=v*(1-(cpc>>3)*2);PC-=1
 E=-1
 if pt==1 and abs(to-fr)==32:E=fr+(16-32*col)
 if fl&6:
  rfr=fr+3 if fl&2 else fr-4;rto=fr+1 if fl&2 else fr-1;rpc=b[rfr];b[rfr]=0;b[rto]=rpc;v=PS[rpc][rfr];P-=v*(1-col*2);v=PS[rpc][rto];P+=v*(1-col*2)
 if pr:
  MA+=(PV[pr]-PV[1])*(1-col*2)
  PH+=PW[pr]
  if pr==3:BC[col]+=1
 H=H+1 if pt!=1 and not cap else 0;S^=1;return undo
def U(undo,m):
 global S,C,E,H,K,MA,P,BC,PH,PC
 b=B;fr=m&127;to=(m>>7)&127;fl=m>>17;pc,cap,oc,oe,oh,oksq,om,op,obc0,obc1,oph,opc=undo;col=pc>>3
 b[fr]=pc;b[to]=cap
 if fl&1:
  csq=to-(16-32*col);b[csq]=1+(1-col)*8
 if fl&6:
  rfr=fr+3 if fl&2 else fr-4;rto=fr+1 if fl&2 else fr-1;rpc=b[rto];b[rfr]=rpc;b[rto]=0
 S^=1;C=oc;E=oe;H=oh;K[col]=oksq;MA=om;P=op;BC[0]=obc0;BC[1]=obc1;PH=oph;PC=opc
def A(sq,col):
 b=B;o=1-col;p=1+o*8;n=2+o*8;k=6+o*8;eb=(3+o*8,5+o*8);er=(4+o*8,5+o*8);st=16-32*o
 for d in(st-1,st+1):
  ts=sq-d
  if not(ts&0x88)and b[ts]==p:return 1
 for ts in KN[sq]:
  if b[ts]==n:return 1
 for ts in KG[sq]:
  if b[ts]==k:return 1
 for ds,ps in((BD,eb),(RD,er)):
  for d in ds:
   ts=sq+d
   while not(ts&0x88):
    pc=b[ts]
    if pc:
     if pc in ps:return 1
     break
    ts+=d
 return 0
def IC(col):return A(K[col],col)
def G():
 b=B;moves=[];col=S
 for fr in range(128):
  pc=b[fr]
  if not pc or(pc>>3)!=col:continue
  pt=pc&7
  if pt==1:
   dir=16-32*col;to=fr+dir
   if not(to&0x88)and not b[to]:
    if to>>4==7-7*col:
     for pr in(2,3,4,5):moves.append(fr|(to<<7)|(pr<<14))
    else:
     moves.append(fr|(to<<7))
     if fr>>4==1+5*col:
      to2=to+dir
      if not b[to2]:moves.append(fr|(to2<<7))
   for d in(dir-1,dir+1):
    to=fr+d
    if to&0x88:continue
    cap=b[to]
    if cap and(cap>>3)!=col:
     if to>>4==7-7*col:
      for pr in(2,3,4,5):moves.append(fr|(to<<7)|(pr<<14))
     else:moves.append(fr|(to<<7))
    elif to==E:moves.append(fr|(to<<7)|(1<<17))
  elif pt==2:
   for to in KN[fr]:
    cap=b[to]
    if not cap or(cap>>3)!=col:moves.append(fr|(to<<7))
  elif pt in(3,4,5):
   dirs=BD if pt==3 else RD if pt==4 else BD+RD
   for d in dirs:
    to=fr+d
    while not(to&0x88):
     cap=b[to]
     if cap:
      if(cap>>3)!=col:moves.append(fr|(to<<7))
      break
     moves.append(fr|(to<<7));to+=d
  else:
   for to in KG[fr]:
    cap=b[to]
    if not cap or(cap>>3)!=col:moves.append(fr|(to<<7))
   if fr==4+112*col:
    if C&(1+3*col)and not b[fr+1]and not b[fr+2]and not A(fr,col)and not A(fr+1,col)and not A(fr+2,col):moves.append(fr|((fr+2)<<7)|(2<<17))
    if C&(2+6*col)and not b[fr-1]and not b[fr-2]and not b[fr-3]and not A(fr,col)and not A(fr-1,col)and not A(fr-2,col):moves.append(fr|((fr-2)<<7)|(4<<17))
 return moves
def MU(m):
 fr=m&127;to=(m>>7)&127;pr=(m>>14)&7
 s=chr(97+(fr&7))+chr(49+(fr>>4))+chr(97+(to&7))+chr(49+(to>>4))
 if pr:s+='nbrq'[pr-2]
 return s
def UM(u):
 fr=(ord(u[1])-49)*16+(ord(u[0])-97);to=(ord(u[3])-49)*16+(ord(u[2])-97);pr=0;fl=0
 if len(u)==5:pr='nbrq'.index(u[4])+2
 pc=B[fr]
 if(pc&7)==6 and abs(to-fr)==2:fl=2 if to>fr else 4
 elif(pc&7)==1 and to==E and not B[to]:fl=1
 return fr|(to<<7)|(pr<<14)|(fl<<17)
def EV():
 mg=MA+P;wmg,weg=PS[6][K[0]];bmg,beg=PS[14][K[1]];kmg=wmg-bmg;keg=weg-beg;ph=min(PH,24)
 king=(kmg*ph+keg*(24-ph))//24;bp=25*((BC[0]>=2)-(BC[1]>=2))
 sc=mg+king+bp
 return sc if S==0 else-sc
def EE():
 return E if E>=0 and any(not((E-d)&0x88)and B[E-d]==1+S*8 for d in(15-32*S,17-32*S))else-1
def KY():return(bytes(B),S,C,EE())
def ID(rk):
 if RP.get(rk,0)>=3 or H>=100:return 1
 if PC>4:return 0
 n=0;bc=0;bs=0
 for i in range(128):
  pc=B[i]
  if pc:
   pt=pc&7
   if pt in(1,4,5):return 0
   if pt==2:n+=1
   elif pt==3:n+=1;bc+=1;bs|=1<<((i+(i>>4))&1)
 return 1 if n<=1 or(n==bc and bs in(1,2))else 0
def LG():
 l=[]
 for m in G():
  u=M(m)
  if not A(K[S^1],S^1):l.append(m)
  U(u,m)
 return l
def ADJ(ply):
 lg=LG()
 if not lg:return-MT+ply if IC(S)else 0
 d=0
 for pc in B:
  if pc:d+=[0,1,3,3,5,9,0][pc&7]*(1-(pc>>3)*2)
 if S==1:d=-d
 return 20000 if d>=5 else-20000 if d<=-5 else 0
def CS(m):
 to=(m>>7)&127;cap=B[to]
 if m&(1<<17):cap=1+(1-S)*8
 pr=(m>>14)&7
 return 16*(PV[cap&7]if cap else 0)-PV[B[m&127]&7]+(16*(PV[pr]-PV[1])if pr else 0)
def QX(m,a,b,p,r,q):
 u=M(m)
 if not A(K[S^1],S^1):
  try:return-Q(-b,-a,p+1,r+1,q+1)
  finally:U(u,m)
 U(u,m)
def Q(alpha,beta,ply,rp,qd):
 global N
 N+=1
 if N>NB:raise BE
 if qd>12:return EV()
 b=B;ps=G();one=0
 for m in ps:
  u=M(m)
  if not A(K[S^1],S^1):one=1;U(u,m);break
  U(u,m)
 if not one:return-MT+ply if IC(S)else 0
 if ID(KY()):return 0
 if GP+rp>=200:return ADJ(ply)
 if IC(S):
  for m in ps:
   sc=QX(m,alpha,beta,ply,rp,qd)
   if sc is not None and sc>alpha:
    alpha=sc
    if alpha>=beta:return beta
  return alpha
 sp=EV()
 if sp>=beta:return beta
 if sp>alpha:alpha=sp
 ms=[m for m in ps if b[(m>>7)&127]or m&(1<<17)or(m>>14)&7]
 if not qd:
  for m in ps:
   if m in ms:continue
   u=M(m);c=A(K[S],S);U(u,m)
   if c:ms.append(m)
 ms.sort(key=CS,reverse=True)
 for m in ms:
  cp=b[(m>>7)&127];pr=(m>>14)&7
  if sp+(PV[cp&7]if cp else 0)+(PV[pr]-PV[1]if pr else 0)+(100 if m&(1<<17)else 0)+200<=alpha:continue
  sc=QX(m,alpha,beta,ply,rp,qd)
  if sc is not None and sc>alpha:
   alpha=sc
   if alpha>=beta:return beta
 return alpha
def SE(alpha,beta,depth,ply,rp,null_ok):
 global N,BR,S,E,H
 N+=1
 if N>NB:raise BE
 rk=KY();key=rk+(H,)
 tte=TT.get(key)
 if ply and tte and tte[0]>=depth and RP.get(rk,0)<2:
  sc,bound=tte[1],tte[2]
  if sc>29000:sc+=ply
  elif sc<-29000:sc-=ply
  if bound==0:return sc
  if bound==1 and sc<=alpha:return alpha
  if bound==2 and sc>=beta:return beta
 if depth==0:return Q(alpha,beta,ply,rp,0)
 lg=LG()
 if not lg:return-MT+ply if IC(S)else 0
 if ID(rk):return 0
 if GP+rp>=200:return ADJ(ply)
 if null_ok and depth>=4 and not IC(S):
  rq=mn=0
  for pc in B:
   if pc and(pc>>3)==S:
    t=pc&7
    if t in(4,5):rq=1;break
    if t in(2,3):
     mn+=1
     if mn>1:break
  if(rq or mn>1)and H<80 and rk not in RP:
   os,oe=S,E;S^=1;E=-1
   try:sc=-SE(-beta,-beta+1,depth-2-(depth>=6),ply+1,rp,False)
   finally:S,E=os,oe
   if sc>=beta:return beta
 a0=alpha;tt_mv=tte[3]if tte else 0;rt_mv=BR if ply==0 else 0;k1,k2=KL[ply];ord=[]
 for x in(tt_mv,rt_mv):
  if x in lg and x not in ord:ord.append(x)
 caps=[m for m in lg if m not in ord and(B[(m>>7)&127]or(m>>14)&7 or m&(1<<17))]
 quiets=[m for m in lg if m not in ord and m not in caps]
 caps.sort(key=CS,reverse=True)
 ord.extend(caps)
 for x in(k1,k2):
  if x in lg and x not in ord:ord.append(x)
 quiets.sort(key=lambda m:HH.get(m,0),reverse=True)
 ord+=[m for m in quiets if m not in ord]
 bm=ord[0];bs=-IF
 for m in ord:
  u=M(m)
  try:sc=-SE(-beta,-alpha,depth-1,ply+1,rp+1,True)
  finally:U(u,m)
  if sc>bs:
   bs=sc;bm=m
   if sc>alpha:
    alpha=sc
    if alpha>=beta:
     if not(B[(m>>7)&127]or(m>>14)&7 or(m&(1<<17))):
      KL[ply][1],KL[ply][0]=KL[ply][0],m;HH[m]=HH.get(m,0)+depth**2
     break
 if GP+rp<188:
  if len(TT)>=32768 and key not in TT:TT.pop(next(iter(TT)))
  bound=1 if bs<=a0 else 2 if bs>=beta else 0
  sc=bs
  if sc>29000:sc-=ply
  elif sc<-29000:sc+=ply
  TT[key]=(depth,sc,bound,bm)
 if ply==0:BR=bm
 return alpha
def CH(legal_uci):
 global BR,N,KL
 N=0;HH.clear()
 for k in KL:k[0]=k[1]=0
 BR=0
 sl=set(legal_uci);fb=min(sl)if sl else''
 bim=UM(fb)if fb else 0
 try:
  for d in range(1,13):
   SE(-IF,IF,d,0,0,False)
   if BR and MU(BR)in sl:bim=BR
 except BE:pass
 return MU(bim)if bim else fb
def PO(url,data):
 req=u.Request(url,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
 with u.urlopen(req)as resp:return json.loads(resp.read().decode())
def main():
 global GP
 url=os.environ['MAKEFUN_ENV_URL']
 while True:
  g=PO(url+'/game',{})
  if g.get('status')=='done':break
  while g.get('status')=='your_move':
   F(g['start_fen']);RP.clear();RP[KY()]=1;GP=g['plies']
   for uci in g['moves']:
    M(UM(uci));k=KY();RP[k]=RP.get(k,0)+1
   legal=g['legal_moves']
   if not legal:break
   g=PO(url+'/move',{'game':g['game'],'move':CH(legal)})
if __name__=='__main__':main()
