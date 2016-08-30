#coding:utf-8
import re
action_dict={
    "g":"获取订户号",
    "Q":"修改订户数据",
    "V":"重新发送所有数据包",
    "P":"清除密码",
    "C":"创建订户",
    "U":"取消配对",
    "D":"删除订户",
    "Y":"设置个人区域位",
    "A":"授权服务或OPPV",
    "X":"取消服务或OPPV",
    "O":"发送OSD",
    "E":"发送email",

}
OSD_dic={
    "A":"总是",
    "S":"加密",
    "T":"Taping 没授权",
}
OSD_P_dic={
    "H":"高",
    "M":"中",
    "L":"低",
}
def handle_card(line,l):
    l.append(["报文 ", line])
    # l.append(["长度 ",len(line)])
    l.append(["分析 "])
    l.append(["报文头 ",line[:37]])
    # l.append([line[33:37]])
    l.append(["报文体 ",line[37:]])
    # l.append(["Head Length ", len(line[:37])])
    # l.append(["Version ",line[:4]])
    # l.append(["Type ",line[4]])
    # l.append(["Length ",line[5:9]])
    # l.append(["From ID ",line[9:13]])
    # l.append(["Connection ID ",line[13:15]])
    # l.append(["To ID ",line[15:19]])
    # l.append(["Date ",line[19:27]+" "+line[27:33]])
    # l.append(["Sequence ID ", line[33:37]])
    l.append(["十六位校验位 ", line[-16:]])
    body=line[37:-16]
    return (body,l)
def action_S(body,l):
    # print len(body)
    # l.append(["Body ",body])
    l.append(["动作类型区域 ",body[:11]])
    l.append(["动作类型 ",body[0]])
    l.append(["动作优先级 ",body[1]])
    l.append(["再循环优先级 ",body[2]])
    if len(body[3:11])!=body[3:11].count("0"):
        l.append(["订户号 ",body[3:11]])
    else:
        l.append(["保持不变 ",body[3:11]])
    l.append(["动作编码区域 ", body[11:]])
    actions=body[11:]
    return (actions,l)
def action_g(actions,l):
    l.append(["卡号 ", actions[1:13]])
    return (actions[13:],l)
def action_E(actions,l):
    l.append(["卡号 ", actions[1:13]])
    return (actions[13:],l)
def action_O(actions,l):
    l.append(["频道号 ", actions[1:5]])
    l.append(["OSD控制 ", actions[5],OSD_dic.get(actions[5])])
    l.append(["持续时间/s ", actions[6:8]])
    l.append(["优先级 ", actions[8],OSD_P_dic.get(actions[8])])
    if actions[9:11]=="00":
        l.append(["没有压缩 ", actions[9:11]])
    else:
        l.append(["压缩类型 ", actions[9:11]])
    if actions[11:13]=="FD":
        l.append(["OSD到版本 ", actions[11:13]])
    else:
        l.append(["OSD号 ", actions[11:13]])
    l.append(["OSD长度 ", actions[13:17]])
    l.append(["语言 ", actions[17:19]])
    l.append(["区域1 ", actions[19:21]])
    l.append(["OSD文本区域", actions[21:63]])
    return (actions[63:],l)
def action_Q(actions,l):
    l.append(["区域编码 ", actions[1:9]])
    l.append(["保持不变 ", actions[9:16]])
    return (actions[16:],l)
def action_C(actions,l):
    l.append(["卡号 ", actions[1:13]])
    l.append(["区域编码 ", actions[13:21]])
    l.append(["保持不变 ", actions[21:28]])
    l.append(["CURRENCY", actions[28:32]])
    l.append(["POPID", actions[32:36]])
    l.append(["STBID ", actions[36:48]])
    return (actions[48:],l)
def action_V(actions,l):
    return (actions[1:],l)
def action_D(actions,l):
    return (actions[1:],l)
def action_P(actions,l):
    return (actions[1:],l)
def action_U(actions,l):
    return (actions[1:],l)
def action_Y(actions,l):
    if actions[1]=="A":
        l.append(["设置区域位 ", actions[1]])
    else:
        l.append(["清除区域位 ", actions[1]])
    l.append(["个人区域位 ", actions[2:4]])
    return (actions[4:],l)
def action_A(actions,l):
    l.append(["服务或OPPV号 ", actions[1:5]])
    l.append(["OPPV过期时间 ", actions[5:13]])
    l.append(["Taping 授权 ", actions[13]])
    return (actions[14:],l)
def action_X(actions,l):
    l.append(["服务或OPPV号 ", actions[1:5]])
    return (actions[5:],l)

