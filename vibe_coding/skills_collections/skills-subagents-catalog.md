# Claude Code Subagents 目录

本文档整理自 [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) 仓库，包含所有子代理的定义和描述。

## 概览

- **总计**: 127 个子代理
- **分类**: 10 个主要类别

---

## 01. 核心开发 (Core Development)

|编号|categorie|agents|描述|
|----|----|----|----|
|1|01-core-development|api-designer|在设计新API、创建API规范或重构现有API架构以提升可扩展性和开发者体验时使用此代理。需要REST/GraphQL端点设计、OpenAPI文档、认证模式或API版本策略时调用。|
|2|01-core-development|backend-developer|在构建需要稳健架构、可扩展性规划和生产就绪实现的服务端API、微服务和后端系统时使用此代理。|
|3|01-core-development|electron-pro|在构建需要原生操作系统集成、跨平台分发、安全加固和性能优化的Electron桌面应用时使用此代理。适用于从架构设计到签名可分发安装程序的完整桌面应用开发。|
|4|01-core-development|frontend-developer|在构建需要多框架专业知识和全栈集成的React、Vue和Angular框架完整前端应用时使用。|
|5|01-core-development|fullstack-developer|在需要构建跨越数据库、API和前端层的完整功能作为统一单元时使用此代理。|
|6|01-core-development|graphql-architect|在设计或演进跨微服务的GraphQL模式、实现联邦架构或优化分布式图查询性能时使用此代理。|
|7|01-core-development|microservices-architect|在设计分布式系统架构、将单体应用分解为独立微服务或大规模建立服务间通信模式时使用。|
|8|01-core-development|mobile-developer|在构建需要原生性能优化、平台特定功能和离线优先架构的跨平台移动应用时使用此代理。适用于代码共享超过80%同时保持iOS和Android原生卓越性的React Native和Flutter项目。|
|9|01-core-development|ui-designer|在设计视觉界面、创建设计系统、构建组件库或优化面向用户的视觉效果时使用此代理，需要专业的视觉设计、交互模式和可访问性考量。|
|10|01-core-development|websocket-engineer|在实现使用WebSocket、Socket.IO或类似技术的大规模实时双向通信功能时使用此代理。|

---

## 02. 语言专家 (Language Specialists)

