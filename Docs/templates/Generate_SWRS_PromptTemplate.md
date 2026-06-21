# Prompt tạo Software Requirements Specification (SWRS)

## Thông tin đầu vào

- Module: `<ModuleName>`
- Thư mục module: `<ModuleDirectory>`
- File AUTOSAR SWS PDF: `<AUTOSAR_SWS_PDF_FILENAME>`
- File MRS hiện có: `<MRS_FILENAME>`
- File template SWRS: `<SWRS_TEMPLATE_FILENAME>`

Ví dụ cho MCU:

- Module: `MCU`
- Thư mục module: `Mcu`
- File AUTOSAR SWS PDF: `AUTOSAR_SWS_MCUDriver.pdf`
- File MRS hiện có: `MCU_MRS.md`
- File template SWRS: `ModuleName_SWRS_Template.md`

## Đường dẫn

- AUTOSAR SWS: `Docs/references/<AUTOSAR_SWS_PDF_FILENAME>`
- MRS: `Docs/modules/<ModuleDirectory>/<MRS_FILENAME>`
- Template: `Docs/templates/<SWRS_TEMPLATE_FILENAME>`
- File đầu ra: `Docs/modules/<ModuleDirectory>/<ModuleName>_SWRS.md`

## Mục tiêu

Đọc AUTOSAR SWS, MRS hiện có và template để tạo Software Requirements Specification cho module. Chỉ tạo hoặc cập nhật file đầu ra; không sửa các file nguồn và template.

Nếu người dùng chỉ định một category hoặc subsection, chỉ xử lý các block định nghĩa thuộc phạm vi đó. Ví dụ: `7.1.2.1 Reset` hoặc `Reset`.

## 1. Xác định phạm vi requirement

- Quét toàn bộ SWS vì requirement có thể nằm trong Functional Specification, Error Handling, API Specification, Configuration Specification và các phần liên quan.
- Chỉ lấy các block định nghĩa requirement có ID dạng `SWS_<ModuleName>_xxxxx`.
- Không tạo requirement từ ID chỉ xuất hiện trong mục lục, lịch sử thay đổi, bảng traceability hoặc tham chiếu chéo. Một ID chỉ hợp lệ khi tìm được block định nghĩa và nội dung normative tương ứng.
- Giữ đúng thứ tự xuất hiện của block định nghĩa trong PDF.
- Không lấy câu hướng dẫn, note, rationale hoặc mô tả không có Source ID làm requirement độc lập.

## 2. Tạo software requirements

- Tạo đúng một SWRS cho mỗi block requirement SWS hợp lệ.
- Giữ nguyên chính xác `Source ID`. Nếu AUTOSAR có tên requirement riêng thì giữ nguyên; nếu block chỉ có câu requirement, tạo một tiêu đề ngắn gọn mà không thay đổi ý nghĩa.
- Tạo ID nội bộ liên tục: `<ModuleName>_SWRS_001`, `<ModuleName>_SWRS_002`, ...
- Viết requirement ngắn gọn, atomic, testable và giữ nguyên ý nghĩa normative của SWS.
- Không gộp nhiều Source ID. Chỉ tách một Source ID khi nó chứa nhiều hành vi có applicability hoặc verification criteria khác nhau; khi tách, các SWRS phải cùng tham chiếu Source ID đó và ghi lý do trong `Notes / Deviations`.
- Không thêm API, hành vi, giới hạn phần cứng hoặc quyết định thiết kế không có trong nguồn.
- Nếu thiếu dữ liệu, ghi `TBD`; không tự suy diễn.

## 3. Xác định Upstream

- Đọc phần Requirements Traceability trong SWS để lấy quan hệ giữa SRS ID và SWS ID.
- Đọc MRS và lập ánh xạ từ `Source ID` của MRS sang ID nội bộ `<ModuleName>_MRS_xxx`.
- Với mỗi SWRS, chuyển các SRS ID upstream của Source ID tương ứng thành các MRS ID đã ánh xạ được.
- Nếu requirement được dẫn xuất rõ ràng từ một SWS requirement khác, thêm ID SWRS nội bộ tương ứng vào `Upstream`.
- Chỉ thêm quan hệ upstream có bằng chứng trong SWS hoặc MRS; không coi mọi cross-reference hoặc dependency là upstream.
- Cho phép nhiều giá trị, phân tách bằng dấu phẩy, ví dụ: `[MCU_MRS_003], [MCU_SWRS_002]`.
- Nếu không tìm được upstream, ghi `N/A` và giải thích ngắn trong `Notes / Deviations`.

