# MyBatis添加字段程序
版本 1.0

用于MyBatis生成代码后添加字段

作者：L

时间：2021年5月21日 16:07:26



## v 1.1 更新内容

1、优化了繁琐的文件相关信息输入，现在只要复制Java实体类的绝对路径即可完成自动解析；
2、变更字段类型的输入方式，由输入框变更为下拉框，单次只能添加一种字段类型；
3、添加了程序默认置顶；
4、添加了错误信息提示；
5、解决了创建快捷方式找不到模板问题。



## v 1.0 使用方式

使用模板：
模块路径：D:\WorkSpace\java\crrc\crrc_wms\crrc_wms_business\
	说明：到模块，结尾需有反斜杠
包：com.gillion.project.dms3.wms.bas.self
	说明：java包名
类名：SelfGroupContrast
	说明：java类名
字段：testField,testField2
	说明：多字段使用英文逗号间隔
字段名：测试字段,测试字段2
	说明：多字段使用英文逗号间隔，顺序与【字段】一一对应
字段类型：String,BigDecimal
	说明：目前只支持者两种，且BigDecimal类型需要手动改实体类字段长度