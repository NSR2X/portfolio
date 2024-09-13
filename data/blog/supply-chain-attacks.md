title: France’s Wave of Undisclosed Data Breaches
date: 2024-09-18
description: As of 2024, supply chain attacks have become increasingly pervasive and underestimated cybersecurity threats. High-profile incidents like SolarWinds have highlighted vulnerabilities, but many organizations still fail to grasp the full scope, especially with the rise of SaaS and AI technologies. The attack surface has expanded due to interconnected cloud services and AI integration, introducing new vulnerabilities. Human factors and social engineering amplify risks. Organizations face challenges in visibility, control, and resource constraints. To build resilience, they must implement robust third-party risk management, adopt zero trust architectures, leverage AI for threat detection, and enhance collaboration between government and industry. Only through a holistic approach can organizations navigate the evolving threat landscape and secure their supply chains.
image: /static/supply-chain-attacks.jpg
---

# Supply Chain Attacks: How AI and SaaS Are Changing the Game in 2024

As we navigate through 2024, supply chain attacks have emerged as one of the most pervasive and underestimated cybersecurity threats facing organizations globally. High-profile incidents like SolarWinds and Kaseya have shed light on the vulnerabilities inherent in our interconnected systems. Yet, many companies still fail to grasp the true scope and potential impact of these attacks, leaving critical vulnerabilities exposed and hindering efforts to build robust defenses. The rise of Software-as-a-Service (SaaS) and Managed Security Service (MSS) providers, coupled with advancements in Artificial Intelligence (AI), has further complicated the landscape, introducing both new challenges and opportunities.

## The Expanding Attack Surface

One of the key misconceptions about supply chain attacks is that they target only prominent software vendors and IT service providers. In reality, the potential attack surface is much broader, encompassing hardware manufacturers, open-source projects, cloud services, and even seemingly peripheral third-party relationships.

> "The interconnections within supply chains introduce a layer of complexity, raising the probability of undiscovered vulnerabilities that attackers can exploit," explains Neeraj Singh, senior security researcher at WithSecure.

This complexity creates blind spots where threats can lurk undetected. For instance, the 2021 attack on Codecov, a code coverage tool, allowed attackers to exfiltrate sensitive data from thousands of companies by compromising a single component in many organizations' development pipelines. Similarly, the MOVEit Transfer vulnerability impacted over 1,000 organizations across various sectors, highlighting how a flaw in a widely used file transfer utility can have cascading effects.

Even hardware supply chains are not immune. Theo Zafirakos, CISO at Fortra, warns:

> "At any point in a supply chain where there is a connection between devices or networks, one can find the opportunity to exploit a device that connects to the network to plant malware."

This includes everything from servers and desktops to HVAC systems and network-connected security cameras.

## The Rise of SaaS and MSS Providers

The proliferation of SaaS applications and MSS providers has significantly influenced supply chain security. Organizations now rely on a complex web of interconnected cloud services, each representing a potential entry point for malicious actors. This interconnectedness means that a vulnerability in one SaaS application can potentially compromise an entire network of connected services and downstream customers.

### Expanded Attack Surface

The adoption of multiple SaaS solutions has led to what some experts call a "SaaS application mesh," creating a complex environment that is challenging to secure and monitor effectively. This complexity can obscure potential vulnerabilities and make it difficult for security teams to maintain visibility across the entire supply chain.

> SaaS applications have become an attractive target for cybercriminals, with some experts considering them the "Achilles' heel" for supply chain attacks.

### New Attack Vectors

As SaaS providers increasingly incorporate AI and machine learning into their offerings, a new dimension of supply chain risk has emerged. The AI supply chain, including the data and models used to train these systems, is becoming a central concern for cybersecurity professionals. This introduces new potential vulnerabilities that organizations must consider when assessing their overall security posture.

## The Ripple Effect

Another critical aspect that is often underestimated is the potential ripple effect of supply chain compromises. When an attacker gains a foothold in one part of the supply chain, they can leverage that access to move laterally and compromise multiple downstream targets.

Greg Notch, CISO at Expel, notes:

> "The problem is that there is a hidden tax on these moves that is now coming due in the form of unaddressed supply chain risk that they can't get off their balance sheets."

This interconnectedness means that even organizations with strong internal security practices can be vulnerable through their suppliers and partners.

### The Impact of Attacks

The consequences of these attacks can be severe and long-lasting. According to IBM's **Cost of a Data Breach Report 2023**, the average cost of a software supply chain compromise was **$4.63 million**, 8.3% higher than the average cost of other types of data breaches. Moreover, identifying and containing supply chain compromises required an average of **294 days**, nearly 9% longer than other breaches.

Beyond immediate financial losses, supply chain attacks can lead to:

- **Operational disruptions** and production delays
- **Reputational damage** and loss of customer trust
- **Regulatory fines** and legal liabilities
- **Intellectual property theft** and competitive disadvantage
- **Long-term security implications** from persistent backdoors

## The Human Element

While much attention is focused on technical vulnerabilities, the human element of supply chain attacks is often overlooked. Social engineering tactics targeting employees, contractors, and even customers can be just as effective as exploiting code flaws.

