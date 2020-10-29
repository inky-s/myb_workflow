# myb_workflow

参照

1. https://github.com/lhllhx/miyoubi/issues/3
2. https://github.com/jianggaocheng/mihoyo-signin/blob/master/lib/mihoyoClient.js
3. https://github.com/y1ndan/genshin-impact-helper （GitHub workflow用法有点秀！！）

进行的米游社自动签到+阅帖改进版本



----

Cookie这块我没有细化。。。。Ref 1有取cookie的步骤。 Ref 3有使用Setting->Secret用于workflow的步骤

我事实上是直接把Thor里面拿到的cookie(格式如下)直接复制粘贴成为Setting->Secret里面的变量，然后在Action里面跑。（详见Ref 3)

```
stuid=123456;stoken=abcdef;login_ticket=1234asdf;
```

