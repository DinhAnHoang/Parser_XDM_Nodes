from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parent
CONFIG_DIR = WORKSPACE_ROOT / "Can_TS_T40D2M10I1R0" / "config"

SPREADSHEET_NS = "urn:schemas-microsoft-com:office:spreadsheet"

SUPPORTED_KINDS = {"ctr", "lst", "var", "ref", "chc"}


@dataclass(frozen=True)
class NodeTreeRow:
    path_name: str
    node_type: str


def split_tag(tag: str) -> tuple[str | None, str]:
    if tag.startswith("{"):
        namespace, local_name = tag[1:].split("}", 1)
        return namespace, local_name
    return None, tag


def collect_namespaces(input_path: Path) -> dict[str, str]:
    namespaces: dict[str, str] = {}
    for _, namespace_decl in ET.iterparse(input_path, events=["start-ns"]):
        prefix, uri = namespace_decl
        namespaces[prefix] = uri
    return namespaces


def resolve_input_path(module_name: str) -> Path:
    expected_name = f"{module_name}.xdm".lower()
    matches = [
        candidate
        for candidate in CONFIG_DIR.glob("*.xdm")
        if candidate.name.lower() == expected_name
    ]

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        match_list = "\n".join(str(match) for match in matches)
        raise ValueError(f"Multiple .xdm files found for module {module_name!r}:\n{match_list}")

    raise FileNotFoundError(f"Cannot find input .xdm file for module {module_name!r}")


def find_top_level_packages(root: ET.Element, data_namespace: str) -> ET.Element:
    for element in root.iter():
        namespace, local_name = split_tag(element.tag)
        if (
            namespace == data_namespace
            and local_name == "lst"
            and element.attrib.get("type") == "TOP-LEVEL-PACKAGES"
        ):
            return element
    raise ValueError('Cannot find <d:lst type="TOP-LEVEL-PACKAGES">')


def is_supported_tree_node(
    element: ET.Element,
    data_namespace: str,
    schema_namespace: str,
) -> bool:
    namespace, local_name = split_tag(element.tag)
    return namespace in {data_namespace, schema_namespace} and local_name in SUPPORTED_KINDS


def get_node_type(element: ET.Element) -> str:
    return element.attrib.get("type", "none")


def build_node_tree_rows(
    element: ET.Element,
    parent_path: str,
    data_namespace: str,
    schema_namespace: str,
) -> list[NodeTreeRow]:
    rows: list[NodeTreeRow] = []

    if is_supported_tree_node(element, data_namespace, schema_namespace):
        segment = element.attrib.get("name", "none")
        current_path = f"{parent_path}/{segment}" if parent_path else segment
        rows.append(NodeTreeRow(current_path, get_node_type(element)))
    else:
        current_path = parent_path

    for child in list(element):
        rows.extend(build_node_tree_rows(child, current_path, data_namespace, schema_namespace))

    return rows


def extract_node_tree_rows(input_path: Path) -> list[NodeTreeRow]:
    namespaces = collect_namespaces(input_path)
    data_namespace = namespaces.get("d")
    schema_namespace = namespaces.get("v")

    if not data_namespace:
        raise ValueError("Cannot resolve data namespace prefix 'd'")
    if not schema_namespace:
        raise ValueError("Cannot resolve schema namespace prefix 'v'")

    root = ET.parse(input_path).getroot()
    top_level_packages = find_top_level_packages(root, data_namespace)

    rows: list[NodeTreeRow] = []
    for child in list(top_level_packages):
        rows.extend(build_node_tree_rows(child, "", data_namespace, schema_namespace))
    return rows


def make_cell(value: str) -> ET.Element:
    cell = ET.Element(f"{{{SPREADSHEET_NS}}}Cell")
    data = ET.SubElement(cell, f"{{{SPREADSHEET_NS}}}Data")
    data.set(f"{{{SPREADSHEET_NS}}}Type", "String")
    data.text = value
    return cell


def write_excel_xml(rows: list[NodeTreeRow], output_path: Path) -> None:
    ET.register_namespace("ss", SPREADSHEET_NS)

    workbook = ET.Element(f"{{{SPREADSHEET_NS}}}Workbook")

    worksheet = ET.SubElement(workbook, f"{{{SPREADSHEET_NS}}}Worksheet")
    worksheet.set(f"{{{SPREADSHEET_NS}}}Name", "NodeTree")
    table = ET.SubElement(worksheet, f"{{{SPREADSHEET_NS}}}Table")

    header = ET.SubElement(table, f"{{{SPREADSHEET_NS}}}Row")
    header.append(make_cell("PathName"))
    header.append(make_cell("Type"))

    for row_data in rows:
        row = ET.SubElement(table, f"{{{SPREADSHEET_NS}}}Row")
        row.append(make_cell(row_data.path_name))
        row.append(make_cell(row_data.node_type))

    tree = ET.ElementTree(workbook)
    ET.indent(tree, space="  ", level=0)

    with output_path.open("wb") as file:
        file.write(b'<?xml version="1.0"?>\n')
        file.write(b'<?mso-application progid="Excel.Sheet"?>\n')
        tree.write(file, encoding="utf-8", xml_declaration=False)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python xdm_node_tree_export.py <MODULE>")
        return 2

    module_name = argv[1]
    input_path = resolve_input_path(module_name)
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    output_path = WORKSPACE_ROOT / f"{input_path.stem}_NodeTree.xml"
    rows = extract_node_tree_rows(input_path)
    write_excel_xml(rows, output_path)

    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
