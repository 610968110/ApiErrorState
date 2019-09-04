本项目用于将后台的错误字段解析成文件

## 1、执行
直接在命令行输入 builder.py运行脚本，输出路径可以在builder.py中修改

## 2、修改模板
模板中的{{XXX}}是将要被替换字段

 - {{ROOT}} -> 枚举名
 - {{CONTENT_START}} / {{CONTENT_END}} -> 两个标签中间的内容标识为内容体
 - {{KEY}} -> json的key，目前作为msg
 - {{VALUE}} -> json的code，目前作为错误码

## 3、配置项
目前有 append.config 和 transform.config 两个配置文件，具体说明在配置文件中