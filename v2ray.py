import requests
import base64
import json
import time


# 订阅链接
subscription_url = "https://url"

# 下载订阅内容
response = requests.get(subscription_url)
response.raise_for_status()  # 检查响应状态码，如果不是200会引发异常
subscription_data = response.text

# 解码订阅内容（通常是Base64编码）
decoded_subscription_data = base64.b64decode(subscription_data).decode()
print(decoded_subscription_data)
print(type(decoded_subscription_data))


vmess_links = decoded_subscription_data.strip().split("\n")

# 创建一个空列表来存储解析后的vmess链接
vmess_nodes_base64 = []

# 将每个vmess链接添加到列表中
for link in vmess_links:
    vmess_nodes_base64.append(link)

    # 解码Base64字符串
    decoded_node_data = base64.urlsafe_b64decode(link.split("://")[1] + "==").decode()

    # 解析JSON对象以获取节点信息
    node_info = json.loads(decoded_node_data)


    print(node_info)

    # 提取节点相关信息
    host = node_info.get("add", "")
    port = node_info.get("port", "")
    method = node_info.get("method", "")
    password = node_info.get("password", "")

    print(f"Host: {host}, Port: {port}, Method: {method}, Password: {password}")

    target_url = "https://ip.sb"
    proxy_url = f"ss://{node_info['method']}:{node_info['password']}@{node_info['host']}:{node_info['port']}"
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    try:
        response = requests.get(target_url, proxies=proxies)
        
        # 检查响应状态码
        if response.status_code == 200:
            print("成功连接到节点并发送请求")
            print("响应内容:")
            print(response.text)
        else:
            print(f"连接到节点但请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"连接节点和发送请求时出错: {str(e)}")
