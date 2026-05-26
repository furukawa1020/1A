# Condition Texts

The condition file is:

```text
app/conditions/conditions_2x2x2.json
```

Conditions are not hard-coded into the renderer. The app loads the JSON file and changes only:

- `processing_text`
- `visibility_text`
- `output_text`

The same UI template, layout, colors, typography, and response items are used across all eight conditions.

## Common Scenario

The common scenario avoids saying that the participant is low-performing, stressed, lazy, or definitely experiencing concentration decline. It describes only a presenteeism context:

- not fully well,
- not absent or withdrawn,
- still participating,
- feeling some strain internally.

## Output Text Control

Assertive outputs use labels and recommendations. Non-assertive outputs use cues and interpretive space. Both are rendered in the same output block with the same number of output lines.

