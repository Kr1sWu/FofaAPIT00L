import requests
import json
import base64
import pyfiglet

banner = pyfiglet.figlet_format("FofaScan")
print(banner)
"""
1.通过url拼接完成API调用
 - url + Key认证(Base64) + Payload(语法&筛选) 

2.进行结果处理
 - JSON格式数据处理
 - 返回结果保存本地
 - 进行url筛选以进行后期批量POC验证
"""

url = "https://fofa.info/api/v1/search/all"

#query = "app=\"致远互联-OA\""
#query = "app=\"泛微-协同办公OA\""
#query = 'app="泛微-协同办公OA"'
query = 'app="Landray-OA系统"'

query_bs64 = base64.b64encode(query.encode('utf-8')).decode('utf-8')

print("FOFA: "+query)

params = {
    "key": "YOU_API_KEY",
    "qbase64": query_bs64,
    "fields": "host,port",  # 设置只取host和port, 不取ip
    "page": "1",  # 是否翻页,默认1
    "size": "100",  # 每页查询数量
    "full": "false"  # 默认搜索一年内数据,ture则搜索全部数据
}

def sendurl():
    """发送Get请求"""
    # 发送请求
    res = requests.get(url, params=params)
    print(res.url)  # 检查请求url
    print("API KEY : "+params["key"])
    # 转换为JSON
    data = json.loads(res.text)
    # print("data:")
    # print(data)
    # 判断HTTP状态码
    if res.status_code != 200:
        print("Error:", res.status_code)
    else:
        print("\033[92m[REQUEST SUCCESS]!\033[0m"+" 状态码: ", res.status_code)
        print("\033[93mSTARTING ...   TnT\033[0m")
    for i in data["results"]:
        host = i[0]
        port = i[1]
        if port != "80":
            target = host  # +":"+port
        else:
            target = host
        print("\033[94m[info]\033[0m"+target)
        # 把target写入文件
        with open('targets.txt', 'a') as file:
            file.write(str(target)+"\n")
            file.close()

def add_http_prefix(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # 遍历每一行
        for line in infile:
            # 移除行尾的换行符
            stripped_line = line.rstrip()
            if stripped_line.startswith('http'):
                outfile.write(stripped_line + '\n')
            else:
                # 否则，将http://添加到行首
                outfile.write('http://' + stripped_line + '\n')
    print()
    print("程序执行完成! 新的文件名: ", output_file)

# 开始测绘
sendurl()

# 生成目标文件
# 指定输入文件和输出文件的文件名
input_filename = 'targets.txt'
output_filename = 'urls.txt'
add_http_prefix(input_filename, output_filename)


