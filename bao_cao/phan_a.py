# -*- coding: utf-8 -*-
"""PHAN A: Trang bia, muc luc, danh muc, Mo dau -> Doi tuong & pham vi."""
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from engine import (para, heading, bullet, table, figure, caption, toc,
                    formula, new_section, clear_header, set_page_number_header,
                    FONT, SIZE)


def trang_bia(doc):
    """3.1. Bia bao cao - Trang bia chinh."""
    clear_header(doc.sections[0])

    para(doc, "BỘ GIÁO DỤC VÀ ĐÀO TẠO", align="center", bold=True,
         first_line=0, space_before=6, space_after=2)
    para(doc, "TRƯỜNG ĐẠI HỌC ……………………………", align="center", bold=True,
         first_line=0, space_after=2)
    para(doc, "KHOA ……………………………", align="center", bold=True,
         first_line=0, space_after=40)

    para(doc, "BÁO CÁO TỔNG KẾT", align="center", bold=True, size=Pt(15),
         first_line=0, space_after=4)
    para(doc, "ĐỀ TÀI NGHIÊN CỨU KHOA HỌC CỦA SINH VIÊN",
         align="center", bold=True, size=Pt(15), first_line=0, space_after=36)

    para(doc,
         "SO SÁNH VÀ ĐÁNH GIÁ HIỆU QUẢ GIỮA CHIẾN LƯỢC GIAO DỊCH "
         "DỰA TRÊN TÍN HIỆU KỸ THUẬT VÀ CHIẾN LƯỢC DỰA TRÊN TRÍ TUỆ "
         "NHÂN TẠO TRONG GIAO DỊCH VÀNG",
         align="center", bold=True, size=Pt(16), first_line=0,
         space_after=40, line=1.5)

    para(doc, "Thuộc nhóm ngành khoa học: Kinh tế – Tài chính", align="center",
         italic=True, first_line=0, space_after=60)

    para(doc, "Sinh viên thực hiện:", align="left", bold=True, first_line=0,
         space_after=4)
    for i in range(1, 5):
        para(doc, f"{i}. …………………………………      Mã SV: ……………      Lớp: ……………",
             align="left", first_line=0.6, space_after=4)

    para(doc, "Người hướng dẫn: …………………………………………………",
         align="left", bold=True, first_line=0, space_before=10, space_after=60)

    para(doc, "Hà Nội, tháng …… năm ……", align="center", bold=True,
         first_line=0, space_after=0)


def muc_luc_va_danh_muc(doc):
    """3.2 Muc luc; 3.3 Danh muc bang bieu; 3.4 Danh muc tu viet tat."""
    # Section rieng, danh so trang bang chu so La Ma thuong (i, ii, iii...)
    new_section(doc, page_numbers=True, restart_at=1, fmt="lowerRoman")

    heading(doc, "MỤC LỤC", level=1, align="center")
    toc(doc, ' TOC \\o "1-3" \\h \\z \\u ')

    heading(doc, "DANH MỤC BẢNG BIỂU", level=1, align="center", page_break=True)
    toc(doc, ' TOC \\h \\z \\c "Bảng" ')

    heading(doc, "DANH MỤC HÌNH VẼ", level=1, align="center", page_break=True)
    toc(doc, ' TOC \\h \\z \\c "Hình" ')

    # --- Danh muc tu viet tat: xep theo thu tu bang chu cai ---
    heading(doc, "DANH MỤC NHỮNG TỪ VIẾT TẮT", level=1, align="center",
            page_break=True)
    table(
        doc,
        headers=["Từ viết tắt", "Nguyên nghĩa"],
        rows=[
            ["AI", "Artificial Intelligence – Trí tuệ nhân tạo"],
            ["AMH", "Adaptive Market Hypothesis – Giả thuyết thị trường thích nghi"],
            ["ARCH", "Autoregressive Conditional Heteroskedasticity"],
            ["AUC", "Area Under the ROC Curve – Diện tích dưới đường ROC"],
            ["BB", "Bollinger Bands – Dải Bollinger"],
            ["bps", "Basis point – Điểm cơ bản (1 bps = 0,01%)"],
            ["CAGR", "Compound Annual Growth Rate – Tốc độ tăng trưởng kép hàng năm"],
            ["COMEX", "Commodity Exchange – Sàn giao dịch hàng hóa New York"],
            ["DXY", "US Dollar Index – Chỉ số đồng đô la Mỹ"],
            ["EMA", "Exponential Moving Average – Trung bình động hàm mũ"],
            ["EMH", "Efficient Market Hypothesis – Giả thuyết thị trường hiệu quả"],
            ["FN", "False Negative – Âm tính giả"],
            ["FP", "False Positive – Dương tính giả"],
            ["MA", "Moving Average – Trung bình động"],
            ["MACD", "Moving Average Convergence Divergence"],
            ["MaxDD", "Maximum Drawdown – Mức sụt giảm tối đa"],
            ["MSE", "Mean Squared Error – Sai số bình phương trung bình"],
            ["OHLCV", "Open – High – Low – Close – Volume"],
            ["OOS", "Out-of-sample – Ngoài mẫu"],
            ["ROC", "Receiver Operating Characteristic"],
            ["RSI", "Relative Strength Index – Chỉ số sức mạnh tương đối"],
            ["SHAP", "SHapley Additive exPlanations"],
            ["TA", "Technical Analysis – Phân tích kỹ thuật"],
            ["TN", "True Negative – Âm tính thật"],
            ["TP", "True Positive – Dương tính thật"],
            ["VIX", "CBOE Volatility Index – Chỉ số biến động"],
            ["XGBoost", "eXtreme Gradient Boosting"],
        ],
        widths=[1.6, 6.4],
        font_size=11,
    )


