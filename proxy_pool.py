import asyncio
import aiohttp
import helper_functions

working_set = set()
VALID_STATUSES = [200, 301, 302, 307, 404]


async def task_coroutine(session, proxy):
    try:
        async with session.get("http://ident.me/", proxy=proxy, ssl=False, timeout=600) as resp:
            await resp.text()
            if resp.status in VALID_STATUSES:
                print('Status Code: ' + str(resp.status))
                helper_functions.set_working(proxy, working_set)
    except Exception as e:
        print("Exception: ", e)


async def main_proxy_pool() -> list:
    proxy_list = open("MasterProxyList", "r").read().strip().split("\n")
    tcp_connection = aiohttp.TCPConnector(limit=250)
    header = {"Authorization": "Basic bG9naW46cGFzcw=="}
    async with aiohttp.ClientSession(connector=tcp_connection, headers=header, trust_env=True) as session:
        try:
            tasks = [asyncio.create_task(task_coroutine(session, i)) for i in proxy_list]
            for task in tasks:
                await task
        except Exception as e:
            print(e)
        await asyncio.sleep(0)
    lst = [a for a in working_set]
    print('Number of useable proxies: ' + str(len(lst)))
    return lst


# asyncio.run(main_proxy_pool())