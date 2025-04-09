from datetime import datetime

def get_current_time():
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    # now.weekday() 返回周一=0，周日=6
    weekday = weekdays[now.weekday()]
    return f"当前时间是：{time_str}，{weekday}"

def get_weather(location):
    return f"查询到{location}的天气是晴天"

if __name__ == '__main__':
    print(get_current_time())