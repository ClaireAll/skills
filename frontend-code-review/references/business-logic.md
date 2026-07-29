# Rule Catalog — Business Logic

## Can't use workflowStore in Node components

IsUrgent: True

### Description

File path pattern of node components: `web/app/components/workflow/nodes/[nodeName]/node.tsx`

Node components are also used when creating a RAG Pipe from a template, but in that context there is no workflowStore Provider, which results in a blank screen. [This Issue](https://github.com/langgenius/dify/issues/29168) was caused by exactly this reason.

### Suggested Fix

Use `import { useNodes } from 'reactflow'` instead of `import useNodes from '@/app/components/workflow/store/workflow/use-nodes'`.

## Impact surface follows call sites and data flow

IsUrgent: True

### Description

For bug fixes that change fields, service methods, API shapes, shared components, routing, or cross-package contracts, review beyond the touched file. Search the monorepo for the changed names and trace the entry point, implementation, defaults, runtime inputs, and consumers. A passing typecheck only proves the type chain; it does not prove every semantic branch or host implementation was updated.

### Suggested Fix

Ask for or perform a call-site/data-flow audit before approving the change. The finding should name the unreviewed consumers or the concrete modules that must be included in regression testing.
