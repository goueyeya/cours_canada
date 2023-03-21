
str = "vBBEO.CpefN.TBsgS.HfjLG.wcZee.qZrhY.TDFdp.mBbei.IbHlG.tmXTZ.XqBtD.LYzBt.upRSj.EOzlj.izClL.oRdKf.CpefN.XceXS.mBbei.XqBtD.qPcfO.IbHlG.qZrhY.TDFdp.DMmXT.adNyQ.JkxgL.hhGEG.hhGEG.kcXxq.tmXTZ.yWzOK.EtLOl.adNyQ.NliRt.hMtRY.jNjpP.rAufC.EOzlj.yRfgC.xuGlS.FGtbV.twlpW.OIbPg.AKTma.IpMPe.FGtbV.AsxCD.twlpW.FGtbV.oLrPj.BCzeb.oLrPj.BdnLz.Fktri.BYuJB.ScYNb.ZMame.hjkWz.bsTEm.xNRlR.ScYNb.ChkfV.RBFxa.IpMPe.oLrPj.UaiOC.WXzRX.BMDfi.DUHjr.UaiOC.fZXDJ.NCbJd.WXzRX.zvOaa.PTRdF.TCbsY.oLrPj.DRflS.PTRdF.pQFJM.sejLq.JaOCd.HPiiG.TbJOw.yznHn.pDtKH.JlYAQ.OdlNQ.WklAr.BqlFH.xEDxa.JlYAQ.LJtTc.vFYga.cutFr.TbJOw.JaOCd.RmRNv.AVooT.fFDuB.EAaQc.BdcDQ.EAaQc.WklAr.KFWra.YVGwr.LbYfs.vBzbi.kGNwa.GeMpk.YJmUr.xEDxa.HPiiG.CtXBx.nHUct.GGMkz.OdlNQ.ZSVkT.uUAAc."

str_list = str.split('.')
str_enco = "wO9IesKAqPobmRrcOMAoBqsKCGuWW6PhlG0JXTRp9pBqK2pABpvSvW05ZDgTrZah2vRdnYR7CdcIfvNInkDF4hLfamU9f6tI4DyJCbobmdO1HMVu9FveAaP8"
j = 0
dict = "{"
for i in str_enco:
    dict += "\""+str_list[j]+"\""+":"+"\""+i+"\""+",\n"
    j += 1
dict += "}"

print(dict)
