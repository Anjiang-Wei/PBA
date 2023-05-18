# copied from ember_avail/log_trans, log_ecc
ber1 = {\
'25/ours8' : 0.005821078431372549,
'25/SBA8' : 0.006093409586056644,
'50/ours8' : 0.004901960784313725,
'50/SBA8' : 0.006246595860566449,
'75/ours8' : 0.004723243464052287,
'75/SBA8' : 0.007412513616557734,
'90/ours8' : 0.0036509395424836597,
'90/SBA8' : 0.007727396514161221,
'100/ours8' : 0.003795615468409586,
'100/SBA8' : 0.007421023965141612,
}

ecc1={\
'25/ours8': 1.1075794621026895,
'25/SBA8': 1.1124694376528117,
'50/ours8': 1.1016949152542372,
'50/SBA8': 1.1124694376528117,
'75/ours8': 1.099255583126551,
'75/SBA8': 1.1233933161953729,
'90/ours8': 1.0895522388059702,
'90/SBA8': 1.123456790123457,
'100/ours8': 1.091127098321343,
'100/SBA8': 1.123456790123457,
}

ber2 = {\
'25/ours8' : 0.0065870098039215695,
'25/SBA8' : 0.010263480392156863,
'50/ours8' : 0.005208333333333333,
'50/SBA8' : 0.0059742647058823525,
'75/ours8' : 0.003829656862745098,
'75/SBA8' : 0.00628063725490196,
'90/ours8' : 0.003982843137254902,
'90/SBA8' : 0.005667892156862745,
'100/ours8' : 0.0036764705882352936,
'100/SBA8' : 0.0070465686274509805,
}

ecc2={\
'25/ours8': 1.1152882205513786,
'25/SBA8': 1.1439588688946016,
'50/ours8': 1.102189781021898,
'50/SBA8': 1.1105527638190955,
'75/ours8': 1.091127098321343,
'75/SBA8': 1.1124694376528117,
'90/ours8': 1.091127098321343,
'90/SBA8': 1.1070559610705597,
'100/ours8': 1.0902255639097744,
'100/SBA8': 1.117936117936118,
}

def to_percent(x):
    if x == 1:
        return "100%"
    if x == -1:
        return "-100%"
    if x == 'N/A':
        return "N/A"
    if x == 0:
        return "0%"
    return ("%.2g" % (x * 100)) + "%"

def ber(idx,n,sba):
    if idx == 1:
        if sba == True:
            return ber1[str(n)+"/SBA8"]
        else:
            return ber1[str(n)+"/ours8"]
    else:
        assert idx == 2
        if sba == True:
            return ber2[str(n)+"/SBA8"]
        else:
            return ber2[str(n)+"/ours8"]

def berp(idx,n,sba):
    return to_percent(ber(idx,n,sba))

def delta_ber(idx,n):
    if idx == 1:
        return ber1[str(n)+"/ours8"] - ber1[str(n)+"/SBA8"]
    else:
        assert idx == 2
        return ber2[str(n)+"/ours8"] - ber2[str(n)+"/SBA8"]

def delta_berp(idx,n):
    return to_percent(delta_ber(idx,n))

def ecc(idx,n,sba):
    if idx == 1:
        if sba == True:
            return ecc1[str(n)+"/SBA8"]-1
        else:
            return ecc1[str(n)+"/ours8"]-1
    else:
        assert idx == 2
        if sba == True:
            return ecc2[str(n)+"/SBA8"]-1
        else:
            return ecc2[str(n)+"/ours8"]-1

def eccp(idx,n,sba):
    return to_percent(ecc(idx,n,sba))

def delta_ecc(idx,n):
    if idx == 1:
        return ecc1[str(n)+"/ours8"] - ecc1[str(n)+"/SBA8"]
    else:
        assert idx == 2
        return ecc2[str(n)+"/ours8"] - ecc2[str(n)+"/SBA8"]

def delta_eccp(idx,n):
    return to_percent(delta_ecc(idx,n))

def compute_fstr(n):
    # dataset	SBA	DALA	delta_BER	SBA	DALA	delta_ECC	SBA	DALA	delta_BER	SBA	DALA	delta_ECC
    str1 = f'{n}%,{berp(1,n,True)},{berp(1,n,False)},{delta_berp(1,n)},{eccp(1,n,True)},{eccp(1,n,False)},{delta_eccp(1,n)}' +\
               f',{berp(2,n,True)},{berp(2,n,False)},{delta_berp(2,n)},{eccp(2,n,True)},{eccp(2,n,False)},{delta_eccp(2,n)}'
    return str1

if __name__ == "__main__":
    for i in [25, 50, 75, 90, 100]:
        print(compute_fstr(i))
