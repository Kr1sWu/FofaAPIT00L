import requests
import json
import base64
import pyfiglet

banner = pyfiglet.figlet_format("FofaScan")
print(banner)

url = "https://fofa.info/api/v1/search/all"

"""这里定义搜索语法"""
query = "app=\"泛微-协同办公OA\""

# 对搜索语法进行Base64编码
query_bs64 = base64.b64encode(query.encode('utf-8')).decode('utf-8')

params = {
    "key": "YOU_API_KEY",
    "qbase64": query_bs64,
    "fields": "host,port",  # 设置只取host和port, 不取ip
    "page": "1",  # 是否翻页,默认1
    "size": "100",  # 每页查询数量
    "full": "ture"  # 默认搜索一年内数据,ture则搜索全部数据
}


def sendurl():
    """发送Get请求"""
    # 发送请求
    res = requests.get(url, params=params)
    # 检查请求url
    print(res.url)
    # 转换为JSON
    data = json.loads(res.text)
    # 判断HTTP状态码
    if res.status_code != 200:
        print("Error:", res.status_code)
    else:
        print("Success! ", res.status_code)
    for i in data["results"]:
        # 从列表里取出host和port
        host = i[0]
        port = i[1]
        if port != "80":
            target = host  # +":"+port
        else:
            target = host
        # 检查从JSON列表提取的结果
        print(target)
        # 把target写入文件
        with open('targets.txt', 'a') as file:
            # file = open('targets.txt', 'a')
            file.write(str(target)+"\n")
            file.close()


# 处理文件
def add_http_prefix(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # 遍历每一行
        for line in infile:
            # 移除行尾的换行符
            stripped_line = line.rstrip()

            # 如果行以http开头（包括http和https），则直接保留这行
            if stripped_line.startswith('http'):
                outfile.write(stripped_line + '\n')
            else:
                # 否则，将http://添加到行首
                outfile.write('http://' + stripped_line + '\n')
    print("程序执行完成! 目标url文件名: ", output_file)

# 开始测绘
sendurl()
# 生成目标文件
# 指定输入文件和输出文件的文件名
input_filename = 'targets.txt'
output_filename = 'new_targets.txt'
add_http_prefix(input_filename, output_filename)
