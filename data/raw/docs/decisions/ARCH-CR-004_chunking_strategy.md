# DOCUMENT METADATA AND APPROVAL TRAIL
- **Document ID**: ARCH-CR-004
- **Version**: 1.0
- **Effective Date**: 2024-01-20
- **Review Cycle**: Annual
- **Owner Team**: Architecture Committee
- **Owner Email**: arch-committee@asterion.example
- **Approved By**: Rajesh Venkatraman (Service Delivery Manager, NexaTel)
- **Approval Date**: 2024-01-20
- **Classification**: Restricted - Internal Use Only

## REVISION HISTORY
| Version | Date | Author | Summary of Changes |
|---|---|---|---|
| 1.0 | 2021-01-15 | SRE Lead | Initial draft and release |
| 1.1 | 2022-04-10 | Operations Manager | Updated escalation matrices and team roles |
| 1.0 | 2024-01-20 | SRE Lead | Extended documentation with production runbooks and enterprise details |

## GLOSSARY
- **SLA (Service Level Agreement)**: A formal agreement defining the expected service levels and performance metrics between the service provider and the customer.
- **SLO (Service Level Objective)**: Target metrics defined within an SLA (e.g., 99.9% uptime).
- **SLI (Service Level Indicator)**: The actual measured service level (e.g., latency, throughput).
- **OCS (Online Charging System)**: A telecom system that performs real-time rating and charging of network events.
- **CDR (Call Detail Record)**: A data record documenting the details of a telecommunications transaction (e.g., call time, duration, data usage).
- **TAP3 (Transferred Account Procedure version 3)**: Standard format for exchanging roaming billing data between mobile network operators.
- **HSS (Home Subscriber Server)**: A central database containing subscriber-related and subscription-related information.
- **MSISDN (Mobile Station International Subscriber Directory Number)**: The standard telephone number identifying a mobile subscription.
- **eSIM (Embedded Subscriber Identity Module)**: A digital SIM that allows activation of a cellular plan without a physical SIM card.
- **NOC (Network Operations Center)**: A centralized location where IT/telecom infrastructure is monitored and managed.
- **SRE (Site Reliability Engineering)**: An engineering discipline that applies software engineering principles to operations and infrastructure.
- **MFA (Multi-Factor Authentication)**: A security system requiring multiple credentials for access verification.
- **API (Application Programming Interface)**: A set of protocols for building and integrating application software.
- **ITIL (Information Technology Infrastructure Library)**: A set of detailed practices for IT service management.
- **CI/CD (Continuous Integration/Continuous Deployment)**: A set of operating principles and practices for automated software delivery.
- **TAP (Transferred Account Procedure)**: The billing process for roaming between mobile operators.
- **TAP validator**: Component that validates TAP files for correctness.
- **IMSI (International Mobile Subscriber Identity)**: Unique identifier for a mobile network user.
- **HLR (Home Location Register)**: The main database of permanent subscriber information for a mobile network.
- **SMSC (Short Message Service Center)**: The network element that manages the routing and delivery of SMS text messages.
- **SMPP (Short Message Peer-to-Peer)**: A protocol used for exchanging SMS messages between SMSCs and routing entities.

# Decision Record: RAG Document Chunking Strategy
## Document ID: ARCH-CR-004 | Status: Approved | Date: 2024-01-18 | Owner: Arjun Mehta

### Context
To ensure high retrieval precision and minimize hallucination in SentinelIQ's RAG pipeline, we must define a domain-specific chunking strategy for each data type indexed in the vector store.

### Evaluation Criteria
1. Retrieval Recall: Ability to fetch the exact context needed.
2. Context Conservation: Ensuring related tables and steps remain within the same chunk.
3. Token Economy: Avoiding bloating the LLM prompt with irrelevant context.

### Chunking Strategy by Data Type

#### 1. Support Tickets
- **Rule**: Exactly 1 ticket per chunk.
- **Rationale**: Splitting a ticket across chunks separates customer symptoms from SRE resolution steps. Tickets are stored as a single text block containing metadata, description, and comments list.

#### 2. Operational Policies
- **Rule**: Fixed-size chunking with overlaps (500–800 tokens, 100-token overlap).
- **Rationale**: Policy documents are long and prose-heavy. This chunk size ensures complete paragraphs and rules are preserved.

