import httpx
import asyncio


async def check_domain(domain: str, proxies: dict) -> bool:
    url = f"http://{domain}"
    try:
        async with httpx.AsyncClient(proxies=proxies) as client:
            response = await client.get(url, timeout=5.0)
            return response.status_code == 200
    except httpx.RequestError:
        return False


async def process_domains(input_file: str, valid_output_file: str, invalid_output_file: str, proxies: dict):
    valid_domains = []
    invalid_domains = []
    with open(input_file, 'r') as file:
        domains = [line.strip() for line in file if line.strip()]

    tasks = [check_domain(domain, proxies) for domain in domains]
    results = await asyncio.gather(*tasks)

    for domain, is_valid in zip(domains, results):
        if is_valid:
            valid_domains.append(domain)
        else:
            invalid_domains.append(domain)

    with open(valid_output_file, 'w') as file:
        for domain in valid_domains:
            file.write(f"{domain}\n")

    with open(invalid_output_file, 'w') as file:
        for domain in invalid_domains:
            file.write(f"{domain}\n")


if __name__ == "__main__":
    input_file = 'domain.txt'
    valid_output_file = 'valid_domains_2.txt'
    invalid_output_file = 'invalid_domains_2.txt'
    # proxy = 'http://sph4oqn5f4:ksaqpswd0219%3D@gate.dc.visitxiangtan.com:20001/'
    proxy = 'http://127.0.0.1:10809/'
    proxies = {
        "http://": proxy,
        "https://": proxy
    }

    asyncio.run(process_domains(input_file, valid_output_file, invalid_output_file, proxies))
