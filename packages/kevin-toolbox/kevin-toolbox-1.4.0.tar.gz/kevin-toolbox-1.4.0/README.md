# kevin_toolbox

一个通用的工具代码包集合



环境要求

```shell
numpy>=1.19
pytorch>=1.2
```

安装方法：

```shell
pip install kevin-toolbox  --no-dependencies
```



[项目地址 Repo](https://github.com/cantbeblank96/kevin_toolbox)

[使用指南 User_Guide](./notes/User_Guide.md)

[免责声明 Disclaimer](./notes/Disclaimer.md)

[版本更新记录](./notes/Release_Record.md)：

- v 1.4.0 （2024-09-11）【bug fix】【new feature】【incompatible change】
  - patches
    - for_matplotlib.common_charts
      - 【bug fix】fix bug in plot_confusion_matrix() for paras label_to_value_s，删除了对参数 label_to_value_s 的不合理的检验，并且支持更加自由的 label_to_value_s 设置，比如允许 label_to_value_s 中缺少 data_s 中已有的 label_idx，或者含有部分 data_s 中未见的 label_idx。
      - 【bug fix】fix bug in plot_lines()，对接受的输入 data_s 进行 copy，避免后续操作引起输入意外改变。
      - 增加测试用例。
    - for_streamlit.markdown
      - 【new feature】add show_image()，对 st.markdown 中图片显示部分的改进，能够正确显示本地的图片。
      - 【new feature】add show_table()，对 st.markdown 中表格显示部分的改进，支持以下多种方式来显示表格。
      - 【new feature】add show()，st.markdown 的改进版。
      - 增加测试用例。
  - data_flow.file
    - markdown【incompatible change】【new feature】
      - 【refactor and modify】
        - generate_table() ==> table.generate_table()
        - generate_link() ==> link.generate_link()
        - save_images_in_ndl() ==> utils.save_images_in_ndl()
        - parse_table() ，可以使用 table.convert_format() 来代替实现表格格式的转换
      - table
        - 【new feature】新增 Table_Format、get_format()、convert_format() 用于表格格式的转换，目前支持以下几种格式：
          - simple_dict 简易字典模式：`{<title>: <list of value>, ...}`
          - complete_dict 完整字典模式：`{<index>: {"title": <title>, "values": <list of value>}, ...}`
          - matrix 矩阵形式：`{"matrix": [[...], [...], ...], "orientation":...(, "chunk_nums":..., "chunk_size":...)}`
        - 【new feature】add find_tables()，查找文本中的表格
          - 当 b_compact_format 设为 True，此时返回 table_ls，其中每个元素是一个 MATRIX 格式的表格
          - 当 b_compact_format 设置为 False，此时返回 (table_ls, part_slices_ls, table_idx_ls)，其中 part_slices_ls 是表格和表格前后文本在 text 中对应的 slice，而 table_idx_ls 指出了 part_slices_ls 中第几个元素对应的是表格，table_idx_ls 与 table_ls 依次对应。
        - 【new feature】add padding_misaligned_values()， 将标题下长度不相等的 values 补齐
        - convert
          - 格式转换相关的函数，包括 complete_to_matrix() 和 matrix_to_complete()
      - link
        - 【new feature】add find_links()，查找文本中的链接。与find_tables()类似，也支持 b_compact_format 参数。
      - 增加测试用例。