#### 3. Release Notes
- **Rule**: Chunk-by-feature. Each release note document is parsed, and each feature/fix description block is stored as a separate chunk.
- **Rationale**: SREs search for specific software regressions. Storing individual fixes prevents unrelated feature descriptions from diluting semantic search results.

#### 4. Operational Logs
- **Rule**: 5-minute sliding window aggregation.
- **Rationale**: Systems emit thousands of logs during failures. Grouping logs into 5-minute chunks preserves temporal correlation during incidents.

### Consequences
1. Custom parsers must be built for each data type in the ETL ingestion code.
2. Changes to document layout formats will require parser updates and index rebuilds.


## PROOF-OF-CONCEPT RESULTS
To validate this decision, a Proof-of-Concept (POC) was executed over 14 days under a simulated environment:
- **Baseline performance**: Latency of 200ms/query on standard data volume.
- **POC Test Results**: Tested Vector DB query latency with 100,000 document chunks.
  - *Chroma DB*: 15ms P50 latency, 35ms P99 latency.
  - *Alternative Vector DB*: 45ms P50 latency, 110ms P99 latency.
  - *Recommendation*: Chroma DB provides optimal latency and scaling features.

## RISK REGISTER
| Risk ID | Risk Description | Probability | Impact | Mitigation Plan |
|---|---|---|---|---|
| R-DEC-001 | LLM API Token quota limit exceeded during critical outage | Medium | High | Implement fallback to local offline embedding models and caching. |
| R-DEC-002 | Memory leakage in vector DB service | Low | Medium | Setup automated pod recycling in Kubernetes when memory exceeds 80%. |

## IMPLEMENTATION TIMELINE
```mermaid
gantt
    title Decision Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1: Setup
    Docker container configuration :active, 2024-01-20, 5d
    section Phase 2: Indexing
    Metadata scheme definition : 2024-01-25, 4d
    Initial document indexing : 2024-01-29, 6d
    section Phase 3: Testing
    Performance verification & sign-off : 2024-02-04, 3d
```

## SUCCESS METRICS
- **RAG Retrieve Recall**: > 98% accuracy on verification dataset.
- **RAG Generation Answer Quality**: Score > 4.5/5 on G-Eval criteria.
- **Response Latency**: Core pipeline execution under 1,200ms per query.


## PROOF-OF-CONCEPT RESULTS
To validate this decision, a Proof-of-Concept (POC) was executed over 14 days under a simulated environment:
- **Baseline performance**: Latency of 200ms/query on standard data volume.
- **POC Test Results**: Tested Vector DB query latency with 100,000 document chunks.
  - *Chroma DB*: 15ms P50 latency, 35ms P99 latency.
  - *Alternative Vector DB*: 45ms P50 latency, 110ms P99 latency.
  - *Recommendation*: Chroma DB provides optimal latency and scaling features.

## RISK REGISTER
| Risk ID | Risk Description | Probability | Impact | Mitigation Plan |
|---|---|---|---|---|
| R-DEC-001 | LLM API Token quota limit exceeded during critical outage | Medium | High | Implement fallback to local offline embedding models and caching. |
| R-DEC-002 | Memory leakage in vector DB service | Low | Medium | Setup automated pod recycling in Kubernetes when memory exceeds 80%. |

## IMPLEMENTATION TIMELINE
```mermaid
gantt
    title Decision Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1: Setup
    Docker container configuration :active, 2024-01-20, 5d
    section Phase 2: Indexing
    Metadata scheme definition : 2024-01-25, 4d
    Initial document indexing : 2024-01-29, 6d
    section Phase 3: Testing
    Performance verification & sign-off : 2024-02-04, 3d
```

## SUCCESS METRICS
- **RAG Retrieve Recall**: > 98% accuracy on verification dataset.
- **RAG Generation Answer Quality**: Score > 4.5/5 on G-Eval criteria.
- **Response Latency**: Core pipeline execution under 1,200ms per query.


## PROOF-OF-CONCEPT RESULTS
To validate this decision, a Proof-of-Concept (POC) was executed over 14 days under a simulated environment:
- **Baseline performance**: Latency of 200ms/query on standard data volume.
- **POC Test Results**: Tested Vector DB query latency with 100,000 document chunks.
  - *Chroma DB*: 15ms P50 latency, 35ms P99 latency.
  - *Alternative Vector DB*: 45ms P50 latency, 110ms P99 latency.
  - *Recommendation*: Chroma DB provides optimal latency and scaling features.

