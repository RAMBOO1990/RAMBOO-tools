# RAMBOO-tools
个人实用工具集，包含多列数据处理工具

## Install 安装
```sh
pip install <code_path>
```

## Usage 用法
### 命令行类
直接使用命令即可，均支持shell管道操作
#### csv2txt txt2csv xls2txt txt2xls 格式转换
```sh
cat test.csv | csv2txt > test.txt
cat test.txt | txt2csv > test.csv
cat test.xlsx | xls2txt > test.txt
cat test.txt | txt2xls > test.xlsx
```
#### expand_line 多列数据单行展开
参数：
* -f --field_num：待处理列号（从1开始计数，默认1）
* -s --expand_separator：分隔符（默认","）
* -k --keep_empty_line：是否保留空行
> 单列数据且分隔符为单字符可用 tr <分隔符> '\n'
```sh
echo '111\t222,333,444\t555' | expand_line -f 2
```
输出：
```
111	222	555
111	333	555
111	444	555
```

#### cut2 shell原生cut命令扩展，-d分隔符支持多字符
参数：
* -f --field_num：待处理列号（从1开始计数，默认1）
* -s --expand_separator：分隔符
```sh
echo '11|||22|||33|||44' | cut2 -f 1,3,4 -d '|||'
```
输出
```
11|||33|||44
```

#### pp 字符串格式化
参数：
* -f --field_num：输出列号（从1开始计数，默认1）
* -s --field_num_separator：列号分隔符（默认","）
* --not_fold：不折叠（默认折叠30行之后依然不变化缩进的数据）
* --format_str：格式化字符串类型内容（默认不格式单/双引号内内容）
```sh
echo "Mount3cRequest(product_id='111111', search_img_info=None, attrs_info=AttrsInfo(ocrs=None, title_ners=None, attrs_original=None, sku_props={'网络类型': 'SA/NSA双模(5G)', '机身颜色': 'Mate40【秘银色】', '套餐类型': '官方标配', '存储容量': '8+128GB', '_sku_id_': '22222222'}), brand_info=BrandInfo(brand_name_ai='Huawei/华为', brand_id_ai='333333', brand_name_original='', brand_id_original=''), ctg_info=CategoryInfo(ctg_ai='手机#智能机', ctg_ai_id='444444', ctg_original='', ctg_original_id=''), title='Huawei/华为 Mate 40 pro 5G手机官方旗舰店正品mate40pro5g荣耀p30直降mate30保时捷M40', Base=Base(LogID='', Caller='', Addr='', Client='', TrafficEnv=None, Extra=None))" | pp
```
输出
```
Mount3cRequest(
    product_id='111111',
    search_img_info=None,
    attrs_info=AttrsInfo(
        ocrs=None,
        title_ners=None,
        attrs_original=None,
        sku_props={
            '网络类型': 'SA/NSA双模(5G)',
            '机身颜色': 'Mate40【秘银色】',
            '套餐类型': '官方标配',
            '存储容量': '8+128GB',
            '_sku_id_': '22222222'
        }
    ),
    brand_info=BrandInfo(
        brand_name_ai='Huawei/华为',
        brand_id_ai='333333',
        brand_name_original='',
        brand_id_original=''
    ),
    ctg_info=CategoryInfo(
        ctg_ai='手机#智能机',
        ctg_ai_id='444444',
        ctg_original='',
        ctg_original_id=''
    ),
    title='Huawei/华为 Mate 40 pro 5G手机官方旗舰店正品mate40pro5g荣耀p30直降mate30保时捷M40',
    Base=Base(
        LogID='',
        Caller='',
        Addr='',
        Client='',
        TrafficEnv=None,
        Extra=None
    )
)
```

#### edit_dis 计算两列数据之间的编辑距离
参数
* -f --field_num：待计算数据列号1（从1开始计数，默认1）
* -f2 --field_num_2：待计算数据列号2（从1开始计数，默认2）
```sh
echo 'hello world\thello ramboo' | edit_dis
```
输出
```
hello world	hello ramboo	6
```

### lib类
#### stream_processor 流式多列处理器
> 默认保持原数据，新结果添加在最后一列
```py
from ramboo_tools.stream_processor import StreamProcessor
class MyProcessor(StreamProcessor):
    def rows_process(self, rows=None, *objects, **kwargs):
        return 'hello world'
MyProcessor().stream_process()
```
运行
```sh
echo '111\t222' | python test.py
```
输出
```
111	222	hello world
```
