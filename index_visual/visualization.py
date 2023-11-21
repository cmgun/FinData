import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# 示例数据
df = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=30),
    'Values': [30, 35, 40, 25, 20, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165]
})

# 初始化 Dash 应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    dcc.Graph(id='bar-chart'),
    dcc.Graph(
        id='line-chart',
        figure={
            'data': [
                go.Scatter(x=df['Date'], y=df['Values'], mode='lines+markers')
            ],
            'layout': go.Layout(title='历史点数', clickmode='event+select')
        }
    ),
])

# 回调函数更新柱状图
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('line-chart', 'clickData')]
)
def update_bar_chart(clickData):
    if clickData is None:
        # 默认值
        values = [20, 30, 40, 50]
    else:
        date = clickData['points'][0]['x']
        # 根据日期获取值，这里简化处理为一个固定值
        values = [50, 60, 70, 80] # 这里应根据实际需要替换逻辑

    # 更新柱状图
    data = [
        go.Bar(
            x=['A', 'B', 'C', 'D'],
            y=values,
            marker_color=['green' if v > 50 else 'red' for v in values]
        )
    ]
    return {'data': data, 'layout': go.Layout(title='水位观察')}

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)