def mo_dau(doc):
    """3.5. Mo dau."""
    # Section noi dung chinh: danh so trang Arabic, bat dau lai tu 1
    new_section(doc, page_numbers=True, restart_at=1, fmt="decimal")

    heading(doc, "MỞ ĐẦU", level=1, align="center")

    para(doc,
         "Vàng là một trong những tài sản có lịch sử giao dịch lâu dài nhất và "
         "giữ vai trò đặc biệt trong hệ thống tài chính toàn cầu. Khác với cổ "
         "phiếu hay trái phiếu, vàng không sinh dòng tiền nội tại, giá trị của "
         "nó được xác lập chủ yếu qua quan hệ cung – cầu, kỳ vọng lạm phát, "
         "chính sách tiền tệ và nhu cầu trú ẩn an toàn. Chính đặc tính này khiến "
         "việc dự báo biến động giá vàng trở thành một bài toán vừa có giá trị "
         "thực tiễn cao, vừa là thách thức học thuật đáng kể.")

    para(doc,
         "Trong hai thập niên gần đây, hoạt động giao dịch trên thị trường vàng "
         "đã dịch chuyển mạnh từ ra quyết định thủ công sang giao dịch tự động "
         "dựa trên quy tắc. Hai cách tiếp cận nổi bật cùng tồn tại. Cách tiếp "
         "cận thứ nhất, giao dịch dựa trên tín hiệu kỹ thuật (signal-based), sử "
         "dụng các chỉ báo được xây dựng từ chuỗi giá quá khứ như trung bình "
         "động, chỉ số sức mạnh tương đối hay đường phân kỳ hội tụ trung bình "
         "động để phát sinh tín hiệu mua – bán theo những quy tắc cố định, minh "
         "bạch và dễ kiểm chứng. Cách tiếp cận thứ hai, giao dịch dựa trên trí "
         "tuệ nhân tạo (AI-based), sử dụng các mô hình học máy để học quan hệ "
         "phi tuyến giữa nhiều biến đầu vào và hướng biến động giá, từ đó phát "
         "sinh tín hiệu một cách linh hoạt theo trạng thái thị trường.")

    para(doc,
         "Câu hỏi đặt ra là: liệu sự phức tạp tăng thêm của mô hình trí tuệ nhân "
         "tạo có thực sự chuyển hóa thành hiệu quả giao dịch vượt trội so với "
         "các chiến lược kỹ thuật truyền thống? Trên thực tế, phần lớn các nghiên "
         "cứu công bố chỉ dừng ở việc báo cáo độ chính xác dự báo của mô hình mà "
         "không kiểm chứng xem độ chính xác đó có chuyển thành lợi nhuận sau khi "
         "trừ chi phí giao dịch hay không, cũng không đối chiếu với các benchmark "
         "bắt buộc như chiến lược nắm giữ thụ động. Khoảng trống này khiến nhiều "
         "kết luận về ưu thế của trí tuệ nhân tạo trong giao dịch còn thiếu cơ sở "
         "vững chắc.")

    para(doc,
         "Đề tài này thực hiện một so sánh có kiểm soát giữa hai cách tiếp cận "
         "nêu trên, trên cùng một bộ dữ liệu giá vàng giai đoạn 2015 – 2025, với "
         "cùng một thiết kế kiểm định ngoài mẫu và cùng một hệ thống chỉ tiêu "
         "đánh giá gồm lợi nhuận, mức độ rủi ro và tính ổn định. Điểm khác biệt "
         "về phương pháp của đề tài là việc đặt trọng tâm vào tính trung thực "
         "của kết quả: toàn bộ quy trình được thiết kế để loại trừ rò rỉ thông "
         "tin tương lai, chi phí giao dịch được tính đầy đủ, và chất lượng dữ "
         "liệu đầu vào được kiểm định độc lập trước khi diễn giải bất kỳ kết quả "
         "dự báo nào.")

    para(doc,
         "Báo cáo được cấu trúc thành bốn chương nội dung. Chương 1 trình bày cơ "
         "sở lý thuyết về khả năng dự báo của thị trường, phân tích kỹ thuật và "
         "mô hình XGBoost. Chương 2 mô tả dữ liệu, quy trình xây dựng đặc trưng, "
         "kết quả kiểm định chất lượng dữ liệu và thiết kế thực nghiệm. Chương 3 "
         "trình bày kết quả dự báo, kết quả so sánh hiệu quả các chiến lược và "
         "kiểm định tính ổn định. Chương 4 thảo luận, đối chiếu với lý thuyết và "
         "phân tích các hạn chế. Phần cuối đưa ra kết luận và kiến nghị.")


