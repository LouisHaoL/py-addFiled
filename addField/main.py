import os
import tkinter
import windnd
import locale
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

path = "D:\\WorkSpace\\java\\crrc\\crrc_wms\\crrc_wms_business\\"
base_package = "com.gillion.project.dms3.wms.bas.self"
modelName = "SelfGroupContrast"
fieldNames = "field"
fieldNameCns = "测试字段"
fieldTypes = "String"


def join_under_line(string):
    pattern = re.compile(r'([A-Z])')
    return re.sub(pattern, "_" + r'\1', string).upper()


def find_file(file_path, file_name):
    for root, dirs, files in os.walk(file_path):
        if file_name in dirs or file_name in files:
            root = str(root)
            return os.path.join(root, file_name)
    return -1


def get_template_content(template_file_name, file_name, field_name, field_name_cn, field_type):
    field_template = open(os.path.dirname(os.path.realpath(sys.argv[0])) + "/template/" + template_file_name, "r", encoding="utf-8")
    content = field_template.read()
    field_template.close()
    fields = field_name.split(",")
    field_cns = field_name_cn.split(",")
    all_content = ""
    for index, field in enumerate(fields):
        field_cn = field_cns[index]
        act_content = content.replace("ModelName", file_name)
        act_content = act_content.replace("字段名", field_cn)
        act_content = act_content.replace("String", field_type)
        if field_type == "BigDecimal":
            act_content = act_content.replace("VARCHAR", "NUMERIC")
        act_content = act_content.replace("fieldName", field)
        add_field_upper = join_under_line(field)
        act_content = act_content.replace("FIELD_NAME", add_field_upper)
        field_name_upper = field[0].upper() + field[1:]
        act_content = act_content.replace("FieldName", field_name_upper)
        all_content += act_content
    return all_content


def get_file_content(file_name, is_java: bool):
    model_file = get_file_path(file_name, is_java)
    if model_file == -1:
        return ""
    file = open(model_file, "r", encoding="utf-8")
    content = file.read()
    file.close()
    return content


def write_file_content(file_name, content, is_java: bool):
    model_file = get_file_path(file_name, is_java)
    if model_file == -1:
        return ""
    file = open(model_file, "w", encoding="utf-8")
    file.write(content)
    file.close()


def get_file_path(file_name, is_java):
    if is_java:
        package_path = path + "src\\java\\" + base_package.replace(".", "\\")
    else:
        package_path = path + "src\\resources\\" + base_package.replace(".", "\\") + "\\mapper"
    model_file = find_file(package_path, file_name)
    if model_file == -1:
        showinfo("错误", "文件未找到")
    return model_file


