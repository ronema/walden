---
layout: post
title: 欢迎使用Jekyll！
subtitle: 一个强大的静态网站生成器。
author: Jeffrey
categories: jekyll
banner:
  video: https://vjs.zencdn.net/v/oceans.mp4
  loop: true
  volume: 0.8
  start_at: 8.5
  image: https://bit.ly/3xTmdUP
  opacity: 0.618
  background: "#000"
  height: "100vh"
  min_height: "38vh"
  heading_style: "font-size: 4.25em; font-weight: bold; text-decoration: underline"
  subheading_style: "color: gold"
tags: jekyll theme yat
top: 1
sidebar: []
---

你可以在`_posts`目录中找到这篇文章。继续编辑它并重新构建网站以查看更改。你可以通过多种方式重新构建网站，但最常见的方法是运行`jekyll serve`，它会启动一个Web服务器并在文件更新时自动重新生成你的网站。

要添加新文章，只需在`_posts`目录中添加一个遵循`YYYY-MM-DD-文章名称.ext`格式的文件，并包含必要的前置信息。查看这篇文章的源代码以了解其工作原理。

## 第一部分

Jekyll还提供了强大的代码片段支持：

{% highlight ruby %}
def print_hi(name)
puts "Hi, #{name}"
end
print_hi('Tom')
#=> 打印 'Hi, Tom' 到 STDOUT。
{% endhighlight %}

## 第二部分

查看[Jekyll文档][jekyll-docs]以获取有关如何充分利用Jekyll的更多信息。请在[Jekyll的GitHub仓库][jekyll-gh]中提交所有错误/功能请求。如果你有任何问题，可以在[Jekyll Talk][jekyll-talk]上提问。

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]: https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/

$ a \* b = c ^ b $

$ 2^{\frac{n-1}{3}} $

$ \int_a^b f(x)\,dx. $

```cpp
#include <iostream>
using namespace std;

int main() {
  cout << "Hello World!";
  return 0;
}
// 打印 'Hi, Tom' 到 STDOUT。
```

```python
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("John", 36)

print(p1.name)
print(p1.age)
