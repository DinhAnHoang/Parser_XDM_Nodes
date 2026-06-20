# XDM Node Name Tree Export Design

## Objective

Parse an EB Tresos XDM file and export a tree of node names into one XML file that can be opened by Excel.

The parser must be generic. Do not create CAN-specific data models or hard-code CAN node names, except in examples and tests.

## Scope

Current input behavior:

- The Python script receives a module name parameter.
- Treat `Configuration Tool` as the root path.
- Resolve the module by finding a matching `<Module>.xdm` file only under `Can_TS_T40D2M10I1R0/config`.
- Matching should be case-insensitive.
- Current known files:
  - `CAN` resolves to `Can_TS_T40D2M10I1R0/config/Can.xdm`
  - `Gpt` resolves to `Can_TS_T40D2M10I1R0/config/Gpt.xdm`

Ignored project area:

- Always ignore `Reffer project`.

Current output:

- One Excel-openable `.xml` file.
- Output file name is `<InputFileStem>_NodeTree.xml`.
  - `Can.xdm` exports to `Can_NodeTree.xml`.
  - `Gpt.xdm` exports to `Gpt_NodeTree.xml`.
- The file contains the node-name tree rooted at `<d:lst type="TOP-LEVEL-PACKAGES">`.
- Current version exports only two columns:
  - `PathName`
  - `Type`

Do not export AUTOSAR attributes in the current version.

## XDM Node Categories

The XDM rules are documented in `ai/XDM rule.md`.

Supported tree nodes:

- Data nodes: `d:ctr`, `d:lst`, `d:var`, `d:ref`, `d:chc`
- Schema nodes: `v:ctr`, `v:lst`, `v:var`, `v:ref`, `v:chc`

Ignored nodes for the node-name tree:

- Attribute nodes: `a:a`, `a:da`, `a:v`, `a:tst`, and other `a:*` nodes
- Generic XML wrapper nodes outside the selected root, such as `<datamodel>`
- Comments and text content

Important: ignored nodes may contain useful metadata later, but they must not become path segments for this output.

## Namespace Handling

The parser must read all namespace declarations using `ElementTree.iterparse(..., events=["start-ns"])`.

The parser must support namespaces declared at:

- root `<datamodel>`
- nested AUTOSAR factory nodes such as `<d:ctr type="AUTOSAR" factory="autosar">`

Do not rely on literal prefixes only. Resolve namespace URIs, then classify an element as data/schema/attribute by its namespace.

Known namespace roles from the current XDM format:

- `d`: data namespace
- `v`: schema namespace
- `a`: attribute namespace

## Tree Root

The logical root of the exported tree is the data list:

```xml
<d:lst type="TOP-LEVEL-PACKAGES">
```

Do not include these ancestors in output paths:

- `<datamodel>`
- `<d:ctr type="AUTOSAR" factory="autosar">`
- `<d:lst type="TOP-LEVEL-PACKAGES">`

Start exported paths from the children of `<d:lst type="TOP-LEVEL-PACKAGES">`.

In `Can.xdm`, the first exported package node is:

```xml
<d:ctr name="TS_T40D2M10I1R0" type="AR-PACKAGE">
```

So exported paths begin with:

```text
TS_T40D2M10I1R0
```

## Node Name Rule

For every supported `d:*` or `v:*` node:

1. If the XML element has a `name` attribute, use that value as the path segment.
2. If the XML element has no `name` attribute, use the literal segment `none`.
3. Do not use `type`, `value`, tag name, namespace prefix, or text content as fallback names.
4. Do not include `a:*` attribute node names in the path.

Example:

```xml
<d:ctr name="TS_T40D2M10I1R0" type="AR-PACKAGE">
    <a:a name="UUID" value="ECUC:181f65b6-f772-4dd7-b9a6-1186c4c7eba8" />
    <d:lst type="ELEMENTS">
        <d:chc name="Can" type="AR-ELEMENT" value="MODULE-DEF">
```

The expected path is:

```text
TS_T40D2M10I1R0/none/Can
```

Explanation:

- `TS_T40D2M10I1R0` comes from `d:ctr @name`.
- `none` comes from `d:lst type="ELEMENTS"` because it has no `name` attribute.
- `Can` comes from `d:chc @name`.
- `UUID` is ignored because `<a:a>` is an attribute node.

## Traversal Rule

Traverse descendants of `<d:lst type="TOP-LEVEL-PACKAGES">` in document order.

When visiting a supported tree node:

- Create the node segment using the Node Name Rule.
- Append the segment to the current parent path.
- Emit one output row for the current node.
- Continue recursively through its children.

When visiting an ignored node:

- Do not emit a row for that node.
- Do not add a path segment for that node.
- Continue traversal only if needed to reach supported descendant nodes.

This matters because a supported node can appear below ignored metadata wrappers in future XDM files.

## Required Example From `Can.xdm`

Inside `Can_TS_T40D2M10I1R0/config/Can.xdm`, the top-level package contains:

```xml
<d:lst type="TOP-LEVEL-PACKAGES">
    <d:ctr name="TS_T40D2M10I1R0" type="AR-PACKAGE">
        <a:a name="UUID" value="ECUC:181f65b6-f772-4dd7-b9a6-1186c4c7eba8" />
        <d:lst type="ELEMENTS">
            <d:chc name="Can" type="AR-ELEMENT" value="MODULE-DEF">
            <d:chc name="Can_EcuParameterDefinition" type="AR-ELEMENT" value="ECU_PARAMETER_DEFINITION">
            <d:chc name="Can_ModuleDescription" type="AR-ELEMENT" value="BSW_MODULE_DESCRIPTION">
```

The output must include at least:

```text
TS_T40D2M10I1R0
TS_T40D2M10I1R0/none
TS_T40D2M10I1R0/none/Can
TS_T40D2M10I1R0/none/Can_EcuParameterDefinition
TS_T40D2M10I1R0/none/Can_ModuleDescription
```

The example paths requested by the user are:

```text
TS_T40D2M10I1R0/none/Can
TS_T40D2M10I1R0/none/Can_EcuParameterDefinition
TS_T40D2M10I1R0/none/Can_ModuleDescription
```

The full output must continue below `TS_T40D2M10I1R0/none/Can` and include all nested schema and data nodes using the same rule.

## Current Row Model

Each output row should contain two values:

- `PathName`: slash-separated node-name path
- `Type`: XML `type` attribute from the same supported node. If the node has no `type` attribute, use `none`.

Do not add `Level`, `NodeName`, `NamespaceRole`, `Kind`, `Value`, or attribute columns in the current version.

Future versions may add more metadata columns after `PathName` and `Type` output is working.

## Excel-Openable XML Format

Use an XML workbook format that Excel can open directly, such as SpreadsheetML 2003.

The workbook can contain one worksheet named `NodeTree`.

Recommended columns:

```text
PathName
Type
```

Do not create separate sheets for `ctr`, `lst`, and `chc`. The current requirement is one tree of node names.

## Implementation Notes For Future Codex

- Use Python 3.10.10.
- Prefer `xml.etree.ElementTree` unless a strong reason appears.
- Keep parsing independent from EB Tresos runtime.
- Keep the parser generic and testable.
- Preserve document order.
- Do not skip disabled nodes. If a node has `<a:a name="ENABLE" value="false"/>`, it still belongs in the node-name tree if the node itself is `d:*` or `v:*`.
- Do not parse or export attributes as tree nodes in the current version.