|编号|categorie|agents|描述|
|----|----|----|----|
|11|02-language-specialists|angular-architect|在架构具有复杂状态管理的Angular 15+企业应用、优化RxJS模式、设计微前端系统或解决大型代码库中的性能和可扩展性挑战时使用。|
|12|02-language-specialists|cpp-pro|在构建需要现代C++20/23特性、模板元编程或零开销抽象的高性能C++系统，用于系统编程、嵌入式系统或性能关键型应用时使用此代理。|
|13|02-language-specialists|csharp-developer|在构建ASP.NET Core Web API、云原生.NET解决方案或需要异步模式、依赖注入、Entity Framework优化和整洁架构的现代C#应用时使用此代理。|
|14|02-language-specialists|django-developer|在构建Django 4+ Web应用、REST API或使用异步视图和企业模式现代化现有Django项目时使用。|
|15|02-language-specialists|dotnet-core-expert|在构建需要云原生架构、高性能微服务、现代C#模式或使用最小化API和高级ASP.NET Core特性进行跨平台部署的.NET Core应用时使用。|
|16|02-language-specialists|dotnet-framework-4.8-expert|在处理需要维护、现代化或与Windows基础设施集成的传统.NET Framework 4.8企业应用时使用此代理。|
|17|02-language-specialists|elixir-expert|在需要构建利用OTP模式、GenServer架构和Phoenix框架进行实时应用的容错、并发系统时使用此代理。|
|18|02-language-specialists|flutter-expert|在构建需要自定义UI实现、复杂状态管理、原生平台集成或跨iOS/Android/Web性能优化的Flutter 3+跨平台移动应用时使用。|
|19|02-language-specialists|golang-pro|在构建需要并发编程、高性能系统、微服务或云原生架构的Go应用时使用，其中惯用模式、出色的错误处理和效率至关重要。|
|20|02-language-specialists|java-architect|在设计企业Java架构、迁移Spring Boot应用或为可扩展的云原生系统建立微服务模式时使用此代理。|
|21|02-language-specialists|javascript-pro|在需要构建、优化或重构需要ES2023+特性、异步模式或性能关键型实现的浏览器、Node.js或全栈应用的现代JavaScript代码时使用此代理。|
|22|02-language-specialists|kotlin-specialist|在构建需要高级协程模式、多平台代码共享或使用函数式编程原则进行Android/服务端开发的Kotlin应用时使用。|
|23|02-language-specialists|laravel-specialist|在构建Laravel 10+应用、设计具有复杂关系的Eloquent模型、实现异步处理队列系统或优化API性能时使用。|
|24|02-language-specialists|nextjs-developer|在构建需要App Router、服务端组件和高级性能优化的全栈开发生产级Next.js 14+应用时使用此代理。需要架构或实现完整Next.js应用、优化Core Web Vitals、实现服务端操作和变更或部署SEO优化应用时调用。|
|25|02-language-specialists|php-pro|在处理需要严格类型、现代语言特性和企业框架专业知识（Laravel或Symfony）的PHP 8.3+项目时使用此代理。用于构建可扩展应用、优化性能或需要异步/Fiber模式时。|
|26|02-language-specialists|powershell-5.1-expert|在自动化需要使用RSAT模块进行Active Directory、DNS、DHCP、GPO管理的Windows基础设施任务，或在传统.NET Framework环境中构建安全的企业级自动化工作流时使用。|
|27|02-language-specialists|powershell-7-expert|在构建跨平台云自动化脚本、Azure基础设施编排或需要PowerShell 7+与现代.NET互操作、幂等操作和企业级错误处理的CI/CD管道时使用。|
|28|02-language-specialists|python-pro|在需要为Web API、系统工具或需要现代异步模式和广泛类型覆盖的复杂应用构建类型安全、生产就绪的Python代码时使用此代理。|
|29|02-language-specialists|rails-expert|在构建或现代化需要全栈开发、Hotwire响应性、实时功能或追求最大化生产力的Rails惯用模式的Rails应用时使用。|
|30|02-language-specialists|react-specialist|在优化现有React应用性能、实现高级React 18+特性或解决React代码库中的复杂状态管理和架构挑战时使用。|
|31|02-language-specialists|rust-engineer|在构建内存安全、所有权模式、零成本抽象和性能优化至关重要的Rust系统时使用，用于系统编程、嵌入式开发、异步应用或高性能服务。|
|32|02-language-specialists|spring-boot-engineer|在构建需要微服务架构、云原生部署或响应式编程模式的企业级Spring Boot 3+应用时使用此代理。|
|33|02-language-specialists|sql-pro|在需要优化复杂SQL查询、设计高效数据库模式或解决PostgreSQL、MySQL、SQL Server和Oracle上需要高级查询优化、索引策略或数据仓库模式的性能问题时使用此代理。|
|34|02-language-specialists|swift-expert|在构建需要高级并发模式、面向协议架构和Swift特定优化的原生iOS、macOS或服务端Swift应用时使用此代理。用于SwiftUI现代化、async/await实现、基于actor的状态管理或内存安全问题。|
|35|02-language-specialists|typescript-pro|在实现需要高级类型系统模式、复杂泛型、类型级编程或跨全栈应用端到端类型安全的TypeScript代码时使用。|
|36|02-language-specialists|vue-expert|在构建需要Composition API精通、响应性优化或具有企业级性能关注的Nuxt 3开发的Vue 3应用时使用此代理。|

---

## 03. 基础设施 (Infrastructure)

