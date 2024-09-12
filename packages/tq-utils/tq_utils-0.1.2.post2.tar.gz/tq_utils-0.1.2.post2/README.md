Util list:

- ARM, Analysis Module Relationship
  
    通过 import、from-import 分析模块之间的关系.

    CodeAnalyzer 还可以一块分析每个模块导的包，所含的类、函数、全局变量
    
    缺陷：
    - 只能分析当前文件夹下的所有模块，不递归分析子文件夹（还没写）。
    - 仅支持静态分析，分析不了动态的模块导入。
    - 分析不了__init__.py中导入的包
    - 分析的前提要保障代码的格式规范（以Pycharm的自动代码规范格式为标准）
    - CodeAnalyzer只能分析单元素的赋值定义，且赋值的字面值需要缩进不能与赋值定义同缩进.
    - CodeAnalyzer暂不支持分析相对导入

 - file_manager
   
   对 open() 的封装，添加了文件名有效性判断、路径缺失创建、读时文件缺失创建，等。
   
 - graph_dot

    仅提供了有向图的创建，但重写`__str__()`能够输出 dot 格式的图信息。

 - profile_decorator

    将 pyinstrument 封装成修饰器，方便对函数进行性能分析。