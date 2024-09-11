def deduplicate_links(input_file: str, output_file: str):
    links = set()

    # 读取输入文件中的所有链接
    with open(input_file, 'r') as file:
        for line in file:
            link = line.strip()
            if link:
                links.add(link)

    # 将去重后的链接写入输出文件
    with open(output_file, 'w') as file:
        for link in sorted(links):  # 按字典序排序（可选）
            file.write(f"{link}\n")


if __name__ == "__main__":
    input_file = 'domain.txt'  # 指定输入文件名
    output_file = 'deduplicated_links.txt'  # 指定输出文件名

    deduplicate_links(input_file, output_file)
    print(f"去重后的链接已保存到 {output_file}")