def tong_quan(doc):
    """3.6. Tong quan tinh hinh nghien cuu thuoc linh vuc de tai."""
    heading(doc, "TỔNG QUAN TÌNH HÌNH NGHIÊN CỨU THUỘC LĨNH VỰC ĐỀ TÀI",
            level=1, align="center", page_break=True)

    heading(doc, "1. Nghiên cứu về khả năng dự báo của thị trường tài chính",
            level=2)
    para(doc,
         "Nền tảng lý thuyết của mọi nghiên cứu về dự báo giá tài sản là Giả "
         "thuyết Thị trường Hiệu quả do Fama (1970) đề xuất. Ở dạng yếu, giả "
         "thuyết này khẳng định giá hiện tại đã phản ánh toàn bộ thông tin chứa "
         "trong dữ liệu giá quá khứ, do đó không thể sử dụng thông tin quá khứ "
         "để thu lợi nhuận vượt trội một cách hệ thống. Hệ quả trực tiếp là các "
         "chỉ báo phân tích kỹ thuật – vốn đều là hàm số của chuỗi giá quá khứ – "
         "về mặt lý thuyết không có năng lực dự báo.")
    para(doc,
         "Lo (2004) đưa ra Giả thuyết Thị trường Thích nghi như một cách dung "
         "hòa giữa lý thuyết hiệu quả và các bằng chứng thực nghiệm trái ngược. "
         "Theo đó, hiệu quả thị trường không phải trạng thái tĩnh mà biến đổi "
         "theo thời gian: các cơ hội sinh lợi xuất hiện, bị khai thác rồi biến "
         "mất khi đủ nhiều nhà đầu tư tham gia. Quan điểm này có hàm ý phương "
         "pháp luận quan trọng là mô hình dự báo cần được tái huấn luyện định kỳ "
         "thay vì huấn luyện một lần duy nhất.")

    heading(doc, "2. Nghiên cứu ứng dụng học máy trong dự báo giá tài sản",
            level=2)
    para(doc,
         "Hướng nghiên cứu ứng dụng học máy vào dự báo thị trường tài chính đã "
         "phát triển mạnh trong khoảng mười năm gần đây, với các thuật toán phổ "
         "biến gồm máy vectơ hỗ trợ, rừng ngẫu nhiên, mạng nơ-ron hồi tiếp và "
         "các biến thể tăng cường gradient. Trong nhóm này, XGBoost do Chen và "
         "Guestrin (2016) đề xuất được sử dụng rộng rãi nhờ ba đặc tính phù hợp "
         "với dữ liệu tài chính: khả năng học quan hệ phi tuyến và tương tác "
         "giữa các biến, cơ chế điều chuẩn tích hợp giúp hạn chế quá khớp trên "
         "dữ liệu nhiễu cao, và khả năng diễn giải thông qua độ quan trọng đặc "
         "trưng.")
    para(doc,
         "Tuy nhiên, khảo sát các công bố hiện có cho thấy ba hạn chế phương "
         "pháp lặp lại khá phổ biến. Thứ nhất, nhiều nghiên cứu sử dụng kiểm "
         "định chéo ngẫu nhiên trên chuỗi thời gian, làm tập huấn luyện chứa "
         "quan sát xảy ra sau tập kiểm định và dẫn tới kết quả bị phóng đại một "
         "cách hệ thống. Thứ hai, kết quả thường được báo cáo dưới dạng độ chính "
         "xác phân loại mà không chuyển thành hiệu quả giao dịch có tính chi phí. "
         "Thứ ba, phần lớn nghiên cứu thiếu benchmark thụ động, trong khi một "
         "chiến lược chủ động chỉ tạo ra giá trị kinh tế nếu vượt được chiến "
         "lược nắm giữ đơn thuần sau chi phí.")

    heading(doc, "3. Nghiên cứu về đánh giá hiệu quả chiến lược giao dịch",
            level=2)
    para(doc,
         "Về khung đánh giá, Sharpe (1966) đề xuất tỷ số lợi nhuận trên một đơn "
         "vị rủi ro tổng, đến nay vẫn là thước đo hiệu quả điều chỉnh rủi ro phổ "
         "biến nhất. Sortino và Price (1994) chỉ ra hạn chế của tỷ số Sharpe khi "
         "phạt cả biến động tăng, và đề xuất chỉ tính độ lệch chuẩn phần âm. "
         "Bailey và López de Prado (2014) cảnh báo về thiên lệch lựa chọn trong "
         "backtest: khi thử nghiệm nhiều biến thể chiến lược rồi báo cáo kết quả "
         "tốt nhất, tỷ số Sharpe quan sát được bị phóng đại, và đề xuất chỉ tiêu "
         "hiệu chỉnh Deflated Sharpe Ratio.")
    para(doc,
         "Về kiểm định chất lượng dữ liệu, các nghiên cứu về tính chất chuỗi giá "
         "tài chính của Mandelbrot (1963) và Engle (1982) xác lập hai đặc trưng "
         "thống kê quan trọng: chuỗi lợi suất có tự tương quan gần bằng không "
         "trong khi chuỗi biến động có tự tương quan dương và bền vững – hiện "
         "tượng tụ cụm biến động. Hai đặc trưng này cung cấp tiêu chí khách quan "
         "để kiểm tra xem một chuỗi dữ liệu có phản ánh hành vi thị trường thực "
         "hay đã bị biến dạng bởi quá trình xử lý.")

    heading(doc, "4. Khoảng trống nghiên cứu mà đề tài hướng tới", level=2)
    para(doc,
         "Từ tổng quan trên, đề tài xác định ba khoảng trống. Một là thiếu các "
         "nghiên cứu so sánh trực tiếp chiến lược trí tuệ nhân tạo với chiến "
         "lược kỹ thuật truyền thống trên cùng dữ liệu, cùng thiết kế kiểm định "
         "và cùng hệ chỉ tiêu. Hai là thiếu sự kết nối giữa chất lượng dự báo "
         "thống kê và hiệu quả giao dịch thực tế sau chi phí. Ba là bước kiểm "
         "định chất lượng dữ liệu đầu vào thường bị bỏ qua, trong khi đây là "
         "nguyên nhân phổ biến nhất của các kết quả không thể tái lập trong tài "
         "chính định lượng. Đề tài này được thiết kế để giải quyết đồng thời cả "
         "ba khoảng trống đó.")


