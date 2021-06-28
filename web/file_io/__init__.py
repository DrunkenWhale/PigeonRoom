'''
文件上传接口

限定最大64MB的文件上传

所有接口都必须拿到token

使用了werkzeug.secure_file来检查文件名 顺便改了下源代码 让它支持中文来着

file_list的接口虽然是用get请求 但是请将token放在form内

别问为什么没有严格统一 问就是前端我自己在写 图省事.jpg


'''