# 门窗业务平台项目计划 (Plan)

## 1. 任务目标
构建一套现代化的门窗业务管理系统，包含 **Web官网** (展示+后台) 和 **移动端App** (业务作业)。

## 2. 实施步骤 (Phases)

### Phase 1: 需求与原型设计 (Current)
- [x] 业务调研与分析
- [ ] App 原型设计 (Key Screens & Flows)
- [ ] Web 原型设计 (Sitemap & Wireframes)
- [ ] 生成 HTML/CSS 交互演示

### Phase 2: UI/UX 设计 (Next)
- 确定品牌色（建议：高端灰/科技蓝/环保绿）。
- 设计高保真 UI 图。

### Phase 3: 开发实施 (Future)
- 后端：建议使用 Java (SpringBlade) 或 Python (FastAPI/Django)。根据现有 User Rules，推荐 SpringBlade 架构。
- Web端：Vue 3 + Element Plus / Tailwind CSS。
- App端：Uni-app (跨平台小程序/App) 或 Flutter。

## 3. 原型交付物清单
1.  **Web 端架构图**：网站地图 (Sitemap)。
2.  **App 功能清单**：功能列表 (Feature List)。
3.  **关键页面线框图 (Wireframes)**：
    - **App**: 首页、产品详情、报价器、订单详情。
    - **Web**: 首页、案例中心、后台管理Dashboard。

## 4. 风险评估
- **算价逻辑复杂性**：门窗算价涉及公式极多（平米、延米、不足一平按一平算等），原型阶段需简化，开发阶段需重点攻克。
- **移动端适配**：量尺师现场环境复杂，App需支持离线暂存。