def write_model_clz():
    file_name = modelName + ".java"
    content = get_file_content(file_name, True)
    field_method = get_template_content("fieldTemplate.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = content.replace("//fields", "//fields\n" + field_method)
    get_set_content = get_template_content("getSetMethodTemplate.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r"(.*@Override\n.*equals)"), get_set_content + r'\1', content)
    write_file_content(file_name, content, True)


def write_example_clz():
    file_name = modelName + "Example.java"
    content = get_file_content(file_name, True)
    example_template_content = get_template_content("exampleTemplate.txt", modelName, fieldNames, fieldNameCns,
                                                    fieldTypes)
    content = re.sub(re.compile(r'(super\(columnMaps\);\n.*\n)'), r'\1' + example_template_content, content)
    write_file_content(file_name, content, True)


def write_mapper_xml():
    file_name = modelName + "Mapper.xml"
    content = get_file_content(file_name, False)
    upper1 = get_template_content("xmlUpperTemplate1.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r'(<id column=.*\n)'), r'\1' + upper1, content)

    upper23 = get_template_content("xmlUpperTemplate23.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r'(<sql id=\"Base_Column_List.*\n)'), r'\1' + upper23, content)
    content = re.sub(re.compile(r'(insert into .*\(.*\n)'), r'\1' + upper23, content)

    upper4 = get_template_content("xmlUpperTemplate4.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r'(insert into .*\n.*<trim prefix.*\n)'), r'\1' + upper4, content)

    upper5 = get_template_content("xmlUpperTemplate5.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r'(<update id=\"updateByExampleSelective\".*\n.*update.*\n.*<set.*\n)'),
                     r'\1' + upper5, content)

    upper6 = get_template_content("xmlUpperTemplate6.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r'(<update id=\"updateByExample\".*\n.*update.*set.*\n)'), r'\1' + upper6, content)

    upper7 = get_template_content("xmlUpperTemplate7.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r'(<update id=\"updateByPrimaryKeySelective\"(.*\n)*.*<set.*\n)'), r'\1' + upper7,
                     content)

    upper8 = get_template_content("xmlUpperTemplate8.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r'(<update id=\"updateByPrimaryKey\"(.*\n)*.*update.*set.*\n)'), r'\1' + upper8,
                     content)

    lower1 = get_template_content("xmlLowerTemplate1.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r'(\)\n.*values \(.*\n)'), r'\1' + lower1, content)

    lower2 = get_template_content("xmlLowerTemplate2.txt", modelName, fieldNames, fieldNameCns, fieldTypes)
    content = re.sub(re.compile(r'(<trim prefix=\"values \(\".*\n)'), r'\1' + lower2, content)

    write_file_content(file_name, content, False)


def startup():
    global path, base_package, modelName, fieldNames, fieldNameCns, fieldTypes
    # 绝对路径
    all_path = path_text.get()
    if not all_path.endswith('.java'):
        showinfo('错误', '路径不是Java文件！')
        return
    left = all_path.find('src\\java')
    if left == -1:
        showinfo('错误', '路径不是常规项目路径，没有找到“src\\java”！')
        return
    path = all_path[0: all_path.find('src\\java')]
    paths = all_path.split('\\')
    modelName = paths[len(paths) - 1].replace('.java', '')
    right = all_path.rfind(f'\\domain\\{modelName}')
    if right == -1:
        showinfo('错误', f'路径不是常规项目路径，没有找到“\\domain\\{modelName}”！')
        return
    base_package = all_path[left: right].replace('\\', '.').replace('src.java.', '')
    fieldNames = field_text.get()
    fieldNameCns = field_cn_text.get()
    fieldTypes = field_type_text.get()
    try:
        write_model_clz()
        write_example_clz()
        write_mapper_xml()
        showinfo('提示', '添加成功！')
    except Exception as e:
        showinfo('错误', f'文件/模板未找到！\n{e}')
        print(e)


def file_drag_in(files):
    path_text.delete(0, END)
    path_text.insert(0, files[0].decode(locale.getpreferredencoding()))


if __name__ == '__main__':

    top = tkinter.Tk(className='添加字段小工具')
    top.geometry("390x160")
    # 置顶
    top.wm_attributes('-topmost', 1)
    # 文件拖放
    windnd.hook_dropfiles(top, func=file_drag_in)
    # 文件路径
    item1 = Label(top, text='Java实体类：')
    item1.grid(row=0, column=0)
    path_text = Entry(top)
    path_text.grid(row=0, column=1, padx=10, pady=5)
    path_text.place(width=300, x=80)

    item4 = Label(top, text='字段：')
    item4.grid(row=1, column=0)
    field_text = Entry(top)
    field_text.grid(row=1, column=1, padx=10, pady=5)
    field_text.place(width=300, x=80, y=23)

    item5 = Label(top, text='字段名：')
    item5.grid(row=2, column=0)
    field_cn_text = Entry(top)
    field_cn_text.grid(row=2, column=1, padx=10, pady=5)
    field_cn_text.place(width=300, x=80, y=46)

    item6 = Label(top, text='字段类型：')
    item6.grid(row=3, column=0)
    field_type_text = ttk.Combobox(top)
    field_type_text['value'] = ('String', 'BigDecimal')
    field_type_text.current(0)
    field_type_text.grid(row=3, column=1, padx=10, pady=5)
    field_type_text.place(width=100, x=80, y=69)

    Button(top, text='添加', width=10, command=startup).grid(row=4, column=0, sticky=E, padx=10, pady=5)
    Button(top, text='退出', width=10, command=top.quit).grid(row=4, column=1, sticky=E, padx=10, pady=5)
    item7 = Label(top, text='作者：L')
    item7.grid(row=5, column=0)
    item8 = Label(top, text='版本：1.1')
    item8.grid(row=5, column=1)

    top.mainloop()