## 4. Tạo block requirement theo template

- Giữ nguyên cấu trúc tài liệu của template. Trong mỗi block requirement, thứ tự trường bắt buộc là: `Type`, `Requirement`, `Verification Criteria`, `Rationale`, `Notes / Deviations`.
- Trong Document Information:
  - `Document ID`: `<ModuleName>_SWRS`;
  - `Module`: `<ModuleName>`;
  - giữ các giá trị project khác từ template nếu đầu vào không cung cấp giá trị mới.
- Mỗi block requirement chỉ chứa tiêu đề, `Type`, `Requirement`, `Verification Criteria`, `Rationale` và `Notes / Deviations`, theo đúng thứ tự này.
- Không lặp Source ID, upstream, category, applicability, dependencies, downstream links hoặc status trong block; các metadata này chỉ được ghi trong Traceability Matrix. Riêng `Type` phải xuất hiện ở đầu mỗi block và đồng thời được ghi trong Traceability Matrix.
- `Verification Criteria` mô tả điều kiện quan sát được để xác nhận requirement, ưu tiên dạng Given/When/Then. Không mô tả thuật toán, thanh ghi hoặc cách triển khai. Nếu nguồn chưa đủ để xác định, ghi `TBD`.
- `Rationale` lấy từ nguồn hoặc ghi `TBD` khi không có.
- `Type` chọn một trong `Functional`, `Interface`, `Error Handling`, `Configuration`, `Non-functional`.
- `Notes / Deviations` ghi giới hạn, giả định, deviation và lý do khi applicability là `Partial`, `Not Applicable` hoặc `TBD`. Nếu không có ghi chú, ghi `None`.

## 5. Tạo Traceability Matrix

- Tạo một dòng cho mỗi SWRS theo đúng thứ tự requirement.
- Mỗi dòng gồm: `SWRS ID`, `SWS Source ID`, `Upstream`, `Category`, `Type`, `Applicability`, `Dependencies`, `Architecture`, `Detailed Design`, `Test IDs`, `Status`.
- `Category`: subsection gần nhất chứa block định nghĩa.
- `Type`: chọn một trong `Functional`, `Interface`, `Error Handling`, `Configuration`, `Non-functional`.
- `Applicability`: kế thừa quyết định liên quan từ MRS hoặc điều kiện rõ ràng trong SWS; nếu chưa đủ bằng chứng, ghi `TBD`.
- `Dependencies`: chỉ ghi prerequisite/dependency được nguồn nêu rõ; nếu không có, ghi `None`.
- `Architecture`, `Detailed Design`, `Test IDs`: `TBD`; `Status`: `Draft`.
- Không để thiếu SWRS ID, Source ID hoặc Upstream.

## 6. Kiểm tra trước khi hoàn tất

- Mỗi block định nghĩa SWS hợp lệ xuất hiện trong đầu ra đúng số lần theo quy tắc tách requirement.
- Không có Source ID chỉ lấy từ bảng traceability, mục lục hoặc tham chiếu chéo.
- ID nội bộ liên tục từ `001`, không trùng và không thiếu số.
- Mọi ID trong `Upstream` tồn tại trong MRS hoặc trong chính SWRS đầu ra.
- Không nhầm `Dependencies` thành `Upstream`.
- Số dòng trong Traceability Matrix bằng số SWRS đã tạo.
- File đầu ra tuân thủ template và không chứa thông tin design tự suy diễn.
- Không sửa bất kỳ file nào ngoài file đầu ra.

## Báo cáo sau khi hoàn tất

Báo lại ngắn gọn:

- Module đã xử lý;
- tổng số block SWS tìm thấy và tổng số SWRS đã tạo;
- Source ID đầu tiên và cuối cùng;
- Source ID bị thiếu, trùng hoặc bị tách, nếu có;
- SWRS không tìm được upstream, nếu có;
- đường dẫn file đầu ra.