def ly_do_chon_de_tai(doc):
    """3.7. Ly do lua chon de tai."""
    heading(doc, "LÝ DO LỰA CHỌN ĐỀ TÀI", level=1, align="center",
            page_break=True)

    para(doc, "Đề tài được lựa chọn dựa trên bốn lý do sau.", first_line=1.0)

    heading(doc, "1. Tính cấp thiết về mặt thực tiễn", level=2)
    para(doc,
         "Giai đoạn 2020 – 2025 chứng kiến biến động đặc biệt mạnh của giá vàng "
         "thế giới, với mức tăng lũy kế vượt 170% và riêng năm 2025 tăng gần "
         "68%. Bối cảnh này làm gia tăng nhu cầu về các công cụ hỗ trợ ra quyết "
         "định giao dịch có cơ sở định lượng. Đồng thời, sự phổ cập của các nền "
         "tảng giao dịch tự động và thư viện học máy nguồn mở khiến việc triển "
         "khai chiến lược dựa trên trí tuệ nhân tạo trở nên khả thi với cả nhà "
         "đầu tư cá nhân, làm cho câu hỏi về hiệu quả thực sự của cách tiếp cận "
         "này trở nên cấp thiết.")

    heading(doc, "2. Tính mới về mặt phương pháp", level=2)
    para(doc,
         "Khác với phần lớn các nghiên cứu chỉ dừng ở chỉ số độ chính xác, đề "
         "tài xây dựng một quy trình đánh giá hai lớp: lớp thứ nhất đánh giá "
         "chất lượng dự báo thống kê, lớp thứ hai chuyển dự báo thành chiến lược "
         "giao dịch có tính chi phí và đánh giá bằng hệ chỉ tiêu tài chính. "
         "Việc bổ sung bước kiểm định chất lượng dữ liệu độc lập trước khi diễn "
         "giải kết quả, cùng với thí nghiệm đối chứng trên nguồn dữ liệu thứ hai, "
         "là điểm khác biệt về phương pháp so với các công bố tương tự.")

    heading(doc, "3. Khả năng ứng dụng của kết quả", level=2)
    para(doc,
         "Kết quả nghiên cứu cung cấp bằng chứng định lượng về đánh đổi giữa lợi "
         "nhuận và rủi ro của hai cách tiếp cận, giúp nhà đầu tư lựa chọn chiến "
         "lược phù hợp với mức chấp nhận rủi ro của mình. Bộ chương trình được "
         "xây dựng có tính tái sử dụng, có thể áp dụng cho các tài sản khác mà "
         "không cần thay đổi cấu trúc.")

    heading(doc, "4. Phù hợp với năng lực và điều kiện thực hiện", level=2)
    para(doc,
         "Đề tài sử dụng dữ liệu giá công khai và các thư viện phân tích nguồn "
         "mở, không đòi hỏi chi phí thu thập dữ liệu hay hạ tầng tính toán đặc "
         "biệt. Phạm vi nghiên cứu được giới hạn ở một tài sản và một khung thời "
         "gian, bảo đảm tính khả thi trong thời lượng thực hiện đề tài nghiên "
         "cứu khoa học sinh viên.")


