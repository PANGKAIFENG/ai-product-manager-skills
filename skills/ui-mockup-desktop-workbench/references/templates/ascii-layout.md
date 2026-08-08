# ASCII Layout Template

```text
+--------------------------------------------------------------------------------+
| App shell / top bar                                                            |
+----------------------+----------------------------------+----------------------+
| Left rail            | Main work area                   | Inspector / artifact |
| - Nav                | - Primary content                | - Details            |
| - Context            | - State-specific region          | - Actions            |
| - Settings           | - Scroll container               | - Recovery           |
+----------------------+----------------------------------+----------------------+
| Status / footer / transient feedback                                           |
+--------------------------------------------------------------------------------+
```

Add a variant when a state changes the layout structure, not only the content.
Label fixed rails, flexible regions, scroll containers, primary actions, and
modal overlays explicitly.