|编号|categorie|agents|描述|
|----|----|----|----|
|37|03-infrastructure|azure-infra-engineer|在设计、部署或管理专注于网络架构、Entra ID集成、PowerShell自动化和Bicep IaC的Azure基础设施时使用。|
|38|03-infrastructure|cloud-architect|在需要大规模设计、评估或优化云基础设施架构时使用此代理。设计多云策略、规划云迁移、实施灾难恢复、优化云成本或确保跨云平台安全/合规时调用。|
|39|03-infrastructure|database-administrator|在优化数据库性能、实施高可用架构、设置灾难恢复或管理生产系统数据库基础设施时使用此代理。|
|40|03-infrastructure|deployment-engineer|在设计、构建或优化CI/CD管道和部署自动化策略时使用此代理。|
|41|03-infrastructure|devops-engineer|在构建或优化基础设施自动化、CI/CD管道、容器化策略和部署工作流以加速软件交付同时保持可靠性和安全性时使用此代理。|
|42|03-infrastructure|devops-incident-responder|在主动响应生产事故、诊断关键服务故障或进行事故复盘以实施永久修复和预防措施时使用。|
|43|03-infrastructure|docker-expert|在需要为生产环境构建、优化或保护Docker容器镜像和编排时使用此代理。|
|44|03-infrastructure|incident-responder|在发生主动安全漏洞、服务中断或运维事故需要立即响应、证据保全和协调恢复时使用此代理。|
|45|03-infrastructure|kubernetes-specialist|在需要设计、部署、配置或排查生产环境中的Kubernetes集群和工作负载时使用此代理。|
|46|03-infrastructure|network-engineer|在设计、优化或排查云和混合网络基础设施，或处理网络安全、性能或可靠性挑战时使用此代理。|
|47|03-infrastructure|platform-engineer|在构建或改进内部开发者平台（IDP）、设计自助服务基础设施或优化开发者工作流以减少摩擦并加速交付时使用。平台工程师代理专注于设计平台架构、实施黄金路径和最大化开发者自助服务能力。|
|48|03-infrastructure|security-engineer|在基础设施中实施综合安全解决方案、在CI/CD管道中构建自动化安全控制或建立合规和漏洞管理程序时使用此代理。用于威胁建模、零信任架构设计、安全自动化实施以及将安全左移到开发工作流中。|
|49|03-infrastructure|sre-engineer|在需要通过SLO定义、错误预算管理和自动化来建立或改进系统可靠性时使用此代理。实施SLI/SLO框架、减少运维琐事、设计容错系统、进行混沌工程或优化事故响应流程时调用。|
|50|03-infrastructure|terraform-engineer|在使用Terraform构建、重构或扩展基础设施即代码时使用，专注于多云部署、模块架构和企业级状态管理。|
|51|03-infrastructure|terragrunt-expert|精通基础设施编排、DRY配置和多环境部署的Terragrunt专家。掌握堆栈、单元、依赖管理和可扩展IaC模式，专注于代码复用、可维护性和企业级基础设施自动化。|
|52|03-infrastructure|windows-infra-admin|在管理Windows Server基础设施、Active Directory、DNS、DHCP和组策略配置时使用，特别适用于需要安全自动化和合规验证的企业级部署。|

---

## 04. 质量与安全 (Quality & Security)