Zafirakos cautions:

> "When someone we deal with on a regular basis gets compromised and their email account is taken over by a cybercriminal, it's easy to be fooled and follow any instructions they send us because they originate from someone we know."

This type of attack can be particularly difficult to detect and prevent, as it exploits established trust relationships.

### AI-Enhanced Social Engineering

The rise of AI and machine learning introduces new vectors for social engineering at scale. Deepfake technology and advanced language models make it increasingly feasible to automate highly convincing phishing campaigns and business email compromise (BEC) attacks targeting an organization's supply chain.

## Challenges in Mitigation

The expansive and complex nature of modern supply chains creates significant challenges for security teams trying to mitigate these risks. Some key obstacles include:

- **Visibility**: Many organizations lack a comprehensive view of their entire supply chain ecosystem, including nth-party suppliers and open-source dependencies.
- **Control**: Companies have limited ability to directly influence the security practices of their suppliers and partners.
- **Complexity**: The sheer number of potential attack vectors and interconnections makes it difficult to identify and prioritize risks.
- **Resource Constraints**: Thoroughly vetting and monitoring every supplier and component is often infeasible, especially for smaller organizations.
- **Regulatory Landscape**: Evolving compliance requirements around supply chain security add another layer of complexity for multinational companies.

## Building a Resilient Defense

Despite these challenges, there are steps organizations can take to improve their resilience against supply chain attacks:

1. **Implement Robust Third-Party Risk Management**: Conduct regular security assessments of key suppliers, including their own supply chain practices.
2. **Adopt a Zero Trust Architecture**: Assume compromise and limit lateral movement within networks.
3. **Invest in Comprehensive Vulnerability Management**: Cover both internal systems and third-party components.
4. **Develop and Test Incident Response Plans**: Account for supply chain compromise scenarios.
5. **Enhance Security Awareness Training**: Focus on recognizing social engineering tactics.
6. **Maintain Accurate Software Bills of Materials (SBOMs)**: Use Software Composition Analysis (SCA) to track dependencies.
7. **Leverage AI and Automation**: Utilize for continuous monitoring and anomaly detection across the supply chain.
8. **Participate in Information Sharing Initiatives**: Stay ahead of emerging threats within your industry.
9. **Consider Cyber Insurance**: Incorporate as part of a holistic risk management strategy.

## AI's Role in Supply Chain Risk Management

AI can significantly impact SaaS supply chain risk management in several key ways:

### Enhanced Threat Detection and Prediction

AI can analyze vast amounts of data to identify potential threats and vulnerabilities in the SaaS supply chain more quickly and accurately than traditional methods. Machine learning algorithms can detect subtle patterns and anomalies that may indicate emerging risks or attacks.

### Automated Risk Assessment and Scoring

AI-powered systems can continuously evaluate and score the risk levels of different SaaS vendors and components in real-time. This allows organizations to prioritize their risk mitigation efforts and make more informed decisions about which SaaS solutions to use.

### Improved Visibility and Monitoring

AI provides deeper visibility into the complex web of SaaS applications and their interconnections within an organization's ecosystem. This enhanced monitoring capability helps identify potential weak points and unauthorized access attempts across the supply chain.

### Predictive Analytics for Supplier Performance

Machine learning models can analyze historical data and external factors to forecast potential issues with SaaS suppliers, such as service disruptions or quality problems. This allows organizations to take proactive measures to mitigate risks before they materialize.

### Automated Compliance Checks

AI can automate the process of checking SaaS vendors' compliance with various regulations and security standards. This helps ensure that all components of the supply chain meet necessary requirements and reduces the manual effort required for compliance audits.

## The Role of Government and Industry Collaboration

Addressing the full scope of supply chain security risks requires collaboration between the public and private sectors. Initiatives like the U.S. Cybersecurity and Infrastructure Security Agency's (CISA) efforts around SBOMs and the National Institute of Standards and Technology's (NIST) Secure Software Development Framework (SSDF) are important steps.

However, more work is needed to develop comprehensive standards, improve information sharing, and provide resources for smaller organizations that may lack the expertise to tackle these challenges independently.

## Looking Ahead

As we move further into 2024 and beyond, the importance of understanding and mitigating supply chain risks will only grow. The increasing adoption of cloud services, the Internet of Things (IoT), and edge computing will continue to expand the attack surface. At the same time, geopolitical tensions and the commoditization of cyber weapons raise the stakes for critical infrastructure and national security.

Organizations that fail to grasp the true scope and potential impact of supply chain attacks risk finding themselves unprepared for the next major incident. By taking a holistic view of their ecosystem, implementing defense-in-depth strategies, and fostering a culture of security awareness, companies can build the resilience needed to weather the evolving threat landscape.

## Conclusion

The convergence of supply chain complexities, the rise of SaaS and MSS providers, and advancements in AI have created a new frontier in cybersecurity. While these technologies offer significant benefits in terms of scalability and efficiency, they also introduce new vulnerabilities that adversaries are eager to exploit.

