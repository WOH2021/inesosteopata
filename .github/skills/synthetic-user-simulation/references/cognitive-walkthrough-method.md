# Cognitive Walkthrough Method — Adapted for Mock User Simulation

## Background

The cognitive walkthrough is a usability inspection method that evaluates an interface by simulating a user's thought process at each step of a task. Originally developed by Wharton et al. (1994), it focuses on **learnability** — how easily a new or infrequent user can accomplish tasks.

This skill adapts the method for AI-simulated personas rather than human evaluators.

## Core Questions (per step)

At each interaction step, evaluate from the persona's perspective:

1. **Will the user try to achieve the right effect?**

   - Does the persona understand what they need to do next?
   - Does their goal align with what the interface expects?

2. **Will the user notice the correct action is available?**

   - Is the relevant control visible and recognisable to this persona?
   - Given their vocabulary and mental model, will they identify it?

3. **Will the user associate the correct action with the desired effect?**

   - Does the label/icon match what the persona expects?
   - Could they confuse it with another action?

4. **Will the user interpret the system's feedback correctly?**
   - After acting, does the persona understand what happened?
   - Is the feedback timely, clear, and in their vocabulary?

## Adaptation for Persona Simulation

When using this method with a simulated persona:

### Grounding in persona data

- Every judgment must trace back to a specific persona attribute (tech literacy, vocabulary, frustration triggers, etc.)
- If a judgment cannot be grounded, flag it as an assumption

### Severity assessment

Map each failure to a severity level:

- **Blocker**: Persona cannot answer YES to question 1 or 2 — they cannot proceed
- **High**: Persona struggles significantly with question 3 or 4 — they proceed but with high friction
- **Medium**: Persona hesitates or makes an error but self-corrects
- **Low**: Minor confusion that doesn't materially affect task completion

### Think-aloud simulation (Deep dive mode)

For deep-dive walkthroughs, narrate the persona's internal monologue:

- What are they looking at?
- What are they thinking?
- What do they expect to happen?
- How do they feel when something unexpected occurs?

## Limitations

- **Not a replacement for real users.** Simulated walkthroughs reflect the quality of the persona definition and the evaluator's interpretation.
- **Bias toward learnability.** The method favours first-use scenarios; expert workflows may be under-represented.
- **Interface inspection required.** Without actual interface inspection (URL, screenshots, Figma), findings are speculative. Always flag uninspected assumptions.

## References

- Wharton, C., Rieman, J., Lewis, C., & Polson, P. (1994). The cognitive walkthrough method: A practitioner's guide.
- Spencer, R. (2000). The streamlined cognitive walkthrough method. CHI 2000.
- Mahatody, T., Sagar, M., & Kolski, C. (2010). State of the art on the cognitive walkthrough method. _Journal of Universal Computer Science_.
