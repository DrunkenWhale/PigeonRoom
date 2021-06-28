"""

登陆系统 签发统一的token 需要前端在请求的时候带上

delete请求将token放在params内

post请求将token放在headers内

不带token除了login和register两个接口能够正常使用

其他全部都无法使用


好吧 其实并不是严格遵守上述规则的 还是有小小的改动的 （总有那么几个特例嘛）

哦对了 请把 register接口要求的sex用0/1的形式传上来 可能是因为我对序列化理解有问题 反正没办法直接得到bool值

"""
