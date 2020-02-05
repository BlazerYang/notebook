# requests

## requests库如何在不修改hosts的请求下请求指定的ip？
```python
requests.get('https://127.0.0.1/s?q=%E6%B5%8B%E8%AF%95&f=json&from=cmd', headers={'Host': 'www.youhost.com'}, verify=False)
```