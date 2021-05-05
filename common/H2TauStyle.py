from ROOT import TColor, kViolet, kBlue, kRed, kMagenta, kAzure

class Style:

    def __init__(self,
                 markerStyle=8,
                 markerColor=1,
                 markerSize=1,
                 lineStyle=1,
                 lineColor=1,
                 lineWidth=2,
                 fillColor=None,
                 fillStyle=1001):
        self.markerStyle = markerStyle
        self.markerColor = markerColor
        self.markerSize = markerSize
        self.lineStyle = lineStyle
        self.lineColor = lineColor
        self.lineWidth = lineWidth
        if fillColor is None:
            self.fillColor = lineColor
        else:
            self.fillColor = fillColor
        self.fillStyle = fillStyle

    def formatHisto(self, hist, title=None):
        hist.SetMarkerStyle(self.markerStyle)
        hist.SetMarkerColor(self.markerColor)
        hist.SetMarkerSize(self.markerSize)
        hist.SetLineStyle(self.lineStyle)
        hist.SetLineColor(self.lineColor)
        hist.SetLineWidth(self.lineWidth)
        hist.SetFillColor(self.fillColor)
        hist.SetFillStyle(self.fillStyle)
        if title != None:
            hist.SetTitle(title)
        return hist

# the following standard files are defined and ready to be used.
# more standard styles can be added on demand.
# user defined styles can be created in the same way in any python module

sBlack = Style()
sData = Style(fillStyle=0, markerSize=1.3)
sBlue = Style(markerColor=4, fillColor=4)
sGreen = Style(markerColor=8, fillColor=8)
sRed = Style(markerColor=2, fillColor=2)
sYellow = Style(lineColor=1, markerColor=5, fillColor=5)
sViolet = Style(lineColor=1, markerColor=kViolet, fillColor=kViolet)

qcdcol = TColor.GetColor(250,202,255)
sHTT_QCD = Style(lineColor=1, markerColor=qcdcol, fillColor=qcdcol)
dycol =  TColor.GetColor(248,206,104)
sHTT_DYJets = Style(lineColor=1, markerColor=dycol, fillColor=dycol)
wcol = TColor.GetColor(222,90,106)
sHTT_WJets = Style(lineColor=1, markerColor=wcol, fillColor=wcol)

ttcol = kAzure
TTJets_t = Style(lineColor=1, markerColor=ttcol+1, fillColor=ttcol+1)
TTJets_j = Style(lineColor=1, markerColor=ttcol+2, fillColor=ttcol+2)
TTJets_l = Style(lineColor=1, markerColor=ttcol+3, fillColor=ttcol+3)

ttcol_v2 = TColor.GetColor(135,206,250)
sHTT_TTJets_v2 = Style(lineColor=1, markerColor=ttcol_v2, fillColor=ttcol_v2)


ttcol2 = TColor.GetColor(155,152,204)
sHTT_TTJets = Style(lineColor=1, markerColor=ttcol, fillColor=ttcol2)







zlcol = TColor.GetColor(100,158,154)
sHTT_ZL = Style(lineColor=1, markerColor=zlcol, fillColor=zlcol)
dibosoncol = TColor.GetColor(222,140,106)
sHTT_VV = Style(lineColor=1, markerColor=dibosoncol, fillColor=dibosoncol)

jtfake = TColor.GetColor(100,222,106)
sHTT_jtfake = Style(lineColor=1, markerColor=jtfake, fillColor=jtfake)

lowmass = TColor.GetColor(240,175,60)
sHTT_lowmass = Style(lineColor=1, markerColor=lowmass, fillColor=lowmass)


sBlackSquares = Style(markerStyle=21)
sBlueSquares = Style(lineColor=4, markerStyle=21, markerColor=4)
sGreenSquares = Style(lineColor=8, markerStyle=21, markerColor=8)
sRedSquares = Style(lineColor=2, markerStyle=21, markerColor=2)


styleSet = [sBlue, sGreen, sRed, sYellow, sViolet, sBlackSquares, sBlueSquares, sGreenSquares, sRedSquares]
iStyle = 0

def nextStyle():
    global iStyle
    style = styleSet[iStyle]
    iStyle = iStyle+1
    if iStyle >= len(styleSet):
        iStyle = 0
    return style

