# copied from ember_repeatavail/log_trans, log_ecc
ber1 = {\
'25/ours' : [0.007440597766884533, 0.0017482047878879376],
'25/SBA' : [0.007515488834422658, 0.0016599955757213953],
'50/ours' : [0.005261097494553377, 0.0006359206718799173],
'50/SBA' : [0.007597188180827887, 0.0010051658420795928],
'75/ours' : [0.0042619825708060995, 0.0004820164072767624],
'75/SBA' : [0.006827001633986927, 0.0005125293403494151],
'90/ours' : [0.004202410130718954, 0.0002897220654831672],
'90/SBA' : [0.00678359885620915, 0.0005202385208044458],
'100/ours' : [0.0037956154684095854, 4.336808689942018e-19],
'100/SBA' : [0.007421023965141613, 0],
}

ecc1={\
'25/ours': 1.123456790123457,
'25/SBA': 1.123456790123457,
'50/ours': 1.103448275862069,
'50/SBA': 1.123456790123457,
'75/ours': 1.0963855421686748,
'75/SBA': 1.117936117936118,
'90/ours': 1.095,
'90/SBA': 1.117936117936118,
'100/ours': 1.091127098321343,
'100/SBA': 1.123456790123457,
}

ber2 = {\
'25/ours' : [0.005729166666666666, 0.0016811452105783026],
'25/SBA' : [0.007781862745098041, 0.0018982740287573124],
'50/ours' : [0.005024509803921569, 0.0012212703080879137],
'50/SBA' : [0.0070006127450980395, 0.0015532363076239308],
'75/ours' : [0.004610906862745098, 0.000972340751994997],
'75/SBA' : [0.006786151960784313, 0.0008193675931566383],
'90/ours' : [0.0037990196078431376, 0.0005557094714220913],
'90/SBA' : [0.006709558823529411, 0.0010133477578763012],
'100/ours' : [0.0036764705882352936, 0.0],
'100/SBA' : [0.0070465686274509805, 0.0],
}


ecc2={\
'25/ours': 1.1070559610705597,
'25/SBA': 1.123456790123457,
'50/ours': 1.1016949152542372,
'50/SBA': 1.117936117936118,
'75/ours': 1.0966183574879227,
'75/SBA': 1.117936117936118,
'90/ours': 1.091127098321343,
'90/SBA': 1.1176470588235294,
'100/ours': 1.0902255639097744,
'100/SBA': 1.117936117936118,
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
            return ber1[str(n)+"/SBA"][0]
        else:
            return ber1[str(n)+"/ours"][0]
    else:
        assert idx == 2
        if sba == True:
            return ber2[str(n)+"/SBA"][0]
        else:
            return ber2[str(n)+"/ours"][0]

def berp(idx,n,sba):
    return to_percent(ber(idx,n,sba))

def delta_ber(idx,n):
    if idx == 1:
        return ber1[str(n)+"/ours"][0] - ber1[str(n)+"/SBA"][0]
    else:
        assert idx == 2
        return ber2[str(n)+"/ours"][0] - ber2[str(n)+"/SBA"][0]

def delta_berp(idx,n):
    return to_percent(delta_ber(idx,n))

def ecc(idx,n,sba):
    if idx == 1:
        if sba == True:
            return ecc1[str(n)+"/SBA"]-1
        else:
            return ecc1[str(n)+"/ours"]-1
    else:
        assert idx == 2
        if sba == True:
            return ecc2[str(n)+"/SBA"]-1
        else:
            return ecc2[str(n)+"/ours"]-1

def eccp(idx,n,sba):
    return to_percent(ecc(idx,n,sba))

def delta_ecc(idx,n):
    if idx == 1:
        return ecc1[str(n)+"/ours"] - ecc1[str(n)+"/SBA"]
    else:
        assert idx == 2
        return ecc2[str(n)+"/ours"] - ecc2[str(n)+"/SBA"]

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
