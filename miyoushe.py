import requests
import json
import time
import random
import hashlib

s = requests.Session()
header = {"Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-cn",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Host": "api-takumi.mihoyo.com",
            "Referer": "https://app.mihoyo.com",
            'User-Agent': 'Hyperion/67 CFNetwork/1128.0.1 Darwin/19.6.0',
            "x-rpc-app_version": "2.2.0",
            "x-rpc-channel": "appstore",
            "x-rpc-client_type": "1",
            "x-rpc-device_id": "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 32)).upper(),
            "x-rpc-device_model": "iPhone11,8",
            "x-rpc-device_name": "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', random.randrange(5))).upper(),
            "x-rpc-sys_version": "14.0.1",}

cookies_user = ""
if (cookies_user == ""):
    cookies_user = input().strip()
    print(cookies_user)

header["Cookie"] = cookies_user

def get_DS():
    """
    IOS sign
    """
    t = int(time.time())
    a = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 6))
    re = hashlib.md5(f"salt=b253c83ab2609b1b600eddfe974df47b&t={t}&r={a}".encode(encoding="utf-8")).hexdigest()
    return f"{t},{a},{re}"

## 签到：post
def miyoushe_signin(module_id):
    """
    docstring
    """
    global header

    ## DS 加密算法: 
    ## Ref: 1. https://github.com/lhllhx/miyoubi/issues/3
    #       2. https://github.com/jianggaocheng/mihoyo-signin/blob/master/lib/mihoyoClient.js
    header["DS"] = get_DS()

    ## 1: bh3, 2: ys, 3: bh2, 4: wd
    sign_data = {'gids': module_id} 
    url_signin = 'https://api-takumi.mihoyo.com/apihub/sapi/signIn'
    res_signin = s.post(url_signin, json=sign_data, headers=header)
    print(res_signin.text)

def miyoushe_forumPost(fid):
    """
    1, 26, 30, 37
    """
    global header

    URL = "https://api-takumi.mihoyo.com/post/api/getForumPostList?forum_id={}&is_good=false&is_hot=false&page_size=20&sort=create".format(fid)
    res = s.get(URL, headers=header)
    res_text = json.loads(res.text)

    URL_upvote = 'https://api-takumi.mihoyo.com/apihub/sapi/upvotePost'
    URL_read = 'https://api-takumi.mihoyo.com/post/api/getPostFull?post_id='

    

    count = 10
    while count > 0:
        post_id = res_text['data']['list'][count]['post']['post_id']
        
        ## 阅读
        header["DS"] = get_DS()
        URL_read_id = URL_read + post_id
        res_read = s.get(URL_read_id,headers=header)

        ## 点赞
        upvote_data = {'is_cancel':False,  'post_id':post_id}
        res_vote = s.post(URL_upvote, json=upvote_data, headers=header)
        print(res_vote.text)
        print("Forum_id: {}, count: {}\n".format(fid, count))
        
        count = count - 1
    
    ## 分享最后一帖
    sharePost(post_id)


def sharePost(post_id):
    global header

    header["DS"] = get_DS()
    URL_post_share = "https://api-takumi.mihoyo.com/apihub/api/getShareConf?entity_id={}&entity_type=1".format(post_id)
    res_share = s.get(URL_post_share, headers=header)
    print(res_share.text)
    

if __name__ == "__main__":
    ## 签到    ## 1: bh3, 2: ys, 3: bh2, 4: wd
    for i in ['1', '2', '3', '4']:
        miyoushe_signin(i)

    ## 帖子相关：阅读，点赞，分享
    for fid in [1, 26, 30, 37]:
        miyoushe_forumPost(fid)