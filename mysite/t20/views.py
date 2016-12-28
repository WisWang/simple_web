#coding:utf-8
from django.shortcuts import render,HttpResponse
from t20 import t1,func_checkbit
import json,subprocess
# Create your views here.
int_char_dic={
    1:"一",
    2:"二",
    3:"三",
    4:"四",
    5:"五",
    6:"六",
    7:"七",
    8:"八",
}
def week(request):
    return render(request,"week.html")
def analy(request):
    if request.method=="POST":
        # print request.POST
        t20=request.POST["t20"]
        result=""
        if not t20:
            return render(request, "home.html", {"error": "this can't be blank"})
        l_t20=[]
        print t20,type(t20)
        lines=t20.split("\n")
        count=0
        for line in lines:
            l_t20_ac=[]
            line = line.strip()
            if line.endswith("\""):
                line = line[:-2]
            if not (line.startswith("000") ):
            # if not (line.startswith("000") or line.startswith(";000")):
                continue
            if line.startswith(";"):
                #the branch deal with the response
                response_t20="this is a response"
                l_t20_ac.append("this is a response")
                line = line[1:]
                (body,l_t20_ac) = t1.handle_card(line,l_t20_ac)
                # (body, l_t20_ac) = t1.action_S(body, l_t20_ac)
                l_t20_ac.append(["body:",body])

            else:
                # l_t20_ac.append(["T20指令"+int_char_dic.get(len(l_t20)+1)])
                body, l_t20_ac = t1.handle_card(line,l_t20_ac)
                verify_bit=l_t20_ac.pop(-1)
                #l_t20_ac代表具体一个T20指令，l_t20代表所有的指令
                body, l_t20_ac = t1.action_S(body, l_t20_ac)
                action_count=0
                while True:
                    # break
                    #only process the head and action type area
                    if body.startswith("-xn"):
                        body = t1.action_xn(body)
                        action_count += 1
                    if body.startswith("-Bq"):
                        body = body[1:]
                    action = "action_" + body[0]
                    # l_t20_ac.append([])
                    if t1.action_dict.get(body[0]):
                        l_t20_ac.append(["动作编码 ",t1.action_dict[body[0]],body[0]])
                        # print "\033[35;1mThis action means: %s \033[0m" % t1.action_dict[body[0]]
                    if hasattr(t1, action):
                        func = getattr(t1, action)
                        action_count += 1
                        body,l_t20_ac = func(body,l_t20_ac)
                        # print "\033[33;1mAction %s finished\033[0m" % action
                        # body=left
                    else:
                        # print "\033[31;1mLeft Body: %s \033[0m" % body
                        l_t20_ac.append(["剩余动作:",body])
                        l_t20_ac.append(verify_bit)
                        break
                    if len(body) == 0:
                        # l_t20_ac.append(["***结束***"])
                        l_t20_ac.append(verify_bit)
                        break
                # l_t20_ac.append(["body:", body])
            l_t20.append(l_t20_ac)
        return render(request,"home.back.html",{"result":l_t20,})
    return render(request,"home.back.html")

def handle(request):
    if request.method=="POST":
        print request.POST
        cmd_list=["./send_t20.sh"]
        ipaddr=request.POST["ip"]
        print ipaddr
        cmd_list.append(ipaddr)
        oragin_t20=request.POST["msg"]
        cmd_list.append(oragin_t20)
        if request.POST["act"]=="send_t20":
            cmd_list.append("1")
        feedback_dict={}
        obj = subprocess.Popen(cmd_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               cwd="/wis/webt20")
        buff = obj.stdout.readlines()
        # feedback_dict["back"]=data["action"]+"success"
        feedback_dict["back"]=buff[0].strip()
        if request.POST["act"] == "send_t20":
            feedback_dict["back"] = buff[2].strip()
        feedback_dict["other"]="test"
        return HttpResponse(json.dumps(feedback_dict))
    else:
        return render(request,"handle_t20.html")
def checkbit(request):
    if request.method == "POST":
        checkbit_cardlist=[]
        cardlist = request.POST["t20"]
        cardlist=cardlist.split()
        for i in cardlist:
            check_b=func_checkbit.checkbit(i)
            checkbit_cardlist.append('{:0>12}'.format(i+str(check_b)))
        return render(request, "checkbit.html", {"result": checkbit_cardlist,})
    else:
        return render(request,"checkbit.html")

