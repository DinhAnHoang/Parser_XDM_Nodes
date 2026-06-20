1. XDM Format:
	1. Nodes
	2. Attribute
2. Nodes: 
	1. Generic nodes
	2. Schema nodes
	3. Data nodes
3. node name structure:
	1. Short rule:
		1. '</' Namespace-prefix ':' core-node-type '>'
	2. long rule:
		1.  '<' Namespace-prefix ':' core-node-type [''name="'node name"']
								            [''type="'type-string"'] 
								            [' value='"'value'"']
								            ...								             '>' 
                                
4. Namespace-Prefix
	1. Node name symbol:
		1. common:
			1. a: attribute
			2. v: schema node
			3. d: data node
			4. none: generic node
		2. User created:
			1. define by 'xmlns':''user-defined-name'="link"
	2. Attribute name
		1. ctr: contains
		2. chc: choice nodes
		3. lst: list nodes
		4. var: variable nodes
		5. ref: reference nodes
   
## Namespace Handling

The parser must read all namespace declarations using `ElementTree.iterparse(..., events=["start-ns"])`.

The parser must support namespaces declared at:
- root `<datamodel>`
- nested AUTOSAR factory nodes such as `<d:ctr type="AUTOSAR" factory="autosar">`