def muc_tieu_noi_dung_phuong_phap(doc):
    """3.8. Muc tieu, noi dung, phuong phap nghien cuu."""
    heading(doc, "MỤC TIÊU, NỘI DUNG, PHƯƠNG PHÁP NGHIÊN CỨU",
            level=1, align="center", page_break=True)

    heading(doc, "1. Mục tiêu nghiên cứu", level=2)
    para(doc, "Mục tiêu tổng quát:", bold=True, first_line=0, space_after=2)
    para(doc,
         "So sánh và đánh giá hiệu quả giữa chiến lược giao dịch tự động dựa "
         "trên tín hiệu kỹ thuật và chiến lược dựa trên trí tuệ nhân tạo trong "
         "giao dịch vàng, thông qua ba tiêu chí: lợi nhuận, mức độ rủi ro và "
         "tính ổn định của chiến lược.")
    para(doc, "Mục tiêu cụ thể:", bold=True, first_line=0, space_after=2)
    bullet(doc, "Xây dựng tập đặc trưng từ các chỉ báo kỹ thuật và huấn luyện "
                "mô hình XGBoost dự báo hướng biến động giá vàng ngày kế tiếp.")
    bullet(doc, "Định lượng đóng góp của từng nhóm đặc trưng vào năng lực dự "
                "báo của mô hình.")
    bullet(doc, "Chuyển đầu ra của mô hình thành chiến lược giao dịch và đánh "
                "giá hiệu quả bằng các chỉ tiêu Sharpe, Sortino, Max Drawdown, "
                "Calmar.")
    bullet(doc, "So sánh chiến lược trí tuệ nhân tạo với bốn chiến lược tín "
                "hiệu kỹ thuật và benchmark nắm giữ thụ động.")
    bullet(doc, "Kiểm định chất lượng dữ liệu đầu vào và đánh giá mức độ tin "
                "cậy của các kết luận.")

    heading(doc, "2. Nội dung nghiên cứu", level=2)
    para(doc, "Đề tài triển khai sáu nội dung chính:", first_line=1.0)
    bullet(doc, "Nội dung 1: Hệ thống hóa cơ sở lý thuyết về khả năng dự báo "
                "của thị trường, phân tích kỹ thuật và thuật toán XGBoost.")
    bullet(doc, "Nội dung 2: Thu thập, kiểm định chất lượng và xử lý dữ liệu "
                "giá vàng giai đoạn 2015 – 2025.")
    bullet(doc, "Nội dung 3: Xây dựng tập 14 đặc trưng thuộc bốn nhóm (xu "
                "hướng, động lượng, biến động, đặc trưng trễ).")
    bullet(doc, "Nội dung 4: Huấn luyện mô hình XGBoost theo thiết kế "
                "walk-forward và đánh giá chất lượng dự báo.")
    bullet(doc, "Nội dung 5: Xây dựng và backtest tám chiến lược giao dịch, "
                "tính toán hệ chỉ tiêu đánh giá.")
    bullet(doc, "Nội dung 6: Phân tích so sánh, diễn giải mô hình và đánh giá "
                "hạn chế.")

    heading(doc, "3. Phương pháp nghiên cứu", level=2)

    heading(doc, "3.1. Phương pháp thu thập và xử lý dữ liệu", level=3)
    para(doc,
         "Dữ liệu sơ cấp là chuỗi giá vàng dạng OHLCV theo ngày giai đoạn "
         "02/01/2015 – 30/12/2025. Dữ liệu được kiểm định chất lượng bằng ba "
         "phép kiểm định thống kê trước khi sử dụng: tỷ lệ bước giá trùng lặp, "
         "hệ số tự tương quan của log-return, và phân bố quan sát theo ngày "
         "trong tuần. Một nguồn dữ liệu thứ hai được thu thập độc lập để thực "
         "hiện thí nghiệm đối chứng.")

    heading(doc, "3.2. Phương pháp mô hình hóa", level=3)
    para(doc,
         "Bài toán được phát biểu dưới dạng phân loại nhị phân với biến mục tiêu "
         "là dấu của log-return ngày kế tiếp. Mô hình sử dụng là XGBoost với các "
         "siêu tham số được lựa chọn theo cơ sở lý luận về đặc tính nhiễu cao "
         "của dữ liệu tài chính. Đầu ra của mô hình là xác suất, được chuyển "
         "thành nhãn dự báo qua ngưỡng phân loại và được kiểm định mức độ hiệu "
         "chuẩn.")

    heading(doc, "3.3. Phương pháp kiểm định ngoài mẫu", level=3)
    para(doc,
         "Đề tài sử dụng thiết kế walk-forward với cửa sổ mở rộng thay vì kiểm "
         "định chéo ngẫu nhiên, nhằm tôn trọng ràng buộc nhân quả theo thời gian "
         "và loại trừ rò rỉ thông tin tương lai. Mô hình được tái huấn luyện "
         "định kỳ để thích nghi với hiện tượng trôi khái niệm.")

    heading(doc, "3.4. Phương pháp phân tích đóng góp đặc trưng", level=3)
    para(doc,
         "Đóng góp của từng nhóm đặc trưng được định lượng bằng ablation study: "
         "huấn luyện lại mô hình từ đầu với từng tập con đặc trưng cộng dồn và "
         "so sánh hiệu năng ngoài mẫu. Kết quả được đối chiếu với độ quan trọng "
         "Gain nội bộ của mô hình và giá trị SHAP.")

    heading(doc, "3.5. Phương pháp đánh giá hiệu quả chiến lược", level=3)
    para(doc,
         "Mỗi chiến lược được backtest theo quy ước thực thi bảo đảm tín hiệu "
         "không biết trước lợi nhuận cùng kỳ, có tính chi phí giao dịch theo mức "
         "thay đổi vị thế. Hiệu quả được đánh giá đồng thời bằng nhóm chỉ tiêu "
         "lợi nhuận, nhóm chỉ tiêu rủi ro, nhóm chỉ tiêu hiệu quả điều chỉnh rủi "
         "ro và nhóm chỉ tiêu tính ổn định.")

    heading(doc, "4. Công cụ nghiên cứu", level=2)
    para(doc,
         "Toàn bộ phân tích được thực hiện bằng ngôn ngữ Python với các thư viện "
         "pandas và NumPy cho xử lý dữ liệu, xgboost cho mô hình hóa, "
         "scikit-learn cho các chỉ số đánh giá, shap cho diễn giải mô hình, và "
         "matplotlib cùng seaborn cho trực quan hóa. Mã nguồn được tổ chức thành "
         "năm chương trình độc lập theo chức năng, bảo đảm khả năng tái lập kết "
         "quả.")


