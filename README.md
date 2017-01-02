# 简介
这个程序是实现了三个功能，主要是简化我们平时的日常工作，这个页面是用django做的，bootstrap渲染。
# 一 通过调用脚本往后端服务器发指令
这个页面里面有两个按钮，通过前端ajax传过的参数不同实现不同的脚本调用，下面是往后端发送ajax的js代码：

        function Send(arg) {
            var msg_text = $("textarea").val();
            if($("#ip").val()) {
                var ipaddr = $("#ip").val();
            }
            else{
                var ipaddr=$("#ip").attr("placeholder");
            }
            $.ajax({
                url: "/",
                method: "POST",
                data: {msg: msg_text, act: $(arg).attr("name"), ip:ipaddr},
                success: function(arg1){
                    var callback_dict = $.parseJSON(arg1);
                    var back=callback_dict["back"];
                    back="<p>"+back+"</p>"
                    console.log(back)
                    $(".myform").after(back);
                }//end function
            });//end ajax
        };// end function send

# 二 计算卡号校验位
这个就是根据小于20位的数字字符串计算出另一位数字，源码如下：

    def checkbit(id):
        sum=0
        id='{:0>20}'.format(id)
        for i in range(0,20):
            a=i+1
            b=id[20 - a:21 - a]
            c=2 if i%2==0 else 1
            d=c*int(b)
            e=d if d<10 else int(d/10)+d%10
            sum+=e
        checkbit = 0 if sum % 10 == 0 else 10 - sum % 10
        return checkbit
算是我写的最精简的一段代码了吧。O(∩_∩)O~
# 三 分析指令
这个指令分析主要是分析我们这边和SMS系统交互的指令，也是功能一中发送和收到的指令，指令很长需要一段一段的截和分析，用了反射实现的指令截断，相关反射代码如下：

    if hasattr(t1, action):
        func = getattr(t1, action)
        action_count += 1
        body,l_t20_ac = func(body,l_t20_ac)