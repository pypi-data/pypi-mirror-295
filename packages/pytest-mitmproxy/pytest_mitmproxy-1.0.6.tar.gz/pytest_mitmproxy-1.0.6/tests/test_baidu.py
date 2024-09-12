import pytest
import requests


def test_baidu(mitmdump_proxy):
    mitmdump_proxy.url_filter = "baidu"

    requests.get("http://www.baidu.com")

    urls = mitmdump_proxy.get_urls()
    assert "baidu" in "".join(urls)


if __name__ == "__main__":
    pytest.main(["-vs"])
