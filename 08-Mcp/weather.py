from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP 服务器
mcp = FastMCP("weather")

# 常量
NWS_API_BASE = "https://api.weather.gov" # 美国国家气象局 API 基础 URL
USER_AGENT = "weather-app/1.0" # API 请求的用户代理


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """向 NWS API 发出请求并进行适当的错误处理。"""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status() # 如果请求失败 (状态码 >= 400)，则引发 HTTPError
            return response.json()
        except Exception as e:
            # 捕获所有可能的异常 (例如超时、连接错误、JSON 解码错误)
            print(f"请求 NWS API 时出错: {url}, 错误: {e}")
            return None


def format_alert(feature: dict) -> str:
    """将警报要素格式化为可读字符串。"""
    props = feature["properties"]
    return f"""
事件: {props.get('event', '未知')}
区域: {props.get('areaDesc', '未知')}
严重性: {props.get('severity', '未知')}
描述: {props.get('description', '无描述')}
指示: {props.get('instruction', '无具体指示')}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """获取美国某个州的天气警报。

    Args:
        state: 两个字母的美国州代码 (例如 CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "无法获取警报或未找到警报。"

    if not data["features"]:
        return f"该州 ({state}) 当前无生效的警报。"

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """获取某个地点的天气预报。

    Args:
        latitude: 地点的纬度
        longitude: 地点的经度
    """
    # 首先获取预报网格点信息的端点 URL
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data or "properties" not in points_data or "forecast" not in points_data["properties"]:
        return f"无法获取该地点 ({latitude}, {longitude}) 的预报数据。"

    # 从网格点信息响应中获取实际的预报 URL
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data or "properties" not in forecast_data or "periods" not in forecast_data["properties"]:
        return "无法获取详细的预报信息。"

    # 将预报时段格式化为可读的预报
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # 仅显示接下来的 5 个时段
        forecast = f"""
{period['name']}:
温度: {period['temperature']}°{period['temperatureUnit']}
风速: {period['windSpeed']} {period['windDirection']}
预报: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    if not forecasts:
        return "未能生成预报信息。"

    return "\n---\n".join(forecasts)


if __name__ == "__main__":
    # 初始化并运行服务器
    print("NWS Weather MCP 服务启动...")
    print(f"服务名称: {mcp.name}")
    print("可用工具:")
    for tool_name, tool_func in mcp.tools.items():
        # 获取文档字符串的第一行作为工具的简短描述
        doc_lines = tool_func.__doc__.strip().splitlines()
        short_desc = doc_lines[0] if doc_lines else "无描述"
        print(f"  - {tool_name}: {short_desc}")
    print("正在监听 stdio...\n")
    mcp.run(transport="stdio")
