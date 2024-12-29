---
layout: post
title: Markdown测试
subtitle: 每篇文章都可以有一个副标题
categories: markdown
tags: [测试]
---

你可以在这里编写常规的[Markdown](https://markdowntutorial.com/)，Jekyll会自动将其转换为漂亮的网页。我强烈建议你[花5分钟学习如何编写Markdown](http://markdowntutorial.com/)，它将教你如何将常规文本转换为粗体/斜体/标题/表格等。

**这是一些粗体文本**

## 这是一个二级标题

这里有一个无用的表格：

| 数字 | 下一个数字 | 上一个数字 |
| :------ |:--- | :--- |
| 五 | 六 | 四 |
| 十 | 十一 | 九 |
| 七 | 八 | 六 |
| 二 | 三 | 一 |

来一张美味的可丽饼怎么样？

![可丽饼](https://s3-media3.fl.yelpcdn.com/bphoto/cQ1Yoa75m2yUFFbY2xwuqw/348s.jpg)

它也可以居中显示！

![可丽饼](https://s3-media3.fl.yelpcdn.com/bphoto/cQ1Yoa75m2yUFFbY2xwuqw/348s.jpg){: .center-block :}

这里是一个代码块：

~~~
var foo = function(x) {
  return(x + 5);
}
foo(3)
~~~

这是带有语法高亮的相同代码：

```javascript
var foo = function(x) {
  return(x + 5);
}
foo(3)
```

这是带有行号的相同代码：

{% highlight javascript linenos %}
var foo = function(x) {
  return(x + 5);
}
foo(3)
{% endhighlight %}

## 盒子
你可以像这样添加通知、警告和错误框：

### 通知

{: .box-note}
**注意：** 这是一个通知框。

### 警告

{: .box-warning}
**警告：** 这是一个警告框。

### 错误

{: .box-error}
**错误：** 这是一个错误框。

### 表情符号

这个单引号代码 `inet:email:message:to` 不会被解析为表情符号图标
:+1:.