Securing the global supply chain is a shared responsibility that requires ongoing vigilance, innovation, and collaboration across industries and borders. By leveraging AI intelligently, enhancing third-party risk management, and adopting adaptive security measures, organizations can strike a balance between reaping the benefits of modern technologies and maintaining a strong, resilient security posture.

## Data and sources:

<details>
<summary>Data and sources:</summary>

1. [10xDS: 7 Ways Gen AI Can Improve Supply Chain Risk Management](https://10xds.com/blog/7-ways-gen-ai-can-improve-supply-chain-risk-management/)
2. [AppVinTech: Challenges of AI and Machine Learning in Supply Chain Management](https://appvintech.com/challenges-of-ai-and-machine-learning-in-supply-chain-management/)
3. [Consumer Goods Technology: The Future of AI in the Supply Chain](https://consumergoods.com/future-ai-supply-chain)
4. [Darktrace: The Future of Cyber Security - Software Supply Chain Attacks Become a Given in 2022](https://darktrace.com/es/blog/the-future-of-cyber-security-software-supply-chain-attacks-become-a-given-in-2022)
5. [Throughput: Challenges of AI in Supply Chain](https://throughput.world/blog/challenges-of-ai-in-supply-chain/)
6. [AppSoc: AI is the New Frontier of Supply Chain Security](https://www.appsoc.com/blog/ai-is-the-new-frontier-of-supply-chain-security)
7. [Dark Reading: Hardware Supply Chain Threats Can Undermine Endpoint Infrastructure](https://www.darkreading.com/vulnerabilities-threats/hardware-supply-chain-threats-can-undermine-endpoint-infrastructure)
8. [Dark Reading: Rising Tide of Software Supply Chain Attacks](https://www.darkreading.com/vulnerabilities-threats/rising-tide-of-software-supply-chain-attacks)
9. [Everbridge: How Centaur AI Will Shape the Future of Risk Management](https://www.everbridge.com/blog/how-centaur-ai-will-shape-the-future-of-risk-management/)
10. [Forbes: Predictions for SaaS Security in 2024 - Trends to Watch](https://www.forbes.com/councils/forbestechcouncil/2023/12/04/predictions-for-saas-security-in-2024-trends-to-watch/)
11. [Forbes: Rising Threat - Understanding Software Supply Chain Cyberattacks and Protecting Against Them](https://www.forbes.com/councils/forbestechcouncil/2024/02/06/rising-threat-understanding-software-supply-chain-cyberattacks-and-protecting-against-them/)
12. [InfoWorld: Protecting Against Software Supply Chain Attacks](https://www.infoworld.com/article/2335938/protecting-against-software-supply-chain-attacks.html)
13. [Inspectorio: Supply Chain Professionals View AI as a Key Tool to Drive Innovation](https://www.inspectorio.com/press-release/supply-chain-professionals-view-ai-as-a-key-tool-to-drive-innovation)
14. [IS Partners: SCRM - Supply Chain Risk Management](https://www.ispartnersllc.com/blog/scrm-supply-chain-risk-management/)
15. [LinkedIn: Harnessing AI-Enhanced Supply Chain Risk Management](https://www.linkedin.com/pulse/harnessing-ai-enhanced-supply-chain-risk-management-defense-logistics-m3qte)
16. [Nudge Security: SaaS Supply Chain Management](https://www.nudgesecurity.com/it-security-resources/saas-supply-chain-management)
17. [Nudge Security: SaaS Supply Chain Risks](https://www.nudgesecurity.com/use-cases/saas-supply-chain-risks)
18. [OMNITRACKER: AI in Risk Management](https://www.omnitracker.com/en/resources/news/ai-in-risk-management/)
19. [Supply Chain Management Review: Enhancing Operational Intelligence in Supply Chain Management Through AI/ML](https://www.scmr.com/article/enhancing-operational-intelligence-in-supply-chain-management-through-ai-ml)
20. [Security Week: Cyber Insights 2024 - Supply Chain](https://www.securityweek.com/cyber-insights-2024-supply-chain/)
21. [Simform: AI in Supply Chain](https://www.simform.com/blog/ai-in-supply-chain/)
22. [Supply Chain Brain: Are SaaS Apps the Achilles Heel for Supply Chain Attacks?](https://www.supplychainbrain.com/blogs/1-think-tank/post/38279-are-saas-apps-the-achilles-heel-for-supply-chain-attacks)
23. [Trax Technologies: The Future of Risk Management in the Supply Chain - Trends & Predictions](https://www.traxtech.com/blog/the-future-of-risk-management-in-the-supply-chain-trends-predictions)
24. [Valence Security: 2024 State of SaaS Security Report](https://www.valencesecurity.com/lp/2024-state-of-saas-security-report)
25. [Zscaler: New and Critical Layer to Protect Data - SaaS Supply Chain Security](https://www.zscaler.fr/blogs/product-insights/new-and-critical-layer-protect-data-saas-supply-chain-security)
26. [Zycus: AI for Supplier Risk Management for Resilient Supply Chains](https://www.zycus.com/blog/generative-ai/ai-for-supplier-risk-management-for-resilient-supply-chains)

</details>