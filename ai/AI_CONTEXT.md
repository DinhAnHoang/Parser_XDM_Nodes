# AI Context

This project is for documenting and later building a generic EB Tresos XDM parser.

Current documentation goal:
- Describe how Codex should parse `Can_TS_T40D2M10I1R0/config/Can.xdm`.
- Do not write implementation code in this phase.
- Ignore the folder `Reffer project` completely.

Parser goal for the future implementation:
- Build a generic XDM node-name tree parser first.
- Do not create module-specific parser/model initially.
- Focus example input module: CAN.
- Root the exported tree at the data node list `<d:lst type="TOP-LEVEL-PACKAGES">`.
- Include both schema nodes (`v:*`) and data nodes (`d:*`) in the tree.
- Do not include attributes (`a:*`) as tree nodes for the current output.

Expected input:
- Python script receives a module name parameter.
- Treat `Configuration Tool` as the root path.
- The parser finds a matching `<Module>.xdm` file only under `Can_TS_T40D2M10I1R0/config`.
- Current examples:
  - `CAN` resolves to `Can_TS_T40D2M10I1R0/config/Can.xdm`
  - `Gpt` resolves to `Can_TS_T40D2M10I1R0/config/Gpt.xdm`

Expected output:
- One `.xml` file that can be opened by Excel.
- Output file name should be `<InputFileStem>_NodeTree.xml`, for example `Can_NodeTree.xml` or `Gpt_NodeTree.xml`.
- The XML should contain rows representing the node-name tree.
- Current version exports two values:
  - `PathName`: the slash-separated path name.
  - `Type`: the XML `type` attribute from the same node as the `name` attribute. If the node has no `type`, use `none`.
- Example path names:
  - `TS_T40D2M10I1R0/none/Can`
  - `TS_T40D2M10I1R0/none/Can_EcuParameterDefinition`
  - `TS_T40D2M10I1R0/none/Can_ModuleDescription`

Node name rule:
- For each `d:*` or `v:*` node, use the `name` attribute when it exists.
- If the node has no `name` attribute, use `none`.
- Do not use `type` as a fallback name. Example: `<d:lst type="ELEMENTS">` contributes `none`.
- Attribute nodes such as `<a:a name="UUID" ... />` are ignored for the node-name tree.

Expected workflow:
- Read XDM XML.
- Collect namespaces.
- Find `<d:lst type="TOP-LEVEL-PACKAGES">`.
- Traverse all descendant schema and data nodes in document order.
- Build slash-separated node paths from node names.
- Export path names and node types into an Excel-openable XML workbook.
