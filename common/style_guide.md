# DualTwin Technologies 360° - Style Guide

This document defines the standards and conventions for all content in this repository. Every contributor must follow these guidelines to maintain consistency across all concept modules.

## Folder Structure

Each concept folder must follow this exact structure:

```
/<concept_slug>/
├── README.md                      # 4W+H documentation
├── intro_<concept_slug>.ipynb     # Introduction notebook
├── examples_<concept_slug>.ipynb  # Examples notebook
├── exercises_<concept_slug>.ipynb # Exercises notebook
├── code/
│   ├── main_<concept_slug>.py     # Main executable script
│   └── config_<concept_slug>.yaml # Configuration (if needed)
└── html_demo/
    ├── index.html                 # Main HTML demo page
    ├── styles.css                 # Stylesheet
    └── script.js                  # JavaScript for animations
```

## README.md Template (4W+H Format)

Every concept README must include these sections in order:

### Header
```markdown
# [Concept Number] - [Concept Title]

> [One-sentence summary for quick reference]
```

### What?

**Non-Technical Explanation:**
Start with a simple analogy or real-world comparison that anyone can understand. Avoid technical jargon.

**Technical Definition:**
Provide a precise technical definition for IT professionals. Include relevant terminology and concepts.

### Why?

Explain the importance and benefits:
- Business value
- Operational improvements
- Cost savings
- Risk reduction
- Innovation enablement

Include 2-3 concrete scenarios where this concept improves outcomes.

### Where?

**Industries:**
List specific industries where this concept applies (manufacturing, energy, healthcare, etc.)

**Systems:**
List types of systems or assets (production lines, turbines, buildings, vehicles, etc.)

**Platforms:**
Mention deployment environments (cloud, edge, on-premises, hybrid)

### Who?

**Roles that interact with this concept:**
- Operators
- Engineers
- Data Scientists
- Managers
- Executives

**Non-IT vs IT perspectives:**
Explain what each group cares about regarding this concept.

### How?

**High-Level Process:**
Describe the workflow in 5-7 steps.

**Architecture Overview:**
Include a text-based or linked diagram showing:
- Data sources
- Ingestion layer
- Processing layer
- Twin model
- Visualization/Control layer

### Key Terms

Provide a glossary of 5-10 important terms used in this concept.

### Relations to Other Concepts

Explain how this concept connects to other modules in the repository.

### Programs in This Folder

List each program with:
- Short description
- Command to run
- Expected output

## Jupyter Notebook Standards

### Introduction Notebook (intro_*.ipynb)

Structure:
1. Title and overview (markdown cell)
2. Learning objectives (3-5 bullet points)
3. 4W+H explanation with text and diagrams
4. Simple code demonstration
5. Visualization of key concepts
6. Summary and next steps

### Examples Notebook (examples_*.ipynb)

Structure:
1. Brief introduction
2. 2-4 concrete examples, each with:
   - Problem statement
   - Solution approach
   - Code implementation
   - Visualization
   - Key takeaways
3. Summary

### Exercises Notebook (exercises_*.ipynb)

Structure:
1. Instructions
2. Conceptual questions (4W+H format)
3. Coding exercises with:
   - Clear requirements
   - Starter code
   - Hints
   - (Optional) Solutions in collapsed cells
4. Challenge problems for advanced learners

## Python Code Standards

### File Header
```python
"""
[Concept Name] - [File Purpose]

This script demonstrates [brief description].

Usage:
    python main_<concept_slug>.py [options]

Example:
    python main_01_digital_twin_fundamentals.py --duration 60
"""
```

### Code Style
- Follow PEP 8 guidelines
- Maximum line length: 100 characters
- Use type hints for function parameters and returns
- Include docstrings for all classes and functions
- Use meaningful variable names

### Output Format
- Print clear section headers
- Show progress for long operations
- Display results in readable format
- Include timestamps where relevant

### Error Handling
- Catch and handle expected errors gracefully
- Provide helpful error messages
- Log errors appropriately

## HTML Demo Standards

### index.html Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Concept Name] - DualTwin 360°</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header><!-- Navigation and title --></header>
    <main>
        <section id="what"><!-- What section --></section>
        <section id="why"><!-- Why section --></section>
        <section id="where"><!-- Where section --></section>
        <section id="who"><!-- Who section --></section>
        <section id="how"><!-- How section with animation --></section>
    </main>
    <footer><!-- Links and credits --></footer>
    <script src="script.js"></script>
</body>
</html>
```

### CSS Guidelines
- Use CSS variables for colors and spacing
- Mobile-first responsive design
- Consistent spacing and typography
- Professional color scheme (blues, grays, accents)

### JavaScript Guidelines
- No external dependencies (vanilla JS only)
- Progressive enhancement
- Accessible interactions
- Smooth animations using CSS transitions or requestAnimationFrame

### Required Features
- View toggle: "Non-Technical" vs "Technical" mode
- Step-by-step animation for the "How" section
- Interactive elements for engagement
- Responsive design for all screen sizes

## Writing Style

### For Non-Technical Audience
- Use analogies and real-world examples
- Avoid acronyms without explanation
- Focus on outcomes and benefits
- Use active voice
- Keep sentences short

### For Technical Audience
- Be precise with terminology
- Include architecture details
- Reference standards and protocols
- Provide implementation guidance
- Link to external resources

## Quality Checklist

Before submitting any concept module, verify:

- [ ] README follows 4W+H template completely
- [ ] All three notebooks run without errors
- [ ] Python scripts execute successfully
- [ ] HTML demo opens and animates correctly
- [ ] Code is properly commented
- [ ] No hardcoded paths or credentials
- [ ] Consistent naming conventions used
- [ ] Cross-references to other concepts are accurate
- [ ] Spelling and grammar checked
- [ ] Mobile responsiveness tested for HTML