|编号|categorie|agents|描述|
|----|----|----|----|
|53|04-quality-security|accessibility-tester|在需要综合可访问性测试、WCAG合规验证或辅助技术支持评估时使用此代理。|
|54|04-quality-security|ad-security-reviewer|在需要审计Active Directory安全态势、评估权限提升风险、审查身份委派模式或评估认证协议加固时使用此代理。|
|55|04-quality-security|architect-reviewer|在需要宏观评估系统设计决策、架构模式和技术选择时使用此代理。|
|56|04-quality-security|chaos-engineer|在需要设计和执行受控故障实验、在事故发生前验证系统弹性或进行演练日演习以测试团队事故响应能力时使用此代理。|
|57|04-quality-security|code-reviewer|在需要进行专注于代码质量、安全漏洞和最佳实践的综合代码审查时使用此代理。|
|58|04-quality-security|compliance-auditor|在需要实现法规合规、实施合规控制或准备GDPR、HIPAA、PCI DSS、SOC 2和ISO标准等框架的审计时使用此代理。|
|59|04-quality-security|debugger|在需要诊断和修复错误、识别故障根本原因或分析错误日志和堆栈跟踪以解决问题时使用此代理。|
|60|04-quality-security|error-detective|在需要诊断系统中错误发生原因、跨服务关联错误、识别根本原因并防止未来故障时使用此代理。|
|61|04-quality-security|penetration-tester|在需要进行授权安全渗透测试以通过主动利用和验证识别真实漏洞时使用此代理。用于攻击性安全测试、漏洞利用和动手风险演示。|
|62|04-quality-security|performance-engineer|在需要识别和消除应用、数据库或基础设施系统中的性能瓶颈，以及基线性能指标需要改进时使用此代理。|
|63|04-quality-security|powershell-security-hardening|在需要加固PowerShell自动化、保护远程配置安全、实施最小权限设计或使脚本符合企业安全基线和合规框架时使用此代理。|
|64|04-quality-security|qa-expert|在需要综合质量保证策略、整个开发周期的测试规划或质量指标分析以改进整体软件质量时使用此代理。|
|65|04-quality-security|security-auditor|在进行跨系统、基础设施和流程的综合安全审计、合规评估或风险评估时使用此代理。需要系统漏洞分析、合规差距识别或基于证据的安全发现时调用。|
|66|04-quality-security|test-automator|在需要构建、实施或增强自动化测试框架、创建测试脚本或将测试集成到CI/CD管道中时使用此代理。|

---

## 05. 数据与AI (Data & AI)

|编号|categorie|agents|描述|
|----|----|----|----|
|67|05-data-ai|ai-engineer|在架构、实施或优化端到端AI系统时使用此代理——从模型选择和训练管道到生产部署和监控。|
|68|05-data-ai|data-analyst|在需要从业务数据中提取洞察、创建仪表板和报告或进行统计分析以支持决策时使用。|
|69|05-data-ai|database-optimizer|在需要分析慢查询、跨多个系统优化数据库性能或实施索引策略以改进查询执行时使用此代理。|
|70|05-data-ai|data-engineer|在需要设计、构建或优化数据管道、ETL/ELT流程和数据基础设施时使用此代理。设计数据平台、实施管道编排、处理数据质量问题或优化数据处理成本时调用。|
|71|05-data-ai|data-scientist|在需要分析数据模式、构建预测模型或从数据集中提取统计洞察时使用此代理。用于探索性分析、假设检验、机器学习模型开发以及将发现转化为业务建议。|
|72|05-data-ai|llm-architect|在设计生产级LLM系统、实施微调或RAG架构、优化推理服务基础设施或管理多模型部署时使用。|
|73|05-data-ai|machine-learning-engineer|在需要在生产环境中大规模部署、优化或服务机器学习模型时使用此代理。|
|74|05-data-ai|ml-engineer|在构建需要模型训练管道、模型服务基础设施、性能优化和自动化重训练的生产ML系统时使用此代理。|
|75|05-data-ai|mlops-engineer|在需要设计和实施ML基础设施、为机器学习模型设置CI/CD、建立模型版本系统或优化ML平台的可靠性和自动化时使用此代理。用于构建生产级实验跟踪、实施自动化训练管道、配置GPU资源编排以及建立ML系统的运维监控。|
|76|05-data-ai|nlp-engineer|在构建生产NLP系统、实施文本处理管道、开发语言模型或解决命名实体识别、情感分析或机器翻译等特定领域NLP任务时使用。|
|77|05-data-ai|postgres-pro|在需要优化PostgreSQL性能、设计高可用复制或大规模排查数据库问题时使用。查询优化、配置调优、复制设置、备份策略以及掌握企业部署的高级PostgreSQL特性时调用此代理。|
|78|05-data-ai|prompt-engineer|在需要为生产系统中的大型语言模型设计、优化、测试或评估提示词时使用此代理。|

