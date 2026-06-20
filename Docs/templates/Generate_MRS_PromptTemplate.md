## Thông tin đầu vào

- Module: `<ModuleName>`
- Tên file AUTOSAR SRS PDF: `<AUTOSAR_SRS_PDF_FILENAME>`
- Tên file template: `<TEMPLATE_FILENAME>`

Ví dụ:
- Module: `Mcu`
- Tên file AUTOSAR SRS PDF: `AUTOSAR_SRS_MCUDriver.pdf`
- Tên file template: `ModuleName_MRS_Template.md`

## Đường dẫn

- File AUTOSAR:
  `docs/references/<AUTOSAR_SRS_PDF_FILENAME>`

- File template:
  `docs/templates/<TEMPLATE_FILENAME>`

- File đầu ra:
  `docs/modules/<module-lowercase>/<ModuleName>_MRS.md`

## Yêu cầu thực hiện

Đọc file AUTOSAR SRS PDF và file template được chỉ định để tạo Module Requirements Specification (MRS).

### 1. Xác định phạm vi requirement

- Tìm phần có tiêu đề `Functional Requirements` trong PDF dựa trên tên tiêu đề, không giả định số chapter hoặc section.
- Đọc toàn bộ requirement thuộc phần `Functional Requirements`.
- Dừng khi sang section cùng cấp tiếp theo không còn thuộc `Functional Requirements`.
- Không xử lý requirement ngoài phạm vi này.

### 2. Tạo requirements

- Tạo một requirement trong file đầu ra cho mỗi requirement AUTOSAR tìm được.
- Giữ đúng thứ tự xuất hiện trong PDF.
- Giữ nguyên chính xác:
  - Source ID;
  - tên requirement AUTOSAR.
- Tạo ID nội bộ tuần tự:
  `<ModuleName>_MRS_001`, `<ModuleName>_MRS_002`, ...
- Viết lại `Requirement` và `Rationale` ngắn gọn, chính xác, không sao chép nguyên văn dài.
- Không thêm hoặc suy diễn thông tin không tồn tại trong PDF.
- Nếu PDF không cung cấp Rationale hoặc thông tin cần thiết, ghi `TBD`.
- Không bỏ sót, tạo trùng hoặc gộp nhiều requirement AUTOSAR thành một requirement.

### 3. Áp dụng template

- Sử dụng chính xác cấu trúc và thứ tự các trường của file template.
- Trong phần `Document Information`:
  - Đổi `Document ID` thành `<ModuleName>_MRS`.
  - Thay mọi placeholder `moduleName` hoặc `ModuleName` bằng tên module phù hợp.
  - Giữ nguyên tất cả trường và giá trị khác.
- Lặp lại đúng block requirement trong template cho từng requirement AUTOSAR.
- Đặt:
  - `Source`: tên tài liệu AUTOSAR, lấy từ PDF hoặc tên file không có phần mở rộng;
  - `Source ID`: Source ID chính xác từ PDF;
  - `Origin`: `AR`;
  - `Category`: tên subsection chứa requirement trong PDF;
  - `Dependencies`: theo PDF; nếu PDF ghi `--` thì dùng `None`;
  - `Architecture`: `TBD`;
  - `Detailed Design`: `TBD`.
- Với các trường còn lại:
  - dùng thông tin có trong PDF hoặc giá trị mặc định của template;
  - nếu không xác định được thì ghi `TBD`.

### 4. Kiểm tra kết quả

Trước khi hoàn tất, kiểm tra:

- Mỗi Source ID trong phần `Functional Requirements` xuất hiện đúng một lần.
- Không có Source ID ngoài phần `Functional Requirements`.
- Số block requirement bằng số requirement AUTOSAR đã tìm thấy.
- ID nội bộ liên tục từ `001`, không trùng và không thiếu số.
- File đầu ra tuân thủ đúng cấu trúc template.
- Không sửa bất kỳ file nào ngoài file đầu ra.

## Báo cáo sau khi hoàn tất

Báo lại:

- Module đã xử lý;
- tổng số requirement đã tạo;
- Source ID đầu tiên và cuối cùng;
- danh sách Source ID bị thiếu hoặc trùng, nếu có;
- đường dẫn file đầu ra.
