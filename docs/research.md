# Research register and framework scope

Research session date: **2026-11-15 America/Edmonton** (retrieval host date **2026-11-16 UTC**). This register distinguishes source verification from validation of the application. An initial shell-network attempt failed to retrieve NIST content; subsequent read-only web and GitHub connectors successfully retrieved the primary sources described below. We checked selected publication sections, public metadata, and repository introductions, rather than performing exhaustive framework or software audits. Do not treat the project as an implementation of every requirement in any source.

## Selected authoritative sources

| Source and reference URL | Status and use in this project | Verification limit |
| --- | --- | --- |
| [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework), [AI RMF 1.0 publication](https://doi.org/10.6028/NIST.AI.100-1) | Voluntary risk management framework. Its GOVERN, MAP, MEASURE, and MANAGE functions provide a useful organizing vocabulary for context, ownership, evaluation, and treatment. | Verified NIST AI 100-1, January 2023: executive summary and §5 (printed p.20) confirm voluntary scope and these four functions. This verifies function names and edition, not a complete subcategory assessment or every local mapping. |
| [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework), [CSF 2.0 publication](https://doi.org/10.6028/NIST.CSWP.29) | Voluntary cybersecurity outcome framework. GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, and RECOVER help place AI concerns within organizational cybersecurity responsibilities. | Verified NIST CSWP 29, February 26, 2024: title, abstract, and §2 (printed pp.3–4) confirm edition, outcome-oriented scope, and six functions. Detailed CSF subcategory mappings remain deferred. |
| [MITRE ATLAS](https://atlas.mitre.org/) | Knowledge base of adversarial tactics and techniques affecting AI systems. Useful for future structured attack paths and references to documented adversarial behavior. | Official atlas-data README introduction verified during this session: ATLAS is a public knowledge base of adversary TTPs targeting AI systems, and the repository identifies its YAML files as the authoritative data source. Individual technique identifiers and entries were not reviewed. The MVP should avoid claiming precise ATLAS coverage. An ATLAS technique's existence is not evidence that a particular deployment is vulnerable. |
| [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) | Industry security guidance. Verified 2025 references are LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM06 Excessive Agency, and LLM09 Misinformation. These are conceptual pointers for selected rules. | Edition confirmed from the official repository preface and all four identifiers/headings confirmed from source-file introductions during this session. This verifies reference labels and relevant concepts, not the correctness of every local rule mapping or all suggested safeguards. A triggered rule does not establish exploitation or an OWASP compliance result. |
| [OWASP GenAI Security Project](https://genai.owasp.org/) | Primary project location for LLM and agentic security guidance. Review agentic guidance before Phase 4 to inform permissions, tool boundaries, and human authorization. | Official resource page confirms OWASP Top 10 for Agentic Applications for 2026, dated December 9, 2025. Publication metadata and purpose reviewed; individual agentic identifiers, controls, and scenarios not yet reviewed. The MVP does not implement this guidance. |
| [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) | International AI management system standard with requirements; certification is distinct from this project. Useful organizational themes include accountable management, lifecycle processes, and continual improvement. | Official public product page verified: Edition 1, December 2023, describes organizational AI management system requirements. No full standard text retrieved or purchased. No clause-level interpretation, ISO mapping, conformity determination, or certification claim is supported. |
| [NIST AI RMF Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1) | Voluntary companion guidance relevant to generative AI evaluation and risk management. Candidate later source for evaluation design and evidence requirements. | Not retrieved; detailed incorporation deferred. |

A voluntary framework or standard can become relevant through contracts or an applicable regulatory regime. This tool does not decide that applicability. Binding law depends on jurisdiction, organization, data, and use case; no legal requirements have been researched or encoded in this MVP. Project-authored review priorities, evidence requests, and deployment questions are **our proposed practices**, not requirements quoted from the sources above.

## Existing open-source projects to evaluate

Official README introductions were retrieved and reviewed during this session. These are bounded capability checks, not completed code, license, or maintenance audits. No repositories were cloned, modified, or tested in this research task.

| Project | Relevant capability | Implication for project selection |
| --- | --- | --- |
| [NVIDIA garak](https://github.com/NVIDIA/garak) | LLM vulnerability probing and evaluation. | An adversarial testing harness would overlap existing work and require models, execution controls, and evaluation infrastructure. Later integrate selected safe results as evidence rather than rebuild a probe library. |
| [Microsoft PyRIT](https://github.com/microsoft/PyRIT) | CLI, GUI, and Python framework for scans, adaptive multi-turn attacks, and human-led AI red teaming. The old Azure repository README points to this Microsoft repository. | Useful later for controlled adversarial exercises. The initial assessment CLI addresses organizational context and evidence tracking before automated testing. |
| [AI Verify](https://github.com/aiverify-foundation/aiverify) | AI testing and assessment tooling. | Inspect schemas, test coverage, licensing, and interoperability before expanding into a broader governance platform. The lightweight CLI's educational reason is transparent rules and a small codebase; it should not claim unique assessment functionality. |

Full licenses, dependency requirements, release status, and exact tested functional coverage still require deeper review before reuse or dependency selection. README claims are not independently tested capabilities. The MVP does not import their code or datasets.

## Why selective mappings

The smallest credible demonstration connects explicit deployment facts to inspectable rules, plausible risk scenarios, safeguards, evidence gaps, and named human decisions. It does not need exhaustive framework coverage. A framework reference supplies context, not proof that a safeguard works. Declared safeguards must remain distinct from verified evidence, and generated scenarios must remain distinct from observed incidents.

The next source-verification task should inspect the remaining linked primary publications, record edition and retrieval date, and review every local rule mapping and safeguard against the relevant source. NIST function names, selected OWASP 2025 reference labels, and publication metadata have now been checked as recorded below; local mapping accuracy and source edition maintenance still require review. Subsequent work should add reviewed attack paths and evaluation baselines before introducing agentic research or execution.

## Primary-source checks completed in this session

Access method: read-only GitHub connector, default `main` branches. The following files were retrieved successfully; the blob identifiers identify the returned file revisions. Only the preface and the first 22 lines of each vulnerability file were reviewed, so this is a bounded source check rather than a full guidance review. No source dataset was imported or copied into the application.

| Official OWASP source file | Returned blob SHA | Verified observation |
| --- | --- | --- |
| [2025 preface](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications/blob/main/2_0_vulns/LLM00_Preface.md) | `447854cdb659b76fb63ee6404025adfad255b480` | Identifies this as the 2025 version and discusses increased agency and unchecked permissions. |
| [LLM01](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications/blob/main/2_0_vulns/LLM01_PromptInjection.md) | `a218f465777fc3eded4b250e363105c6178de4a7` | Heading is LLM01:2025 Prompt Injection. Description distinguishes direct user input from indirect external sources such as files and websites. |
| [LLM02](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications/blob/main/2_0_vulns/LLM02_SensitiveInformationDisclosure.md) | `359ad61caf40164ee7a4f3db16cc7b8c7091e0a1` | Heading is LLM02:2025 Sensitive Information Disclosure. Description covers sensitive data exposure through outputs and notes limits of system-prompt restrictions. |
| [LLM06](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications/blob/main/2_0_vulns/LLM06_ExcessiveAgency.md) | `09cdf0d0bab1b3734ffb3c6bd15d89fa5eca5925` | Heading is LLM06:2025 Excessive Agency. Intro identifies excessive functionality, permissions, and autonomy as typical causes. |
| [LLM09](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications/blob/main/2_0_vulns/LLM09_Misinformation.md) | `9c0c882323e93184d228954a7d912da933cda32f` | Heading is LLM09:2025 Misinformation. Intro covers plausible false outputs and overreliance without verification. |

[MITRE ATLAS Data README](https://github.com/mitre-atlas/atlas-data/blob/main/README.md), returned blob `1954b85ce79344909801147edc25eeca4fec266b`, lines 1–60 reviewed. It describes the public knowledge base, identifies repository YAML as authoritative, and explains distributed data and tooling. No particular attack technique, release version, or case study was checked.

These verified concepts support the choice to inspect untrusted-input boundaries, data exposure, tool authority, and human reliance in a deployment assessment. They do not establish that any synthetic scenario is exploitable, that its priority is empirically calibrated, or that the project complies with a standard.

### NIST and ISO verification scope

Read-only web connector retrieved these official sources on host date 2026-11-16 UTC / session date 2026-11-15 America/Edmonton:

- [NIST AI 100-1 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf): title/front matter, executive-summary passages on voluntary use, and §5, printed p.20. Verified January 2023 AI RMF 1.0 and its four functions. Governance spans the other functions; the framework is not a sequential checklist. We did not review all categories and subcategories or validate each engine reference.
- [NIST CSWP 29 PDF](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf): title, abstract, and §2, printed pp.3–4. Verified February 26, 2024 CSF 2.0 and its six functions. CSF describes cybersecurity outcomes and does not prescribe a universal implementation. An older NIST five-functions URL redirected to a CSF 1.1 page; that older page was not used to substantiate CSF 2.0.
- [ISO/IEC 42001 public metadata](https://www.iso.org/standard/42001): checked title, edition/date, and public description of the AI management system scope. The original standard/81230.html link redirects here. Only public metadata was inspected; the paid standard was not acquired.

### OWASP edition maintenance and agentic guidance

The [official Agentic Applications 2026 resource page](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) identifies a publication date of December 9, 2025 and describes guidance for autonomous agent workflows. We reviewed metadata and purpose only, not the downloadable guidance or item-level identifiers. This is voluntary industry guidance, not binding law or certification.

The [official LLM Top 10 2026 resource page](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) is dated August 3, 2026 and advertises a newer edition. **The MVP is explicitly pinned to the verified 2025 references; 2025 must not be described as the latest edition.** Before migration, review the 2026 publication, compare identifiers and substantive changes, update rules and documentation together, and rerun evaluation baselines. This session verified the newer edition's existence, not its detailed content or compatibility with our rules.

### Existing-tool README retrieval record

Read-only GitHub connector reviewed default-branch README introductions, up to the first 65 lines (60 for the Microsoft PyRIT destination). Returned blob identifiers:

| Official source | Returned README blob SHA | Observed scope |
| --- | --- | --- |
| [NVIDIA garak](https://github.com/NVIDIA/garak/blob/main/README.md) | `29d7e4f4c740f1252c64b1b15045abfc7bd71051` | Describes static, dynamic, and adaptive vulnerability probes for LLM applications, including leakage and prompt injection. Lists model/API integration options and a CLI. |
| [Azure PyRIT relocation notice](https://github.com/Azure/PyRIT/blob/main/README.md) | `dd941a879bfdd049a3f310efcd848e4637489bf1` | Directs users to microsoft/PyRIT. |
| [Microsoft PyRIT](https://github.com/microsoft/PyRIT/blob/main/README.md) | `3773e4a423879eceb01e4836256e7e7b8d3fbae2` | Describes automated scans, adaptive multi-turn and human-led testing, plus CLI, GUI, and Python interfaces. |
| [AI Verify](https://github.com/aiverify-foundation/aiverify/blob/main/README.md) | `bf99021e3cb6b97a74a517552cad6282b122f632` | Describes modular testing tools and governance assessment, including supervised classification/regression on tabular/image data. Explicitly disclaims a guarantee of safety or freedom from bias. |

The project-selection inference is therefore narrower than a novelty claim: existing tools already provide substantial adversarial testing or model evaluation. Our small assessment CLI prioritizes deployment context, traceable proposed risks, evidence gaps, and human decisions as an understandable foundation. Later work should ingest appropriate results from established tools rather than rebuild their testing engines.