---

## 06. 开发者体验 (Developer Experience)

|编号|categorie|agents|描述|
|----|----|----|----|
|79|06-developer-experience|build-engineer|在需要优化构建性能、减少编译时间或跨成长团队扩展构建系统时使用此代理。|
|80|06-developer-experience|cli-developer|在构建需要直观命令设计、跨平台兼容性和优化开发者体验的命令行工具和终端应用时使用此代理。|
|81|06-developer-experience|dependency-manager|在需要审计依赖漏洞、解决版本冲突、优化包大小或实施自动化依赖更新时使用此代理。|
|82|06-developer-experience|documentation-engineer|在需要创建、架构或全面改造包括API文档、教程、指南和与代码变化同步的开发者友好内容的综合文档系统时使用此代理。|
|83|06-developer-experience|dx-optimizer|在优化包括构建时间、反馈循环、测试效率和开发者满意度指标的整个开发环境的完整开发者工作流时使用此代理。|
|84|06-developer-experience|git-workflow-manager|在需要为项目或团队设计、建立或优化Git工作流、分支策略和合并管理时使用此代理。|
|85|06-developer-experience|legacy-modernizer|在现代化需要增量迁移策略、技术债务减少和风险缓解同时保持业务连续性的遗留系统时使用此代理。|
|86|06-developer-experience|mcp-developer|在需要构建、调试或优化将AI系统连接到外部工具和数据源的模型上下文协议（MCP）服务器和客户端时使用此代理。|
|87|06-developer-experience|powershell-module-architect|在架构和重构PowerShell模块、设计配置文件系统或创建跨版本兼容的自动化库时使用此代理。用于模块设计审查、配置优化、打包可复用代码和跨团队标准化函数结构。|
|88|06-developer-experience|powershell-ui-architect|在设计或构建需要UI和业务逻辑清晰分离的PowerShell自动化工具桌面图形界面（WinForms、WPF、Metro风格仪表板）或终端用户界面（TUI）时使用。|
|89|06-developer-experience|refactoring-specialist|在需要将结构不良、复杂或重复的代码转换为干净、可维护的系统同时保留所有现有行为时使用。|
|90|06-developer-experience|slack-expert|在开发Slack应用、实施Slack API集成或审查Slack机器人代码的安全性和最佳实践时使用此代理。|
|91|06-developer-experience|tooling-engineer|在需要构建或增强开发者工具（包括CLI、代码生成器、构建工具和IDE扩展）时使用此代理。|

---

## 07. 专业领域 (Specialized Domains)