def doi_tuong_pham_vi(doc):
    """3.9. Doi tuong va pham vi nghien cuu."""
    heading(doc, "ĐỐI TƯỢNG VÀ PHẠM VI NGHIÊN CỨU", level=1, align="center",
            page_break=True)

    heading(doc, "1. Đối tượng nghiên cứu", level=2)
    para(doc,
         "Đối tượng nghiên cứu là hiệu quả của hai cách tiếp cận xây dựng chiến "
         "lược giao dịch vàng: chiến lược dựa trên tín hiệu kỹ thuật và chiến "
         "lược dựa trên mô hình học máy XGBoost. Hiệu quả được xem xét đồng thời "
         "trên ba khía cạnh là lợi nhuận, mức độ rủi ro và tính ổn định.")

    heading(doc, "2. Phạm vi nghiên cứu", level=2)

    heading(doc, "2.1. Phạm vi về tài sản", level=3)
    para(doc,
         "Nghiên cứu giới hạn ở một tài sản duy nhất là vàng, cụ thể là chuỗi "
         "giá hợp đồng vàng tương lai. Việc giới hạn một tài sản cho phép kiểm "
         "soát các yếu tố đặc thù và tập trung vào so sánh phương pháp.")

    heading(doc, "2.2. Phạm vi về thời gian", level=3)
    para(doc,
         "Dữ liệu bao phủ giai đoạn 02/01/2015 – 30/12/2025, tổng cộng 4.016 "
         "quan sát. Trong đó, khoảng 1.825 quan sát đầu tiên được dùng làm tập "
         "huấn luyện ban đầu; giai đoạn đánh giá ngoài mẫu là 19/02/2020 – "
         "29/12/2025 với 2.141 quan sát.")

    heading(doc, "2.3. Phạm vi về khung thời gian giao dịch", level=3)
    para(doc,
         "Nghiên cứu sử dụng dữ liệu tần số ngày và bài toán dự báo hướng giá "
         "cho một ngày kế tiếp. Các khung thời gian trong ngày và các horizon "
         "dự báo dài hơn không thuộc phạm vi đề tài.")

    heading(doc, "2.4. Phạm vi về đặc trưng đầu vào", level=3)
    para(doc,
         "Tập đặc trưng giới hạn ở 14 biến nội sinh được tính từ chuỗi giá và "
         "khối lượng giao dịch. Các biến ngoại sinh như chỉ số đồng đô la Mỹ, "
         "lợi suất trái phiếu hay chỉ số biến động không được đưa vào mô hình "
         "trong phạm vi đề tài này, và được nêu như hướng mở rộng.")

    heading(doc, "2.5. Phạm vi về chiến lược so sánh", level=3)
    para(doc,
         "Nghiên cứu so sánh tám chiến lược gồm: một benchmark thụ động, bốn "
         "chiến lược tín hiệu kỹ thuật đại diện cho cả hai trường phái "
         "trend-following và mean-reversion, và ba biến thể chiến lược dựa trên "
         "trí tuệ nhân tạo. Các chiến lược chỉ sử dụng vị thế toàn phần hoặc "
         "bằng không, không xét đến quản lý khối lượng vị thế theo biến động và "
         "không sử dụng đòn bẩy.")
