import httpx

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}


class http:
    
    def get(link):
        request = httpx.get(link, headers=headers)
        return request
    
    def post(link, data):
        request = httpx.post(link, json=data, headers=headers)
        return request