histPref = {}
histPref['data_*'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['SingleMuon_*'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['SingleElectron_*'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['MuonEG_*'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['Tau_*'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['ZTT'] = {'style':sHTT_DYJets, 'layer':4, 'legend':'Z#rightarrow#tau#tau'}
histPref['ZTT1'] = {'style':sHTT_DYJets, 'layer':4, 'legend':'Z#rightarrow#tau#tau (M > 50)'}
histPref['ZTT2'] = {'style':sHTT_DYJets, 'layer':4, 'legend':'Z#rightarrow#tau#tau (M > 50)'}
histPref['ZTT3'] = {'style':sHTT_DYJets, 'layer':4, 'legend':'Z#rightarrow#tau#tau (M > 50)'}
histPref['ZTT4'] = {'style':sHTT_DYJets, 'layer':4, 'legend':'Z#rightarrow#tau#tau (M > 50)'}
histPref['ZTT10to50'] = {'style':sHTT_lowmass, 'layer':5, 'legend':'Z#rightarrow#tau#tau (10 < M < 50)'}
histPref['embed_*'] = {'style':sViolet, 'layer':4.1, 'legend':None}

histPref['TT'] = {'style':sHTT_TTJets_v2, 'layer':10, 'legend':'t#bar{t} with real #tau_{h}'}
histPref['TTLL'] = {'style':TTJets_t, 'layer':10, 'legend':'t#bar{t} with real #tau_{h}'}
histPref['TTLJ'] = {'style':TTJets_t, 'layer':10, 'legend':'t#bar{t} with real #tau_{h}'}
histPref['TTJJ'] = {'style':TTJets_t, 'layer':10, 'legend':'t#bar{t} with real #tau_{h}'}

histPref['TT_J'] = {'style':TTJets_j, 'layer':10, 'legend':'t#bar{t} with jets'} 
histPref['TTLL_J'] = {'style':TTJets_j, 'layer':10, 'legend':'t#bar{t} with jets'}
histPref['TTLJ_J'] = {'style':TTJets_j, 'layer':10, 'legend':'t#bar{t} with jets'}
histPref['TTJJ_J'] = {'style':TTJets_j, 'layer':10, 'legend':'t#bar{t} with jets'}


histPref['TT_L'] = {'style':TTJets_l, 'layer':10, 'legend':'t#bar{t} with leptons'} 
histPref['TTLL_L'] = {'style':TTJets_l, 'layer':10, 'legend':'t#bar{t} with leptons'}
histPref['TTLJ_L'] = {'style':TTJets_l, 'layer':10, 'legend':'t#bar{t} with leptons'}
histPref['TTJJ_L'] = {'style':TTJets_l, 'layer':10, 'legend':'t#bar{t} with leptons'}

histPref['TTT'] = {'style':TTJets_t, 'layer':10, 'legend':'t#bar{t} with real #tau_{h}'} 
histPref['TTJ'] = {'style':TTJets_j, 'layer':10, 'legend':'t#bar{t} with jets'} 
histPref['TTL'] = {'style':TTJets_l, 'layer':10, 'legend':'t#bar{t} with leptons'} 


histPref['T*tW*'] = {'style':sHTT_TTJets, 'layer':1, 'legend':'Single top'}
histPref['electroweak*'] = {'style':sHTT_WJets, 'layer':2, 'legend':'Electroweak'} 
histPref['TTo*'] = {'style':sHTT_TTJets, 'layer':1, 'legend':'Single top'} 
histPref['Single t'] = {'style':sHTT_TTJets, 'layer':1, 'legend':'Single top'} 
histPref['ST*'] = {'style':sHTT_TTJets, 'layer':1, 'legend':'Single top'} 
histPref['WW*'] = {'style':sHTT_VV, 'layer':0.9, 'legend':'Diboson'} 
histPref['WZ*'] = {'style':sHTT_VV, 'layer':0.8, 'legend':'Diboson'} 
histPref['ZZ*'] = {'style':sHTT_VV, 'layer':0.7, 'legend':'Diboson'} 
histPref['Diboson'] = {'style':sHTT_VV, 'layer':0.7, 'legend':'Diboson'} 
histPref['VV*'] = {'style':sHTT_VV, 'layer':0.7, 'legend':'Diboson'} 
histPref['QCD'] = {'style':sHTT_QCD, 'layer':0.1, 'legend':'QCD multijet'}
histPref['JTF'] = {'style':sHTT_QCD, 'layer':0.1, 'legend':'jet #rightarrow #tau fakes'}
histPref['W'] = {'style':sHTT_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['Electroweak'] = {'style':sHTT_DYJets, 'layer':3, 'legend':'Electroweak'}  
histPref['W1'] = {'style':sHTT_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['W2'] = {'style':sHTT_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['W3'] = {'style':sHTT_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['W4'] = {'style':sHTT_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['WJets'] = {'style':sHTT_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['ZJ*'] = {'style':sHTT_jtfake, 'layer':3.1, 'legend':'Z#rightarrow#tau#tau / Z#rightarrow ll, j#rightarrow#tau'}
histPref['ZL*'] = {'style':sHTT_ZL, 'layer':3.2, 'legend':'Z#rightarrow ll'}


#for idx, mass in enumerate([500,1000,1500,2000]):
#    _sstyle_ = Style(lineColor=idx+1, markerSize=0, markerColor=idx+1, lineWidth=3, lineStyle=2, fillColor=0)
#    _vstyle_ = Style(lineColor=idx+1, markerSize=0, markerColor=idx+1, lineWidth=3, lineStyle=1, fillColor=0)
#
#    histPref['SLQ_pair_M' + str(mass)] = {'style':_sstyle_, 'layer':1001, 'legend':'LQ_{S}LQ_{S}'}
#    histPref['VLQ_pair_M' + str(mass)] = {'style':_vstyle_, 'layer':1001, 'legend':'LQ_{V}LQ_{V}'}
#
#    _sstyle2_ = Style(lineColor=idx+1, markerSize=0, markerColor=idx+1, lineWidth=3, lineStyle=3, fillColor=0)
#    _vstyle2_ = Style(lineColor=idx+1, markerSize=0, markerColor=idx+1, lineWidth=3, lineStyle=4, fillColor=0)
#
#    histPref['SLQ_s-channel_M' + str(mass)] = {'style':_sstyle2_, 'layer':1001, 'legend':'LQ_{S}'}
#    histPref['VLQ_s_channel_M' + str(mass)] = {'style':_vstyle2_, 'layer':1001, 'legend':'LQ_{V}'}


#for idx, mass in enumerate([500,600, 700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900, 2000, 2500, 3000, 5000, 7000]):
for idx, mass in enumerate([600,800,1000,1200,1400,1600, 2000, 2200, 2500]):
#for idx, mass in enumerate([500,800,1000,1200,1500,2000, 2500, 3000, 5000, 7000]):

    _sstyle_ = Style(lineColor=idx+1, markerSize=0, markerColor=idx+1, lineWidth=3, lineStyle=2, fillColor=0)
    _vstyle_ = Style(lineColor=idx+1, markerSize=0, markerColor=idx+1, lineWidth=3, lineStyle=1, fillColor=0)

    _sstyle2_ = Style(lineColor=idx+1, markerSize=0, markerColor=idx+1, lineWidth=3, lineStyle=3, fillColor=0)
    _vstyle2_ = Style(lineColor=idx+1, markerSize=0, markerColor=idx+1, lineWidth=3, lineStyle=4, fillColor=0)

    _sstyle3_ = Style(lineColor=idx+1, markerSize=0, markerColor=idx+1, lineWidth=3, lineStyle=5, fillColor=0)
    _vstyle3_ = Style(lineColor=idx+2, markerSize=0, markerColor=idx+2, lineWidth=3, lineStyle=2, fillColor=0)

    histPref['SLQ_t-channel_M' + str(mass)] = {'style':_sstyle3_, 'layer':1001, 'legend':'NonResLQ_{S}'}
    histPref['VLQ_t-channel_M' + str(mass)] = {'style':_vstyle3_, 'layer':1001, 'legend':'NonResLQ_{V}'}

    histPref['SLQ-s-M' + str(mass)] = {'style':_sstyle_, 'layer':1001, 'legend':'LQ_{s}'}
    histPref['SLQ-p-M' + str(mass)] = {'style':_sstyle2_, 'layer':1001, 'legend':'LQ_{s}LQ_{s}'}
    histPref['SLQ-t-M' + str(mass)] = {'style':_sstyle3_, 'layer':1001, 'legend':'NonRes. LQ_{s}'}

    histPref['VLQ-s-M' + str(mass)] = {'style':_vstyle_, 'layer':1001, 'legend':'LQ_{s}'}
    histPref['VLQ-p-M' + str(mass)] = {'style':_vstyle2_, 'layer':1001, 'legend':'LQ_{s}LQ_{s}'}
    histPref['VLQ-t-M' + str(mass)] = {'style':_vstyle3_, 'layer':1001, 'legend':'NonRes. LQ_{s}'}


#for idx, mass in enumerate([1000, 1500, 2000, 2500, 3000, 3500, 4000]):
#    _sstyle3_ = Style(lineColor=idx+2, markerSize=0, markerColor=idx+2, lineWidth=3, lineStyle=2, fillColor=0)
#    histPref['Zprime_M' + str(mass)] = {'style':_sstyle3_, 'layer':1001, 'legend':'Zprime'}