|编号|categorie|agents|描述|
|----|----|----|----|
|92|07-specialized-domains|api-documenter|在创建或改进API文档、编写OpenAPI规范、构建交互式文档门户或为API生成代码示例时使用此代理。|
|93|07-specialized-domains|blockchain-developer|在构建需要Solidity、Gas优化、安全审计和Web3集成专业知识的智能合约、DApp和区块链协议时使用此代理。|
|94|07-specialized-domains|embedded-systems|在为资源受限的微控制器开发固件、实施基于RTOS的应用或优化硬件约束、延迟保证和可靠性至关重要的实时系统时使用。|
|95|07-specialized-domains|fintech-engineer|在构建支付系统、金融集成或需要安全交易处理、法规遵从和高交易准确性的合规密集型金融应用时使用。|
|96|07-specialized-domains|game-developer|在实现游戏系统、优化图形渲染、构建多人网络或开发针对特定平台的游戏的游戏玩法机制时使用此代理。|
|97|07-specialized-domains|iot-engineer|在设计和部署需要设备管理、边缘计算、云集成专业知识的IoT解决方案时使用，用于处理大规模设备、复杂连接场景或实时数据管道等挑战。|
|98|07-specialized-domains|m365-admin|在自动化Microsoft 365管理任务时使用，包括Exchange Online邮箱配置、Teams协作管理、SharePoint站点配置、许可证生命周期管理和Graph API驱动的身份自动化。|
|99|07-specialized-domains|mobile-app-developer|在开发专注于原生或跨平台实现、性能优化和平台特定用户体验的iOS和Android移动应用时使用此代理。|
|100|07-specialized-domains|payment-integration|在实施需要PCI合规、欺诈防护和安全交易处理的支付系统、集成支付网关或处理金融交易时使用此代理。|
|101|07-specialized-domains|quant-analyst|在需要开发量化交易策略、构建具有严格数学基础的金融模型或进行衍生品和投资组合的高级风险分析时使用此代理。用于统计套利策略开发、历史验证回测、衍生品定价模型和投资组合风险评估。|
|102|07-specialized-domains|risk-manager|在需要识别、量化和管理跨金融、运营、监管和战略领域的企业级风险时使用此代理。需要评估风险敞口、设计控制框架、验证风险模型或确保监管合规时调用。|
|103|07-specialized-domains|seo-specialist|在需要涵盖技术审计、关键词策略、内容优化和搜索排名改进的综合SEO优化时使用此代理。|

---

## 08. 业务与产品 (Business & Product)

|编号|categorie|agents|描述|
|----|----|----|----|
|104|08-business-product|business-analyst|在分析业务流程、从利益相关者收集需求或识别流程改进机会以推动运营效率和可衡量的业务价值时使用。|
|105|08-business-product|content-marketer|在需要制定综合内容策略、创建SEO优化的营销内容或执行多渠道内容活动以推动参与和转化时使用此代理。用于内容规划、内容创作、受众分析和衡量内容ROI。|
|106|08-business-product|customer-success-manager|在需要评估客户健康状况、制定留存策略、识别增购机会或最大化客户生命周期价值时使用此代理。用于账户健康分析、流失预防、产品采用优化和客户成功规划。|
|107|08-business-product|legal-advisor|在需要起草合同、审查合规要求、制定IP保护策略或评估科技企业的法律风险时使用此代理。|
|108|08-business-product|product-manager|在需要根据用户需求和业务目标做出产品战略决策、确定功能优先级或定义路线图计划时使用此代理。|
|109|08-business-product|project-manager|在需要建立项目计划、跟踪执行进度、管理风险、控制预算/进度和协调跨复杂项目的利益相关者时使用此代理。|
|110|08-business-product|sales-engineer|在需要进行技术售前活动时使用此代理，包括解决方案架构、概念验证开发和技术演示以支持复杂销售交易。|
|111|08-business-product|scrum-master|在团队需要引导、流程优化、速度改进或敏捷仪式管理时使用——特别是用于Sprint计划、回顾、障碍移除和跨多团队扩展敏捷实践。|
|112|08-business-product|technical-writer|在需要创建、改进或维护技术文档时使用此代理，包括API参考、用户指南、SDK文档和入门指南。|
|113|08-business-product|ux-researcher|在需要进行用户研究、分析用户行为或生成可操作洞察以验证设计决策和发现用户需求时使用此代理。需要可用性测试、用户访谈、问卷设计、分析解读、人物画像开发或竞争研究以指导产品策略时调用。|
|114|08-business-product|wordpress-master|在需要架构、优化或排查从自定义主题/插件开发到企业级多站点平台的WordPress实现时使用此代理。用于性能优化、安全加固、无头WordPress API、WooCommerce解决方案和扩展WordPress以处理数百万访问者。|

---

## 09. 元编排 (Meta & Orchestration)

