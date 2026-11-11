# Graph Report - Docs-service  (2026-11-12)

## Corpus Check
- В структурный анализ включено файлов исходного кода: 5. Сторонние зависимости, документация и файлы окружения исключены.

## Summary
- 29 nodes · 45 edges · 6 communities (1 shown, 5 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- kafka_consumer.py
- generate_docs
- Settings
- start_consuming
- _parse_payload

## God Nodes (most connected - your core abstractions)
1. `generate_docs()` - 8 edges
2. `start_consuming()` - 5 edges
3. `produce_message()` - 4 edges
4. `_parse_payload()` - 4 edges
5. `Settings` - 3 edges
6. `_resolve_context()` - 3 edges
7. `_resolve_template()` - 3 edges
8. `producer_callback()` - 2 edges
9. `main()` - 2 edges
10. `Config` - 1 edges

## Surprising Connections (you probably didn't know these)
- `start_consuming()` --calls--> `produce_message()`  [EXTRACTED]
  kafka_consumer.py → kafka_producer.py
- `start_consuming()` --calls--> `generate_docs()`  [EXTRACTED]
  kafka_consumer.py → document_generator.py
- `main()` --calls--> `start_consuming()`  [EXTRACTED]
  main.py → kafka_consumer.py

## Import Cycles
- None detected.

## Communities (6 total, 5 thin omitted)

### Community 2 - "generate_docs"
Cohesion: 0.60
Nodes (3): generate_docs(), _resolve_context(), _resolve_template()

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `generate_docs()` connect `generate_docs` to `kafka_consumer.py`, `document_generator.py`, `start_consuming`, `_parse_payload`?**
  _High betweenness centrality (0.212) - this node is a cross-community bridge._
- **Why does `Settings` connect `Settings` to `kafka_consumer.py`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Why does `start_consuming()` connect `start_consuming` to `kafka_consumer.py`, `generate_docs`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._