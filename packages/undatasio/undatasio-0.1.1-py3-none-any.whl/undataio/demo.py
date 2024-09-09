from undata import upload, parser, show_upload, download, show_vision, download_type_info

# 上传
# file = r'Z:\xll\pdftest\test4'
# res = upload(token='025ae1da7598456daa802fef7873e31b', file_lir_path=file)
# print(res)

# 查看上传文件
# res = show_upload(token='025ae1da7598456daa802fef7873e31b')
# print(res)

# 解析
# res = parser(token='025ae1da7598456daa802fef7873e31b', file_name_list=['棉花标准仓单销售合同.pdf',
#                                                                        '调整组合结构应对短期波折基金每日资讯20150608.pdf'])
# print(res)


# 查看历史版本
# res = show_vision(token='025ae1da7598456daa802fef7873e31b')
# print(res)


# 下载指定版本
# res = download(token='025ae1da7598456daa802fef7873e31b', vision='v17')
# print(res)


# 下载指定类型的文本
res = download_type_info(token='025ae1da7598456daa802fef7873e31b',
                         type_info=['title', 'text'],
                         file_name='调整组合结构应对短期波折基金每日资讯20150608.pdf',
                         vision='v17')

print(res)