|编号|categorie|agents|描述|
|----|----|----|----|
|115|09-meta-orchestration|agent-installer|在用户想要发现、浏览或从awesome-claude-code-subagents仓库安装Claude Code代理时使用此代理。|
|116|09-meta-orchestration|agent-organizer|在组装和优化多代理团队以执行需要仔细任务分解、代理能力匹配和工作流协调的复杂项目时使用。|
|117|09-meta-orchestration|context-manager|在多个代理需要协调访问上下文和元数据时，用于管理共享状态、信息检索和数据同步。|
|118|09-meta-orchestration|error-coordinator|在分布式系统错误发生且需要跨多个组件协调处理，或需要实施具有自动故障检测和级联预防的综合错误恢复策略时使用此代理。|
|119|09-meta-orchestration|it-ops-orchestrator|在编排跨多个领域（PowerShell自动化、.NET开发、基础设施管理、Azure、M365）的复杂IT运维任务时使用，通过智能路由将工作分配给专业代理。|
|120|09-meta-orchestration|knowledge-synthesizer|在需要从代理交互中提取可操作模式、综合跨多个工作流的洞察并从集体经验中实现组织学习时使用。|
|121|09-meta-orchestration|multi-agent-coordinator|在协调需要跨系统通信、共享状态、同步工作和处理分布式故障的多个并发代理时使用。|
|122|09-meta-orchestration|performance-monitor|在建立可观测性基础设施以跟踪系统指标、检测性能异常和优化跨多代理环境的资源使用时使用。|
|123|09-meta-orchestration|task-distributor|在跨多个代理或工作者分配任务、管理队列和平衡工作负载以在尊重优先级和截止时间的同时最大化吞吐量时使用。|
|124|09-meta-orchestration|workflow-orchestrator|在需要设计、实施或优化具有多状态、错误处理和事务管理的复杂业务流程工作流时使用此代理。|

---

## 10. 研究与分析 (Research & Analysis)

|编号|categorie|agents|描述|
|----|----|----|----|
|125|10-research-analysis|competitive-analyst|在需要分析直接和间接竞争对手、对标市场领导者或制定加强竞争定位和市场优势的策略时使用。|
|126|10-research-analysis|data-researcher|在需要从多个来源发现、收集和验证数据以支持分析和决策时使用此代理。用于识别数据源、收集原始数据集、执行质量检查和为下游分析或建模准备数据。|
|127|10-research-analysis|market-researcher|在需要分析市场、了解消费者行为、评估竞争格局和估算机会规模以指导业务战略和市场进入决策时使用此代理。|
|128|10-research-analysis|research-analyst|在需要跨多个来源进行综合研究并将发现综合为可操作洞察、趋势识别和详细报告时使用此代理。|
|129|10-research-analysis|scientific-literature-researcher|在需要搜索科学文献并从已发表研究中检索结构化实验数据时使用。当任务需要来自全文研究论文的基于证据的答案，包括方法、结果、样本量和质量评分时调用此代理。|
|130|10-research-analysis|search-specialist|在需要使用高级搜索策略、查询优化和定向信息检索跨多个来源查找特定信息时使用。当优先级是高效定位精确、相关结果而非分析或综合内容时调用此代理。|
|131|10-research-analysis|trend-analyst|在分析新兴模式、预测行业转变或开发未来场景以指导战略规划和竞争定位时使用。|

---

## 分类统计

| 分类 | 代理数量 |
|------|----------|
| 01. 核心开发 | 10 |
| 02. 语言专家 | 26 |
| 03. 基础设施 | 16 |
| 04. 质量与安全 | 14 |
| 05. 数据与AI | 12 |
| 06. 开发者体验 | 13 |
| 07. 专业领域 | 12 |
| 08. 业务与产品 | 11 |
| 09. 元编排 | 10 |
| 10. 研究与分析 | 7 |
| **总计** | **131** |

---

> 数据来源: [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
