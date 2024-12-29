# Walden 博客

Walden 是一个基于 Jekyll YAT 主题构建的个人博客，专注于分享技术见解和生活感悟。博客采用简洁优雅的设计，提供丰富的功能来提升阅读和写作体验。

进行了一些自定义的修改使网站更加美观

## 主要功能

- **响应式设计**：完美适配各种设备，提供流畅的阅读体验
- **夜间模式**：保护眼睛，适合夜间阅读
- **文章分类**：按类别组织文章，方便查找
- **标签系统**：通过标签快速定位相关内容
- **代码高亮**：使用 highlight.js 提供美观的代码展示
- **数学公式支持**：支持 LaTeX 数学公式渲染
- **图片画廊**：使用 PhotoSwipe 5 实现优雅的图片展示
- **SEO 优化**：内置 SEO 优化，提高搜索引擎可见度
- **多语言支持**：支持中英文切换
- **评论系统**：集成 Utterances 评论功能

## 技术栈

- **Jekyll**：静态网站生成器
- **YAT 主题**：现代响应式主题
- **GitHub Pages**：托管平台
- **Jekyll Spaceship**：提供丰富的扩展功能

## 本地开发

1. 克隆仓库
   ```bash
   git clone https://github.com/ronema/walden.git
   ```
2. 安装依赖
   ```bash
   bundle install
   ```
3. 启动开发服务器
   ```bash
   bundle exec jekyll serve
   ```
4. 访问 http://localhost:4000 查看效果

## 部署

博客通过 GitHub Pages 自动部署。每次将更改推送到 `main` 分支时，GitHub Actions 会自动构建并部署网站。

## 许可证

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT)。
