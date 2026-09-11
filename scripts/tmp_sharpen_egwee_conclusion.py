from pathlib import Path

p = Path('manuscript/natural_data_ecological_indicators_spine.md')
text = p.read_text(encoding='utf-8')
anchor = '## 5. Claim ceiling\n'
if text.count(anchor) != 1:
    raise RuntimeError(f'expected one claim-ceiling anchor, found {text.count(anchor)}')
conclusion = '''## 5. Conclusion\n\nAcross the seven locked natural-data analyses, the common result is not a shared ecological effect of islandness, urbanisation, fragmentation or pollination. The common result is an **ordered inferential constraint**: a variable may be interpreted as an ecological state indicator only after its measurement has earned endpoint-relevant status, its analytical representation has preserved the information it claims to contain, any residual context has been tested for transferable predictive gain, and the requested cross-system comparison is identifiable. The analyses show that each of these gates can fail for a different reason in real ecological datasets.\n\nThe paper's positive conclusion is therefore:\n\n> **Test the state before interpreting the residual.** Residual geography, habitat, origin or history is biologically interpretable only after the proposed state itself has passed measurement and representation checks; otherwise the residual cannot diagnose state incompleteness, and its absence cannot certify state sufficiency.\n\nThis is stronger than a reporting checklist but narrower than a universal ecological law: it specifies the order in which downstream interpretation becomes licensed by evidence.\n\n## 6. Claim ceiling\n'''
text = text.replace(anchor, conclusion, 1)
p.write_text(text, encoding='utf-8')
print('sharpened EGWEE conclusion')