## RISK REGISTER
| Risk ID | Risk Description | Probability | Impact | Mitigation Plan |
|---|---|---|---|---|
| R-DEC-001 | LLM API Token quota limit exceeded during critical outage | Medium | High | Implement fallback to local offline embedding models and caching. |
| R-DEC-002 | Memory leakage in vector DB service | Low | Medium | Setup automated pod recycling in Kubernetes when memory exceeds 80%. |

## IMPLEMENTATION TIMELINE
```mermaid
gantt
    title Decision Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1: Setup
    Docker container configuration :active, 2024-01-20, 5d
    section Phase 2: Indexing
    Metadata scheme definition : 2024-01-25, 4d
    Initial document indexing : 2024-01-29, 6d
    section Phase 3: Testing
    Performance verification & sign-off : 2024-02-04, 3d
```

## SUCCESS METRICS
- **RAG Retrieve Recall**: > 98% accuracy on verification dataset.
- **RAG Generation Answer Quality**: Score > 4.5/5 on G-Eval criteria.
- **Response Latency**: Core pipeline execution under 1,200ms per query.

## APPENDIX B: SRE SUPPLEMENTAL RUNBOOK SCENARIOS
This appendix details specific SRE runtime scenario verifications and verification checklists.
### SCENARIO-VER-101: Operational Verification Scenario 1
Standard verification checks for operational consistency of this decision outcome under load condition 1.
1. Run verification test suite against target database endpoints and check query latency.
2. Audit active connections pool saturation and verify it is under the 80% threshold limit.
3. Monitor Kubernetes pod logs for transient exception patterns or connection drop-offs.
### SCENARIO-VER-102: Operational Verification Scenario 2
Standard verification checks for operational consistency of this decision outcome under load condition 2.
1. Run verification test suite against target database endpoints and check query latency.
2. Audit active connections pool saturation and verify it is under the 80% threshold limit.
3. Monitor Kubernetes pod logs for transient exception patterns or connection drop-offs.
### SCENARIO-VER-103: Operational Verification Scenario 3
Standard verification checks for operational consistency of this decision outcome under load condition 3.
1. Run verification test suite against target database endpoints and check query latency.
2. Audit active connections pool saturation and verify it is under the 80% threshold limit.
3. Monitor Kubernetes pod logs for transient exception patterns or connection drop-offs.
### SCENARIO-VER-104: Operational Verification Scenario 4
Standard verification checks for operational consistency of this decision outcome under load condition 4.
1. Run verification test suite against target database endpoints and check query latency.
2. Audit active connections pool saturation and verify it is under the 80% threshold limit.
3. Monitor Kubernetes pod logs for transient exception patterns or connection drop-offs.
### SCENARIO-VER-105: Operational Verification Scenario 5
Standard verification checks for operational consistency of this decision outcome under load condition 5.
1. Run verification test suite against target database endpoints and check query latency.
2. Audit active connections pool saturation and verify it is under the 80% threshold limit.
3. Monitor Kubernetes pod logs for transient exception patterns or connection drop-offs.
### SCENARIO-VER-106: Operational Verification Scenario 6
Standard verification checks for operational consistency of this decision outcome under load condition 6.
1. Run verification test suite against target database endpoints and check query latency.
2. Audit active connections pool saturation and verify it is under the 80% threshold limit.
3. Monitor Kubernetes pod logs for transient exception patterns or connection drop-offs.
### SCENARIO-VER-107: Operational Verification Scenario 7
Standard verification checks for operational consistency of this decision outcome under load condition 7.
1. Run verification test suite against target database endpoints and check query latency.
2. Audit active connections pool saturation and verify it is under the 80% threshold limit.
3. Monitor Kubernetes pod logs for transient exception patterns or connection drop-offs.
### SCENARIO-VER-108: Operational Verification Scenario 8
Standard verification checks for operational consistency of this decision outcome under load condition 8.
1. Run verification test suite against target database endpoints and check query latency.
2. Audit active connections pool saturation and verify it is under the 80% threshold limit.
3. Monitor Kubernetes pod logs for transient exception patterns or connection drop-offs.
### SCENARIO-VER-109: Operational Verification Scenario 9
Standard verification checks for operational consistency of this decision outcome under load condition 9.
1. Run verification test suite against target database endpoints and check query latency.
2. Audit active connections pool saturation and verify it is under the 80% threshold limit.
3. Monitor Kubernetes pod logs for transient exception patterns or connection drop-offs.