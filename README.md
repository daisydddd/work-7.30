# work
初步完成了API的设计，目前还在调试
## 包含功能如下：
### 实现数据导入功能:
- 编写代码读取CSV和Excel文件,并使用pandas将数据存储到数据库。
- 处理文件格式不一致和数据不规则的情况,记录下所有的数据问题。
### 实现数据注释功能:
- 设计一个单独的数据表或集合来存储注释信息,并与主数据表建立关联。
- 编写代码允许用户添加各种类型的注释信息,如列级注释和表级注释。
### 实现数据检索功能:
- 使用SQLAlchemy构建查询构建器,允许用户指定需要查询的表、列和条件。
- 实现跨多个表的联结查询,并返回联结后的数据。
- 支持细粒度的列选择,包括通配符选择。
### 实现数据操作功能:
- 编写代码实现标准的更新和删除操作。
- 确保操作过程中妥善处理不规则和缺失数据。
